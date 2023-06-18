import os
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from dotenv import dotenv_values

config = dotenv_values(".env")

PORT = 587
EMAIL_SERVER = "smtp-mail.outlook.com"

sender_email = config['SENDER_EMAIL']
password_email = config['PASSWORD_EMAIL']

def format_cart_items(cartItems):
    return "\n".join(
        f"{item['quantity']}x {item['name']} (size: {item['size']}, color: {item['color']}, image: {item['image']})"
        for item in cartItems
    )

def create_msg(subject, receiver_email, formatted_cart_items, name, address, phone, invoice_no, amount, toCustomer):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = formataddr(("AI FLICKS", f"{sender_email}"))
    msg["To"] = receiver_email
    msg["BCC"] = sender_email
    
    if toCustomer:
        content = f"""\
            Hi {name},
            Here is your receipt for the following items:
            {formatted_cart_items}
            Total amount: {amount}.
            Your invoice # is {invoice_no}.
            Your custom products are on their way to:
            Address: {address}
            Phone: {phone}
            Best regards,
            AiFlics
            """
        alternative_content = f"""\
            <html>
                <body>
                    <p>Hi {name},</p>
                    <p>Here is your receipt for the following items:</p>
                    <p>{formatted_cart_items}</p>
                    <p>Total amount: {amount}.</p>
                    <p>Your invoice # is {invoice_no}.</p>
                    <p>Your custom products are on their way to:</p>
                    <p>Address: {address}</p>
                    <p>Phone: {phone}</p>
                    <p>Best regards,</p>
                    <p>AiFlics</p>
                </body>
            </html>
            """
    else:
        content = f"""\
            Customer name: {name},
            Total amount: {amount},
            Invoice #: {invoice_no},
            Shipping details:
            Address: {address},
            Phone: {phone},
            Ordered items:
            {formatted_cart_items}
            """
        alternative_content = f"""\
            <html>
                <body>
                    <p>Customer name: {name},</p>
                    <p>Total amount: {amount}.</p>
                    <p>Invoice #: {invoice_no}.</p>
                    <p>Shipping details:</p>
                    <p>Address: {address}</p>
                    <p>Phone: {phone}</p>
                    <p>Ordered items:</p>
                    <p>{formatted_cart_items}</p>
                </body>
            </html>
            """
    msg.set_content(content)
    msg.add_alternative(alternative_content, subtype="html")
    return msg

def send_email(subject, receiver_email, name, address, phone, invoice_no, amount, toCustomer=False, cartItems=None):
    formatted_cart_items = format_cart_items(cartItems)
    msg = create_msg(subject, receiver_email, formatted_cart_items, name, address, phone, invoice_no, amount, toCustomer)

    with smtplib.SMTP(EMAIL_SERVER, PORT) as server:
        server.starttls()
        server.login(sender_email, password_email)
        server.sendmail(sender_email, receiver_email, msg.as_string())