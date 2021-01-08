<?php
session_start();

?>
<html lang="en">
<head>
	<title>ATALAYA-112: Gestion de usuarios</title>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
<!--===============================================================================================-->	
	<link rel="icon" type="image/png" href="images/icons/favicon.ico"/>
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="vendor/bootstrap/css/bootstrap.min.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="fonts/font-awesome-4.7.0/css/font-awesome.min.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="fonts/iconic/css/material-design-iconic-font.min.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="vendor/animate/animate.css">
<!--===============================================================================================-->	
	<link rel="stylesheet" type="text/css" href="vendor/css-hamburgers/hamburgers.min.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="vendor/animsition/css/animsition.min.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="vendor/select2/select2.min.css">
<!--===============================================================================================-->	
	<link rel="stylesheet" type="text/css" href="vendor/daterangepicker/daterangepicker.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="css/util.css">
	<link rel="stylesheet" type="text/css" href="css/main.css">
<!--===============================================================================================-->
</head>
<body>

	
	<div class="limiter">
		<div class="container-login100" style="background-image: url('images/bg-01.jpg');">
			<div class="wrap-login100">
				<form action="add.php" class="login100-form validate-form" method='post' accept-charset='UTF-8'>
					<span class="login100-form-logo">
						<img src="img/icono.png" alt="112" width="150" height="150">
					</span>

					<span class="login100-form-title p-b-34 p-t-27">
						Permite el acceso a la Atalaya-112
					</span>
					<div class="wrap-input100 validate-input" data-validate = "Introduce nombre de usuario">
						<input class="input100" type="text" name="login" placeholder="Usuario">
						<span class="focus-input100" data-placeholder="&#xf207;"></span>
					</div>

					<div class="wrap-input100 validate-input" data-validate="Introduce password">
						<input class="input100" type="password" name="password" placeholder="Password">
						<span class="focus-input100" data-placeholder="&#xf191;"></span>
					</div>
					
					<div class="wrap-input100 validate-input">
						<input type="checkbox" name="permiso">
							Con permiso de administrador
						</input>
					</div>

					<div class="container-login100-form-btn">
						<button class="login100-form-btn">
							Añadir
						</button>
					</div><br><br>
				</form>
				<span class="login100-form-title p-b-34 p-t-27">
						Elimina el acceso a la Atalaya-112
					</span>
				<table class="table">
				  <thead>
					<tr>
					  <th scope="col">#</th>
					  <th scope="col">Usuario</th>
					  <th scope="col">Administrador</th>
					  <th scope="col">Eliminar</th>
					</tr>
				  </thead>
				  <tbody>
					<?php
					$db = pg_connect('host=192.168.1.250 dbname=jesus2020 user=jesus2020 password=jesus2020');

					$query = "SELECT * FROM usuario";
					$result = pg_query($query);
					if (!$result) {
						$errormessage = pg_last_error();
						echo "Error with query: " . $errormessage;
						exit();
					}
					$x=1;
					while ($fila = pg_fetch_row($result)) {
						print("<form action='delete.php' class='login100-form validate-form' method='post' accept-charset='UTF-8'><tr>");	
						print("<td>".$x."</td>");
						print("<input id='login' name='login' type='hidden' value='".$fila[0]."'><td>".$fila[0]."</td>");
						if($fila[2]=="1") {print("<td>Si</td>");} else {print("<td>No</td>");} 
						print('<td><button type="submit" class="btn btn-danger">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
  <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"></path>
  <path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4L4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"></path>
</svg>
                
              </button></td>');
						print("</tr></form>");
						$x=$x+1;
					}	
					pg_close();
					?>				  

					
				  </tbody>
				</table>				
				
			</div>
		</div>
	</div>
	

	<div id="dropDownSelect1"></div>
	
<!--===============================================================================================-->
	<script src="vendor/jquery/jquery-3.2.1.min.js"></script>
<!--===============================================================================================-->
	<script src="vendor/animsition/js/animsition.min.js"></script>
<!--===============================================================================================-->
	<script src="vendor/bootstrap/js/popper.js"></script>
	<script src="vendor/bootstrap/js/bootstrap.min.js"></script>
<!--===============================================================================================-->
	<script src="vendor/select2/select2.min.js"></script>
<!--===============================================================================================-->
	<script src="vendor/daterangepicker/moment.min.js"></script>
	<script src="vendor/daterangepicker/daterangepicker.js"></script>
<!--===============================================================================================-->
	<script src="vendor/countdowntime/countdowntime.js"></script>
<!--===============================================================================================-->
	<script src="js/main.js"></script>

</body>
</html>