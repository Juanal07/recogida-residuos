<p align="center">

<img src="https://raw.githubusercontent.com/Juanal07/recogida-residuos/main/front/img/cleanos.png?token=GHSAT0AAAAAABKWIXK55FROERACWJSBX7BGYSSSPSA"  />

</p>

## Descripción

Este prototipo forma parte de la propuesta que hace Sudo Team al Departamento de Limpieza de Anthelm.

La solución propuesta pretende mejorar el sistema de recogida de basuras actual,
consiguiendo ahorrar combustibles fósiles u otra fuente de energía que use, y optimizar las rutas de recogida de residuos urbanos,
disminuyendo los recorridos de los camiones y tiempo de recogida y todo con una interfaz usable para los conductores.

<p align="center">
<img src="https://raw.githubusercontent.com/Juanal07/recogida-residuos/main/front/img/rutas.png?token=GHSAT0AAAAAABKWIXK5OKROQG7MYHT4CPF2YSSTPMA" width="500" />
</p>

## Miembros del equipo Sudo Team

- **Francisco Afán Rodríguez**
- **Pablo Pascual García**
- **Juan Alberto Raya Rodríguez**

[<img src="https://avatars.githubusercontent.com/u/45666661?v=4" width="100px;"/><sub><b></b></sub>](https://github.com/N3oZ3r0)&nbsp;&nbsp;&nbsp;&nbsp;
[<img src="https://avatars.githubusercontent.com/u/59370966?v=4" width="100px;"/><sub><b></b></sub>](https://github.com/pablopascu99)&nbsp;&nbsp;&nbsp;&nbsp;
[<img src="https://avatars.githubusercontent.com/u/22559891?v=4" width="100px;"/><sub><b></b></sub>](https://github.com/juanal07)&nbsp;&nbsp;&nbsp;&nbsp;

## Instrucciones

### Visualizar rutas

1. Para evitar errores de CORS simulamos un servidor web

> `python -m http.server`

2. Abrir en el navegador

> `localhost:8000/front/map.html`

### Algoritmo optimización

1. Necesario python 3.9 y pip

2. Recomendable instalar herramienta virtualenv

> `pip install virtualenv`

3. Crear virtual enviroment

> `virtualenv venv`

4. Acceder al virtual enviroment (Unix)

> `source venv/bin/activate`

5. Acceder al virtual enviroment (Windows)

> `.\venv\Scripts\activate`

6. Instalar dependencias

> `pip install -r requirements.txt`

7. Modificar drivers.json o locations.json para variar su ubicación o carga simulando
   los datos de los sensores. De esta forma al ejecutar
   el programa se recalcularan las rutas y se podrá ver refrescando la web.

> `python main.py`
