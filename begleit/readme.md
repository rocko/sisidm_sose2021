[![runOnGitHub](https://github.com/rocko/sisidm_sose2021/actions/workflows/runOnGitHub.yml/badge.svg)](https://github.com/rocko/sisidm_sose2021/actions/workflows/runOnGitHub.yml)

# Handbuch (offiziell)
https://doctoolchain.github.io/docToolchain/

# doctoolchain klonen
git clone --recursive https://github.com/docToolchain/docToolchain.git <Zielverzeichnis>

# ins doctoolchain Zielverzeichnis wechseln

## Setup gradle
Ausführen: gradlew.bat

## gradle.properties
Ändern: inputPath = ./src

## Initialisieren des ARC42 Templates

-PnewDocDir=<absolute_path_to_root_dir_where_documentation_is_located> ... e.g E:\Studium\MASTER\SS2021\Softwareintensive_Systeme_in_der_Mobilität\repository\sisidm_2021\begleit

gradlew -b init.gradle initArc42DE -PnewDocDir=E:\Studium\MASTER\SS2021\Softwareintensive_Systeme_in_der_Mobilität\repository\sisidm_2021\begleit

# Ausgaben

## HTML generieren
doctoolchain.bat E:\Studium\MASTER\SS2021\Softwareintensive_Systeme_in_der_Mobilität\repository\sisidm_2021\begleit generateHTML

## PDF generieren
doctoolchain.bat E:\Studium\MASTER\SS2021\Softwareintensive_Systeme_in_der_Mobilität\repository\sisidm_2021\begleit generatePDF


# CI




