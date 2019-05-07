<?php
    $dbconnect = mysqli_connect("localhost", "special_user", "root", "DefinitelyNotARubiks");
    if(mysqli_connect_errno()) {
        echo "Connection failed:".mysqli_connect_errno();
        exit;
    }

?>
