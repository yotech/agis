<?php

/* script for updating the field 'nestudante' of the
 * estudantes table 
 *
 *
 * @author: Yoel Benítez Fonseca <ybenitezf@gmail.com>
 * @version: 0.1
 */
 
defined('SERVIDOR') or define('SERVIDOR','localhost');
defined('UTILIZADOR') or define('UTILIZADOR','root');
defined('SENHA') or define('SENHA','secret');
defined('BASE_DADOS') or define('BASE_DADOS','mydb');

try{
    $db = new PDO(
        'mysql:host='.SERVIDOR.';dbname='.BASE_DADOS, 
        UTILIZADOR, SENHA, 
        array(PDO::ATTR_PERSISTENT => true)
    );
    $stmt = $db->prepare(
        "UPDATE estudantes SET nestudante = :value 
            WHERE estudantes.idtabestudante = :id;"
    );
    $res = $db->query("SELECT * FROM estudantes");
    $res = $res->fetchAll();
    foreach ($res as $st) {
        // Get the data for the nestudante.
        /*  se compone por 2 num (codigo de la escuela), luego 3 num (codigo 
         *  del curso), 2 num (ano en q matriculo la primera ves), 1 num (sexo) 
         *  y 4 numeros consecuticos
         * */
        $sql = "SELECT UO.codigouo FROM 
                       unidade_organicas UO, uo_cursos C, uo_departamentos D, 
                       estudantes E 
                       WHERE E.idcurso = C.idcurso AND 
                       C.iddepartamento = D.iddepartamento AND 
                       D.iduo = UO.idunidadeorganica AND 
                       E.idtabestudante = '" . $st["idtabestudante"] ."'";
        $r = $db->query($sql);
        $r = $r->fetchAll();
        $codigo_uo = $r[0]["codigouo"];
        $sql = "SELECT SUBSTRING(C.codigocurso, 3) as cid, C.duracaoano FROM 
                       uo_cursos C, estudantes E 
                       WHERE E.idcurso = C.idcurso AND
                       E.idtabestudante = '" . $st["idtabestudante"] ."'";
        $r = $db->query($sql);
        $r = $r->fetchAll();
        $codigo_curso = $r[0]['cid'];
        $curso_duracion = (int)$r[0]['duracaoano'];
        $sql = "SELECT P.codigosexo FROM 
                       pessoas P, estudantes E 
                       WHERE P.idpessoa=E.idestudante AND
                       E.idtabestudante = '" . $st["idtabestudante"] ."'";
        $r = $db->query($sql);
        $r = $r->fetchAll();
        $codigo_sexo = $r[0]['codigosexo'];
        $nivel = (int)$st["idnivel"];
        $year = (int)date("Y");
        $entry_year = (string)($year - $nivel);
        $entry_year = substr($entry_year, -2);
        $consec = substr($st["idtabestudante"], -4);
        $ID = $codigo_uo . $codigo_curso . $entry_year . $codigo_sexo . $consec;
        $stmt->bindParam(':value', $ID);
        $stmt->bindParam(':id', $st["idtabestudante"]);
        $stmt->execute();
    }
}catch(PDOException $e){
    echo $e->getMessage();
    die();
}

$db = null;
//select concat(U.codigouo, SUBSTRING(C.codigocu­rso, 3, 5), (2017-E.idnivel), P.codigosexo, substring(E.idtabEst­udante,6,10)) from unidade_organicas U, estudantes E, uo_cursos C, pessoas P where P.idpessoa=E.idestud­ante and E.idcurso=C.idcurso
