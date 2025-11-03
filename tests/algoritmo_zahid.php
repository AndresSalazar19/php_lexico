<?php
//Variables normales
$nombre = "Zahid";
$edad = 25;
$activo = true;
$precio = 100.50;

//Variables de instancia
class Producto {
    private $nombre;
    private $precio;
    
    public function __construct($n, $p) {
        $this->nombre = $n;
        $this->precio = $p;
    }
    
    public function actualizar($n) {
        $this->nombre = $n;
    }
}

//Operadores de asignación compuesta
$total = 100;
$total += 50;        //PLUS_ASSIGN
$total -= 20;        //MINUS_ASSIGN
$total *= 2;         //TIMES_ASSIGN
$total /= 4;         //DIVIDE_ASSIGN

$mensaje = "Hola";
$mensaje .= " Mundo"; //CONCAT_ASSIGN

//Operador de objeto
$producto = new Producto("Laptop", 1200);
$producto->actualizar("PC");

//Herencia y punteros
interface Vendible {
    public function vender();
}

abstract class Item {
    abstract public function obtener();
}

class Articulo extends Item implements Vendible {
    public function vender() {
        return true;
    }
    
    public function obtener() {
        return "Articulo";
    }
}

//Modificadores
final class Config {
    const VERSION = "1.0";
}

//Trait - Use
trait Logger {
    public function log($msg) {
        echo $msg;
    }
}

class Usuario {
    use Logger;
}

//Namespace
namespace App\Models;

use App\Utils\Helper as H;

//Uso de instanceof
$art = new Articulo();
if ($art instanceof Vendible) {
    $art->vender();
}

//Excepciones
try {
    if ($total < 0) {
        throw new Exception("Error");
    }
} catch (Exception $e) {
    echo $e;
} finally {
    $total = 0;
}

//Modularidad
require 'config.php';
include 'helpers.php';
require_once 'database.php';
include_once 'functions.php';

?>