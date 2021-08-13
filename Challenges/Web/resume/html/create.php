<?php

$required = array('fullname', 'linkedin', 'email', 'phonenumber', 'jobposition', 'jobdescription','projectname','projectdescription','universityname','universitydescription');

foreach($required as $field) {
    if (empty($_POST[$field])) {
        die("$field is empty!");
    }
}

$template = file_get_contents("resume.html");

foreach($required as $field) {
    $template=str_replace(strtoupper($field),$_POST[$field],$template);
}

function generateRandomString($length = 20) {
    $characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
    $charactersLength = strlen($characters);
    $randomString = '';
    for ($i = 0; $i < $length; $i++) {
        $randomString .= $characters[rand(0, $charactersLength - 1)];
    }
    return $randomString;
}

$output = generateRandomString();

file_put_contents("${output}.html",$template);

system("wkhtmltopdf --javascript-delay 200 --debug-javascript ${output}.html tmp/${output}.pdf");

@unlink("${output}.html");

echo $template;
echo "<a href='tmp/${output}.pdf'>download</a>";
