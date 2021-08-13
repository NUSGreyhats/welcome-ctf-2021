<?php
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}
?>
<?php
if (!isset($_SESSION['init'])) {
    $_SESSION['init']=1;

    function generateRandomString($length = 20) {
        $characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
        $charactersLength = strlen($characters);
        $randomString = '';
        for ($i = 0; $i < $length; $i++) {
            $randomString .= $characters[rand(0, $charactersLength - 1)];
        }
        return $randomString;
    }

    for ($i = 0; $i < 100; ++$i) {
        $_SESSION[generateRandomString(7)] = generateRandomString(17);

    }
}
//var_dump($_SESSION);

$flag = True;

foreach ($_SESSION as $key => $value) {
    if (isset($_POST[$key]) && $_POST[$key] == $value) {
        continue;
    } else {
        $flag = False;
        break;
    }
}

if ($flag) {
    echo "greyhats{5U8m1551O5_15_FRoM_tH3_CL13Nt_51d3}";
}

?>

<html lang="en">
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
        <meta name="description" content="" />
        <meta name="author" content="" />
        <title>No Submission, Yes Security</title>
        <!-- Favicon-->
        <link rel="icon" type="image/x-icon" href="https://startbootstrap.github.io/startbootstrap-the-big-picture/assets/favicon.ico" />
        <!-- Core theme CSS (includes Bootstrap)-->
        <link href="https://startbootstrap.github.io/startbootstrap-the-big-picture/css/styles.css" rel="stylesheet" />
    </head>
    <body>
        <!-- Navigation-->
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-bottom">
            <div class="container px-4 px-lg-5">
                <a class="navbar-brand" href="#!">No Flag</a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation"><span class="navbar-toggler-icon"></span></button>
                <div class="collapse navbar-collapse" id="navbarResponsive">
                    <ul class="navbar-nav ml-auto">
                        <li class="nav-item active"><a class="nav-link" href="#!">Home</a></li>
                        <li class="nav-item"><a class="nav-link" href="#!">About</a></li>
                        <li class="nav-item"><a class="nav-link" href="#!">Services</a></li>
                        <li class="nav-item"><a class="nav-link" href="#!">Contact</a></li>
                    </ul>
                </div>
            </div>
        </nav>
        <!-- Page Content-->
        <section>
            <div class="container px-4 px-lg-5">
                <div class="row gx-4 gx-lg-5">
                    <div class="col-lg-6">
                        <h1 class="mt-5">No Submit Security</h1>
                        <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Deserunt voluptates rerum eveniet sapiente repellat esse, doloremque quod recusandae deleniti nostrum assumenda vel beatae sed aut modi nesciunt porro quisquam voluptatem. Et non intellegunt ad hoc caput, quia non facit sensu ad me quid aut</p>
                    </div>
                </div>
            </div>
        </section>
        <!-- Bootstrap core JS-->
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js"></script>
        <!-- Core theme JS-->
        <script src="https://startbootstrap.github.io/startbootstrap-the-big-picture/js/scripts.js"></script>
        <form id='1' method="POST" action="./index.php">
<?php
foreach ($_SESSION as $key => $value) {
    echo str_repeat(" ",12)."<input type='hidden' name='$key' value='$value'>\n";
}
?>
        </form>
    </body>
</html>


<html>
<head>
</head>
<body>
</form>
</body>
</html>
