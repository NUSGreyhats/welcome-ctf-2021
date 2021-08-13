<?php

// just in case
if ($_SERVER['REMOTE_ADDR'] !== "127.0.0.1") {
    die("This website only serves localhost!");
}

// Define variables and initialize with empty values
$username = $password = "";
$username_err = $password_err = $login_err = "";

// Processing form data when form is submitted
if($_SERVER["REQUEST_METHOD"] == "POST") {

    // Check if username is empty
    if(empty(trim($_POST["username_VmyK7y39pX99A"]))) {
        $username_err = "Please enter username.";
    } else {
        $username = trim($_POST["username_VmyK7y39pX99A"]);
    }

    // Check if password is empty
    if(empty(trim($_POST["password_6FB8YUthKI3dK"]))) {
        $password_err = "Please enter your password.";
    } else {
        $password = trim($_POST["password_6FB8YUthKI3dK"]);
    }

    // Validate credentials
    if($username === 'admin' && $password === 'admin') {
        echo "congratulations.<br> here is what you want: greyhats{7h12_12_MOr3_7HaN_AN_55rf}";
    } else {
        $login_err = "Invalid username or password.";
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Login</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <style>
        body{ font: 14px sans-serif; }
        .wrapper{ width: 360px; padding: 20px; }
    </style>
</head>
<body>
    <div class="wrapper">
        <h2>Login</h2>
        <p>Please fill in your credentials to login.</p>

        <?php
        if(!empty($login_err)){
            echo '<div class="alert alert-danger">' . $login_err . '</div>';
        }
        ?>

        <form action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>" method="post">
            <div class="form-group">
                <label>Username</label>
                <input type="text" name="username_VmyK7y39pX99A" class="form-control <?php echo (!empty($username_err)) ? 'is-invalid' : ''; ?>" value="<?php echo $username; ?>">
                <span class="invalid-feedback"><?php echo $username_err; ?></span>
            </div>
            <div class="form-group">
                <label>Password</label>
                <input type="password" name="password_6FB8YUthKI3dK" class="form-control <?php echo (!empty($password_err)) ? 'is-invalid' : ''; ?>">
                <span class="invalid-feedback"><?php echo $password_err; ?></span>
            </div>
            <div class="form-group">
                <input type="submit" class="btn btn-primary" value="Login">
            </div>
        </form>
    </div>
</body>
</html>
