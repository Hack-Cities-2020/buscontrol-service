# Hackfellas bus control system
Dentro de la  Categoría: **Movilidad Urbana**. Escogimos resolver  el reto de [Control de puntos intermedios](http://www.hackcities.com/project/1/), ya que vimos que es importante que se  aproveche herramientas tecnológicas  sencillas a favor de una buena gestión y control del área de transporte, con esto aportamos para dar ese pequeño paso a que nos podamos convertir en una ciudad inteligente , beneficiando a todos los ciudadanos.

Este proyecto brinda un sistema integrado de control, monitoreo y gestión del recorrido de vehículos de transporte urbano con funcionalidades avanzadas de estimación de tiempos de llegada y generación de reportes para fines administrativos y de auditoria. 

El proyecto se compone de 3 partes principales:

- App Movil para el seguimiento y control de vehículos: [Repo](https://github.com/Hack-Cities-2020/mobility_project_mobile_2020)
- Servicio API REST de gestión de rutas, recorridos y vehículos (Este Repo).
- Aplicación Web de monitoreo y gestión de rutas, recorridos y vehículos: [Repo](https://github.com/Hack-Cities-2020/mobility_project_front_2020)

## Repo: buscontrol-service
Servicio para tareas de control de itinerarios y rutas de buses de transporte urbano.

> Este repositorio es el servicio web correspondiente a la aplicación web [mobility-project-front](https://github.com/Hack-Cities-2020/mobility_project_front_2020)

## Funcionalidades
Este servicio sirve como base para la aplicación web de monitoreo y administración de rutas y buses. 
Contiene lógica para crear y  gestionar rutas georeferenciadas con sus correspondientes paradas y puntos de control.

El servicio web es expuesto en forma de una **API REST** con distintos endpoints para la gestion de los recursos disponibles


### Rutas
Las rutas se componen de un conjunto de puntos georeferenciados que corresponden con el camino que uno o varios
vehículos seguirán para cumplir el servicio de transporte público. 

Este servicio web cuenta con las siguientes funcionalidades relacionadas con las rutas:

  - Creación y personalización de rutas basado en puntos georeferenciados por GPS (latitud, longitud)
  - Asignación y gestión de **paradas** correspondientes con cada ruta.
  - Asignación y gestión de **puntos de control** correspondientes con cada ruta.
  - Creación y gestión de **vehiculos y conductores** correspondientes con el servicio de transporte.
  - Generación de **reportes** con información acerca de vehículos y conductores y evaluación de rendimiento y faltas.

#### Paradas
Las paradas son puntos georeferenciados que corresponden con las paradas del vehículo de transporte público, es en estas paradas que se registra el vehiculo y la hora a la que pasó. 

#### Puntos de control
Los puntos de control son posiciones específicas dentro de la ruta que sirven para detectar el paso de los vehículos y calcular el tiempo estimado de llegada y la posición relativa en la ruta.
Estos puntos de control se implementarán como dispositivos IoT especificos para la detección del paso de los vehículos.

## Instalación
Para instalar primero clone este repositorio en algún directorio de trabajo:

```bash
git clone https://github.com/Hack-Cities-2020/buscontrol-service.git
cd buscontrol-service
```

Desde el directorio raiz del repositorio instale las dependencias en un entorno virtual de python

```bash
virtualenv env -p python3
source env/bin/activate
pip install -r requirements.txt
```

Si no cuenta con el paquete *virtualenv* lo puede instalar usando:

```bash
sudo pip install virtualenv
```

## Servidor de prueba local
Para iniciar un servidor de prueba en el localhost en el puerto 5000 ejecute el archivo run.py:

```bash
python run.py
```

El servidor correrá en la ip local en el puerto **5000**

> http://localhost:5000

```bash
Ruta base de la api: /api

Rutas: /route, /route/<route_id>

Vehiculos: /vehicle, /vehicle/<vehicle_id>

Paradas: /route/<route_id>/stops, /route/<route_id>/stops/<stop_id>

Puntos de control: /route/<route_id>/checkpoints, /route/<route_id>/checkpoints/<checkpoint_id>

Reportes: /reports
```

## Tecnologías y frameworks usados

Este proyecto está basado completamente sobre herramientas **open source** y 
con licencias privativas, de tal modo que se pueda usar, modificar y distribuir fácilmente.

Las tecnologías usadas se listan a continuación:

- Lenguaje de programación: [Python 3](https://www.python.org/)
- Framework web: [Flask](https://flask.palletsprojects.com/en/1.1.x/)
- Paquetes base: [Flask-restful](https://flask-restful.readthedocs.io/en/latest/), [sqlalchemy](https://www.sqlalchemy.org/)
- DB: [Sqlite*](https://www.sqlite.org/index.html) (el ORM es agnóstico a la DB)


## Licencia: MIT

MIT License

Copyright (c) 2020 Hack-Fellas

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
