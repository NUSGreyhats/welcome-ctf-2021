<html>

<head>
	<title>Ketchup</title>
</head>

<body>
  <!-- Version 2.2.3. Backup file contains version 2.2.2. -->

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
        echo '<h3>greyhats{n0_k3tchup_r4w_s4uc3_892e89h89e}</h3>';
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