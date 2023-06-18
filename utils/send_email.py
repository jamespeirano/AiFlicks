import os
import smtplib
from email.utils import formataddr
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import dotenv_values
import base64
from pathlib import Path

config = dotenv_values(".env")
sender_email = config['SENDER_EMAIL']
password_email = config['PASSWORD_EMAIL']

# Set the images directory in this folder to be the path for the images
images_dir = Path(__file__).resolve().parent / 'images'

PORT = 587
EMAIL_SERVER = "smtp-mail.outlook.com"


def decode_base64(data, output_file):
    with open(output_file, 'wb') as f:
        f.write(base64.b64decode(data))

def create_msg(subject, receiver_email, cart_items, name, address, phone, invoice_no, amount, to_customer, image_path):
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = formataddr(("AI FLICKS", sender_email))
    msg["To"] = receiver_email
    msg["BCC"] = sender_email

    address = f"{address['line1']}, {address['city']}, {address['state']} {address['postal_code']}, {address['country']}"

    table_header = """
    <tr style='background-color: #4CAF50;'>
        <th style='border: 1px solid #ddd; padding: 8px; color: white;'>Name</th>
        <th style='border: 1px solid #ddd; padding: 8px; color: white;'>Size</th>
        <th style='border: 1px solid #ddd; padding: 8px; color: white;'>Color</th>
        <th style='border: 1px solid #ddd; padding: 8px; color: white;'>Price</th>
        <th style='border: 1px solid #ddd; padding: 8px; color: white;'>Quantity</th>
    </tr>
    """

    table_rows = "".join(
        f"""
        <tr>
            <td style='border: 1px solid #ddd; padding: 8px;'>{item['name']}</td>
            <td style='border: 1px solid #ddd; padding: 8px;'>{item['size']}</td>
            <td style='border: 1px solid #ddd; padding: 8px;'>{item['color']}</td>
            <td style='border: 1px solid #ddd; padding: 8px;'>{item['price']}</td>
            <td style='border: 1px solid #ddd; padding: 8px;'>{item['quantity']}</td>
        </tr>
        """
        for item in cart_items
    )

    if to_customer:
        content = f"""
        <html>
            <body>
                <p>Dear <strong>{name}</strong>,</p>
                <p>Thank you for your purchase. Here is your receipt for the following items:</p>
                <table style='font-family: Arial, Helvetica, sans-serif; border-collapse: collapse; width: 50%;'>
                    {table_header}
                    {table_rows}
                </table>
                <p>Your total amount is <strong>{amount}</strong>.</p>
                <p>Your invoice number is <strong>{invoice_no}</strong>.</p>
                <p>Your custom products are on their way to:</p>
                <p>Address: <strong>{address}</strong><br>Phone: <strong>{phone}</strong></p>
                <p>Best regards,<br><strong>AiFlics</strong></p>
            </body>
        </html>
        """
    else:
        content = f"""
        <html>
            <body>
                <p>Customer name: <strong>{name}</strong></p>
                <table style='font-family: Arial, Helvetica, sans-serif; border-collapse: collapse; width: 50%;'>
                    {table_header}
                    {table_rows}
                </table>
                <p>The total amount is <strong>{amount}</strong>.</p>
                <p>Invoice #: <strong>{invoice_no}</strong></p>
                <p>Shipping details:<br>Address: <strong>{address}</strong><br>Phone: <strong>{phone}</strong></p>
                <p>Best regards,<br><strong>AiFlics</strong></p>
            </body>
        </html>
        """

    msg.attach(MIMEText(content, 'html'))

    with open(image_path, 'rb') as img:
        mime = MIMEImage(img.read())
        mime.add_header('Content-Disposition', 'attachment', filename=image_path)
        msg.attach(mime)

    return msg


def send_email(subject, receiver_email, name, address, phone, invoice_no, amount, to_customer, cart_items):
    for item in cart_items:
        image_path = images_dir / f"{item['name']}.png"
        decode_base64(item['image'], str(image_path))
        msg = create_msg(subject, receiver_email, cart_items, name, address, phone, invoice_no, amount, to_customer, str(image_path))
        with smtplib.SMTP(EMAIL_SERVER, PORT) as server:
            server.starttls()
            server.login(sender_email, password_email)
            server.send_message(msg)

        # Remove the image file after the email is sent
        os.remove(image_path)