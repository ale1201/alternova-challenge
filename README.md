# Alternova-challenge
Este repositorio fue creado con el fin de responder a los requerimientos de la prueba técnica presentada por la empresa Alternova. 

## Correr el repositorio localmente
El repositorio se puede correr en la maquina local, este ya cuenta con su propia DB poblada para hacer casos de prueba.

Para correr el repositorio localmente, primero se debe clonar el repositorio. Una vez clonado el repositorio, se abre y haciendo uso de cmd se escibe el comando `pip install requirements.txt` para instalar las librerias necesarias para el funcionamiento de la aplicación.

Seguido a eso, ejecutar el comando `python manage.py makemigrations` y luego `python manage.py migrate` para asegurar que las migraciones se corran y estén actualizadas. 

Para lanzar el servidor, se usa el comando `python manage.py runserver`. Al ejecutar el comando, la aplicación empezará a correr bajo la url: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
### Tests
La aplicación cuenta con tests que prueban las funcionalidades de los diferentes endpoints creados. Estos tests se pueden correr teniendo el repositorio clonado localmente y siguiendo los pasos proporcionados para el despliegue. Sin embargo, en este caso para correr los tests se hace uso del comando `python manage.py test`, lo que ejecuta 24 tests creados para probar los endpoints.

## Aplicación alojada en hosting
Adicional al repositorio, la aplicación se encuentra alojada en el hosting de pythonanywhere, bajo el link: [https://ale1220.pythonanywhere.com/](https://ale1220.pythonanywhere.com/). La aplicación cuenta con su probia DB con datos previamente cargados para hacer pruebas y poder manpular los endpoints con esos datos.

## Especificaciones de la aplicación

La aplicación cuenta con la documentación de los endpoints. Para acceder a esta, sería bajo la url '/docs', por ejemplo [https://ale1220.pythonanywhere.com/docs/](https://ale1220.pythonanywhere.com/docs/). Esta documentación fue generada con Swagger y desde acá también se pueden probar endpoints (por ejemplo endpoints con peticiones diferentes a /GET/).

La aplicación cuenta con Autenticacion y hay endpoints que requieren de esta para su funcionamiento. Se manejaron 2 tipos de autenticacion: Basic authentication (para poder hacer pruebas desde swagger, esta es con inicio de sesión básico) y Token authentication (para hacer pruebas con postman mandando el token de sesión en los headers de las peticiones)

### Endpoints
* GET /api/movies/filter: Este endpoint filtra las películas por nombre, tipo y genero (para el caso del nombre, se buscan peliculas que en el nombre contengan la palabra mandada). Para su funcionamiento se debe pasar por query params los filtros que se desean aplicar, por ejemplo: 'https://ale1220.pythonanywhere.com/api/movies/filter?genre=comedia' o 'https://ale1220.pythonanywhere.com/api/movies/filter?name=t&type=serie', el primero filtra por género y el segundo filtra por nombre de la película y tipo. Este endpoint responde al tercer requerimiento solicitado en la prueba.
* POST /api/movies/login: Este endpoint permite a un usuario iniciar sesión y retorna el Token de sesión de dicho usuario. Este endpoint fue creado principalmente para pruebas en postman, para poder obtener el token de inicio de sesión de un usuario y poderlo mandar en los headers para otros endpoints que requieren autenticación. Este requiere que se mande un cuerpo en la petición con el username y password correspondientes a un usuario que previamente ya fue registrado en la base de datos.
* POST /api/movies/logout: Este endpoint permite a un usuario cerrar sesión, eliminandoo el token de dicho usuario. Este endpoint fue creado principalmente para pruebas en postman, para poder eliminar el token de inicio de sesión de un usuario y eliminar la autenticacion para ese usuario, a menos que vuelva a iniciar sesión. Para su uso, se requiere que el usuario este autenticado.
* GET /api/movies/random: Este endpoint retorna una película aleatoriamente que se encuentre en la base de datos, mostrando todos los datos asociados a la película. Este endpoint NO requiere autenticación para su funcionamiento al ser informativo. Para su uso, basta con usar la url 'https://ale1220.pythonanywhere.com/api/movies/random'.
* 
