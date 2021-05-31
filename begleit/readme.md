# Setup gradle
gradlew.bat ausführen

# Initialisieren

-PnewDocDir=<absolute_path_to_root_dir_where_documentation_is_located> ... e.g E:\Studium\MASTER\SS2021\Softwareintensive_Systeme_in_der_Mobilität\repository\sisidm_2021\begleit

gradlew -b init.gradle initArc42DE -PnewDocDir=E:\Studium\MASTER\SS2021\Softwareintensive_Systeme_in_der_Mobilität\repository\sisidm_2021\begleit


# HTML generieren
doctoolchain.bat E:\Studium\MASTER\SS2021\Softwareintensive_Systeme_in_der_Mobilität\repository\sisidm_2021\begleit generateHTML

# PDF generieren
doctoolchain.bat E:\Studium\MASTER\SS2021\Softwareintensive_Systeme_in_der_Mobilität\repository\sisidm_2021\begleit generatePDF


# CI