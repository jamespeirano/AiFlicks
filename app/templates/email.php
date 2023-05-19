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
            $mail->Username = 'izharali.ab@gmail.com';
            $mail->Password = 'nftxcsavtwlyzjrb';
            $mail->SMTPSecure = 'ssl';
            $mail->Port = 465;

            //Recipients
            $mail->setFrom('izharali.ab@gmail.com');
            $mail->addAddress($recipient);

            //Content
            $mail->isHTML(true);
            $mail->Subject = $subject;
            $mail->Body    = $message;

            $mail->send();
            echo 
            "
            <script>
                alert('Email sent successfully');
                window.location.href='cart.html';
            </script>
            ";
        } catch (Exception $e) {
            echo 
            "
            <script>
                alert('Email not sent. Please try again');
                window.location.href='cart.html';
            </script>
            {$mail->ErrorInfo}
            ";
        }
    } else {
        echo
        "
        <script>
            alert('Invalid email address');
            window.location.href='cart.html';
        </script>
        ";
    }
}
?>
