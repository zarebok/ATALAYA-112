<?php

//AQUI CONECTAMOS A LA BASE DE DATOS DE POSTGRES
$conex = "host=192.168.1.250 port=5432 dbname=jesus2020 user=jesus2020 password=jesus2020";
$cnx = pg_connect($conex) or die ("<h1>Error de conexion.</h1> ". pg_last_error());
session_start();

function quitar($mensaje)
{
 $nopermitidos = array("'",'\\','<','>',"\"");
 $mensaje = str_replace($nopermitidos, "", $mensaje);
 return $mensaje;
}
if(trim($_POST["usuario"]) != "" && trim($_POST["password"]) != "")
{
 // Puedes utilizar la funcion para eliminar algun caracter en especifico
 //$usuario = strtolower(quitar($HTTP_POST_VARS["usuario"]));
 //$password = $HTTP_POST_VARS["password"];
 // o puedes convertir los a su entidad HTML aplicable con htmlentities
 $usuario = strtolower(htmlentities($_POST["usuario"], ENT_QUOTES));
 $password = $_POST["password"];
 $result = pg_query('select password, login, permiso from usuario where password=\''.$password.'\'');
 if($row = pg_fetch_array($result)){
  if($row["login"] == $usuario){
   $_SESSION["k_username"] = $row['login'];
   $_SESSION["k_permiso"] = $row['permiso'];
   echo 'Has sido logueado correctamente '.$_SESSION['k_username'].' <p>';
   session_start();
   //echo '<a href="index.php">Index</a></p>';
   //Elimina el siguiente comentario si quieres que re-dirigir automáticamente a index.php
   //Ingreso exitoso, ahora sera dirigido a la pagina principal.
   ?><SCRIPT LANGUAGE="javascript">
   location.href = "console.php";
   </SCRIPT><?PHP
  }else{
   echo 'Usuario incorrecto';
  }
 }else{
  echo 'Usuario no existente en la base de datos o password incorrecto';
 }
 pg_free_result($result);
}else{
 echo 'Debe especificar un usuario y password';
}
pg_close();
?>
