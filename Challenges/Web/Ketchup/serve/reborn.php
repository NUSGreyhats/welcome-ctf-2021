<html>

<head>
	<title>Ketchup</title>
</head>

<body>
  <!-- I like to use Vim because it always creates a backup for me, in case I forgot to save my work and my computer crashes. --->

	<?php if ($_SERVER['REQUEST_METHOD'] === 'GET') : ?>
		<form action="<?php htmlspecialchars($_SERVER['PHP_SELF']) ?>" method="post">
      <h2>Security Question</h2>
			<div class="form-field">
				<label for="name">What is my favorite ketchup?</label>
				<input type="text" name="ketchup" required="required" placeholder="Enter the answer" />
			</div>

			<div class="form-field">
				<input type="submit" value="Submit" />
			</div>
		</form>
	<?php else : ?>
		<?php
		if (isset($_POST['ketchup'])) {
			$ketchup = htmlspecialchars($_POST['ketchup']);

      if (strcmp($ketchup, 'no ketchup, raw sauce -- too many calories, not good') == 0) {
        echo '<h1>Well, site is still under construction</h1>';
        include "flag.php";
        echo $flag;
      } else {
        echo 'Wrong answer. Go away.';
      }
		} else {
			echo 'You forgot to give an answer. Go back.';
		}
		?>
	<?php endif ?>
</body>

</html>
