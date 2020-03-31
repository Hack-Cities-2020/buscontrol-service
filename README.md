# Hackfellas bus control system


## Repo: buscontrol-service
Servicio para tareas de control de itinerarios y rutas de buses de transporte urbano.

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

- Lenguaje de programación: Python 3
- Framework web: Flask
- Paquetes base: Flask-restful, sqlalchemy
- DB: Sqlite* (el ORM es agnóstico a la DB)

