<?php

use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;
use PHPMailer\PHPMailer\SMTP;

require 'src/Exception.php';
require 'src/PHPMailer.php';
require 'src/SMTP.php';

if ($_SERVER['REQUEST_METHOD'] == 'POST') {

    $recipient = filter_var($_POST['card_holder_email'], FILTER_SANITIZE_EMAIL);
    $subject = 'Payment Confirmation';
    $message = "Thank you for your payment!<br><br>";

    if (filter_var($recipient, FILTER_VALIDATE_EMAIL)) {
        $mail = new PHPMailer(true);

        try {
            // Server settings
            $mail->SMTPDebug = SMTP::DEBUG_SERVER;
            $mail->isSMTP();
            $mail->Host = 'smtp.gmail.com';
            $mail->SMTPAuth = true;
            $mail->Username = 'izharali.ab@gmail.com'; // Replace with your email address
            $mail->Password = 'nftxcsavtwlyzjrb'; // Replace with your email password or app password
            $mail->SMTPSecure = 'tls'; // Use 'tls' instead of 'ssl' for Gmail
            $mail->Port = 587; // Use 587 for 'tls' or 465 for 'ssl'

            // Recipients
            $mail->setFrom('izharali.ab@gmail.com'); // Replace with your email address
            $mail->addAddress($recipient);

            // Content
            $mail->isHTML(true);
            $mail->Subject = $subject;
            $mail->Body = $message;

            $mail->send();
            echo "
            <script>
                alert('Email sent successfully');
                window.location.href='cart.html';
            </script>
            ";
        } catch (Exception $e) {
            echo "
            <script>
                alert('Email not sent. Please try again');
                window.location.href='cart.html';
            </script>
            ";
        }
    } else {
        echo "
        <script>
            alert('Invalid email address');
            window.location.href='cart.html';
        </script>
        ";
    }
}
?>
