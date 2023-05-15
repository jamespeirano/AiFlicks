<?php

use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;
use PHPMailer\PHPMailer\SMTP;

require 'path/to/PHPMailer/src/Exception.php';
require 'path/to/PHPMailer/src/PHPMailer.php';
require 'path/to/PHPMailer/src/SMTP.php';

if ($_SERVER['REQUEST_METHOD'] == 'POST') {

    $recipient = filter_var($_POST['card_holder_email'], FILTER_SANITIZE_EMAIL);
    $subject = 'Payment Confirmation';
    $message = "Thank you for your payment!\n\n";
    $message .= "Full Name: " . filter_var($_POST['card_holder_name'], FILTER_SANITIZE_STRING) . "\n";
    $message .= "Address: " . filter_var($_POST['card_holder_address'], FILTER_SANITIZE_STRING) . "\n";

    if (filter_var($recipient, FILTER_VALIDATE_EMAIL)) {
        $mail = new PHPMailer(true);

        try {
            //Server settings
            $mail->SMTPDebug = SMTP::DEBUG_SERVER;
            $mail->isSMTP();
            $mail->Host = 'smtp.gmail.com';
            $mail->SMTPAuth = true;
            $mail->Username = 'sender@gmail.com';
            $mail->Password = '!';
            $mail->SMTPSecure = PHPMailer::ENCRYPTION_STARTTLS;
            $mail->Port = 587;

            //Recipients
            $mail->setFrom('sender@gmail.com', '');
            $mail->addAddress($recipient);

            //Content
            $mail->isHTML(false);
            $mail->Subject = $subject;
            $mail->Body    = $message;

            $mail->send();
            echo 'Email sent!';
        } catch (Exception $e) {
            echo "Error sending email: {$mail->ErrorInfo}";
        }
    } else {
        echo 'Invalid email address.';
    }
}
?>
