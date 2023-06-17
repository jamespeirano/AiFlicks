import os
import smtplib
from email.message import EmailMessage
from email.utils import formataddr

from dotenv import load_dotenv  

load_dotenv()


PORT = 587  
EMAIL_SERVER = "smtp-mail.outlook.com"  # Adjust server address, if you are not using @outlook

# Read environment variables
sender_email = os.getenv("EMAIL")
password_email = os.getenv("PASSWORD")


def send_email(subject, receiver_email, name, address, phone, invoice_no, amount, toCustomer=False, cartItems=None):

    # Create the base text message.
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = formataddr(("AiFlics!", f"{sender_email}"))
    msg["To"] = receiver_email
    msg["BCC"] = sender_email

    if toCustomer:
      msg.set_content(
          f"""\
          Hi {name},
          Here is your receipt for {cartItems} in the total amount of {amount}.
          your invoice # is {invoice_no}.
          Your custom products are on their way to:
          Address: {address}
          Phone: {phone}
          Best regards,
          AiFlics
          """
      )
      # Add the html version.  This converts the message into a multipart/alternative
      # container, with the original text message as the first part and the new html
      # message as the second part.
      msg.add_alternative(
          f"""\
      <html>
        <body>
          <p>Here is your receipt for {cartItems} in the total amount of {amount}.</p>
          <p>Your invoice # is {invoice_no}.</p>
          <p>Your custom products are on their way to:</p>
          <p>Address: {address}</p>
          <p>Phone: {phone}</p>
          <p>Best regards,</p>
          <p>AiFlics</p>
        </body>
      </html>
      """,
          subtype="html",
      )
    else:
      msg.set_content(
          f"""\
          New Order for {name},
            {amount}
            {invoice_no} 
          

          Address: {address}
          Phone: {phone}


          {cartItems}
          WOOOO
          """
      )
      # Add the html version.  This converts the message into a multipart/alternative
      # container, with the original text message as the first part and the new html
      # message as the second part.
      msg.add_alternative(
          f"""\
      <html>
        <body>
          <body>
            <p>New Order for {name},</p>
            <p>{amount}</p>
            <p>{invoice_no}</p>
            <p>Address: {address}</p>
            <p>Phone: {phone}</p>
            <p>{cartItems}</p>
            <p>WOOOO</p>
        </body>
      </html>
      """,
          subtype="html",
      )


    with smtplib.SMTP(EMAIL_SERVER, PORT) as server:
        server.starttls()
        server.login(sender_email, password_email)
        server.sendmail(sender_email, receiver_email, msg.as_string())