#!/usr/bin/perl

$repeticiones = 30;
@ejecutables = ("heat_main.py");
@versiones = ("py","cyt");
$path = "/home/diego/TercerParcial-Paralela/";

foreach $exe (@ejecutables) {
    foreach $version (@versiones){
        $fichero = "$path"."Soluciones/"."heat_main"."-"."$version";
        print("$path$exe $version \n");
        for($i = 0; $i<$repeticiones; $i++){
            system("python3 $path$exe -v $version >> $fichero")
        }
    }
}

exit(1);