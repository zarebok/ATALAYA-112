<html>
<body>
    <?php
    $db = pg_connect('host=192.168.1.250 dbname=jesus2020 user=jesus2020 password=jesus2020');

    $login = pg_escape_string($_POST['login']);
    $password = pg_escape_string($_POST['password']);
    $permiso = pg_escape_string($_POST['permiso']);
	if($permiso=="on") { $permiso=1;} else {$permiso=0;}
    $query = "INSERT INTO usuario(login, password, permiso) VALUES('" . $login . "', '" . $password . "', '" . $permiso . "')";
    $result = pg_query($query);
    if (!$result) {
        $errormessage = pg_last_error();
        echo "Error with query: " . $errormessage;
        exit();
    }
    printf ("Usuario %s agregado correctamente con permisos de administrador %s.<br>", $login, $permiso);
	echo ("<a href='javascript:history.back(1)'>Regresar</a>");
    pg_close();
    ?>
</body>
</html> 
