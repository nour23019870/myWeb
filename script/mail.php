<?php

/*
    The Send Mail PHP Script for Contact Form
    Server-side data validation is also added for good data validation.
*/

$data = ['error' => false];

$name = $_POST['name'] ?? '';
$email = $_POST['email'] ?? '';
$phone = $_POST['phone'] ?? '';
$website = $_POST['website'] ?? '';
$message = $_POST['message'] ?? '';

// Validate the inputs
if (empty($name)) {
    $data['error'] = 'Please enter your name.';
} elseif (filter_var($email, FILTER_VALIDATE_EMAIL) === false) {
    $data['error'] = 'Please enter a valid email address.';
} elseif (empty($phone)) {
    $data['error'] = 'Please enter your phone number.';
} elseif (empty($message)) {
    $data['error'] = 'The message field is required!';
} else {
    // Set default value for website if empty
    if (empty($website)) {
        $website = 'none';
    }

    $formcontent = "From: $name\nPhone: $phone\nWebsite: $website\nEmail: $email\nMessage: $message";
    
    // Place your email here
    $recipient = "nourmanagment@gmail.com";
    
    $mailheader = "From: $email \r\n";
    
    if (mail($recipient, "New contact form submission", $formcontent, $mailheader) === false) {
        $data['error'] = 'Sorry, an error occurred!';
    } else {
        $data['error'] = false;
    }
}

echo json_encode($data);

?>
