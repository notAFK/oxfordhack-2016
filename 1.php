<?php
	if ( isset($_POST['submit']) && $_POST['submit'] == "" ) {
		  // do nothing
	} else {
		  $myfile = fopen("/home/mistedoom/oxfordhack-2016/input1.txt", "w");
		  $txt = $_POST['lyric'];
		  fwrite($myfile, $txt);
		  fclose($myfile);
		  $process = exec("python /home/mistedoom/oxfordhack-2016/makeuplink.py", $out);
			$message = "Output: " . $out;
	}
}
catch (Exception $ex) {
	$error = "Error: " . $ex->getMessage();
}
?>

<!DOCTYPE html>
<html>
<head>
	<title>AutoDJ</title>
	
	<meta name="viewport" content="width=device-width, initial-scale=1">
	
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">

</head>
<body>
  <header>
		<nav class="navbar navbar-default">
			<div class="container-fluid">
				<div class="navbar-header">
				  <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false">
				    <span class="sr-only">Toggle navigation</span>
				    <span class="icon-bar"></span>
				    <span class="icon-bar"></span>
				    <span class="icon-bar"></span>
				  </button>
				  <a class="navbar-brand" href="#">AutoDJ</a>
				</div>
				<div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
				  <ul class="nav navbar-nav">
				    <li class="active"><a href="#">Link <span class="sr-only">(current)</span></a></li>
				    <li><a href="#">Link</a></li>
					</ul>
				</div>
			</div>
		</nav>
  </header>
	<div class="container main-content">
		<div class="panel panel-default">
			<div class="panel-heading">Get a nice song for ur lyrics</div>
			<div class="panel-body">
				<?=isset($error)?'<span style="color:red">'.$error.'</span>':''?>
				<?=isset($message)?'<span style="color:green">'.$message.'</span>':''?>
				<form action='' method='post'>
					<div class="form-group">
			  		<label for="lyricss">Lyrics: </label>
						<textarea id="lyricss" rows='5' class='form-control' name='lyric'></textarea>
					</div>	
					<input class="btn btn-primary" type='submit' name='submit' value='Submit'>
					
			 	</form>
			</div>
		</div>
	</div>
	<script
			  src="https://code.jquery.com/jquery-1.12.4.min.js"
			  integrity="sha256-ZosEbRLbNQzLpnKIkEdrPv7lOy9C27hHQ+Xp8a4MxAQ="
			  crossorigin="anonymous"></script>
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
</body>
</html>
