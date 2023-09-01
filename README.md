# Alternova-challenge
Este repositorio fue creado con el fin de responder a los requerimientos de la prueba técnica presentada por la empresa Alternova. 

## Correr el repositorio localmente
El repositorio se puede correr en la maquina local, este ya cuenta con su propia DB poblada para hacer casos de prueba.

Para correr el repositorio localmente, primero se debe clonar el repositorio. Una vez clonado el repositorio, se abre y haciendo uso de cmd se escibe el comando `pip install requirements.txt` para instalar las librerias necesarias para el funcionamiento de la aplicación.

Seguido a eso, ejecutar el comando `python manage.py makemigrations` y luego `python manage.py migrate` para asegurar que las migraciones se corran y estén actualizadas. 

Para lanzar el servidor, se usa el comando `python manage.py runserver`. Al ejecutar el comando, la aplicación empezará a correr bajo la url: [](http://127.0.0.1:8000/)
### Tests
La aplicación cuenta con tests que prueban las funcionalidades de los diferentes endpoints creados. Estos tests se pueden correr teniendo el repositorio clonado localmente y siguiendo los pasos proporcionados para el despliegue. Sin embargo, en este caso para correr los tests se hace uso del comando `python manage.py test`, lo que ejecuta 24 tests creados para probar los endpoints.

## Aplicación alojada en hosting
Adicional al repositorio, la aplicación se encuentra alojada en el hosting de pythonanywhere, bajo el link: [](https://ale1220.pythonanywhere.com/).
