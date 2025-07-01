# Restaurante

Este es un proyecto desarrollado en la materia " Laboratorio de programacion y lenguaje ", donde se desarrollo una gestion integral de un restaurante.

Este sistema permite la administracion de pedidos, productos, reservas, notificaciones y usuarios, teniendo en consideracion los roles de clientes y staff ( administrador y cajero )

La estructura del proyecto es el siguiente: 
<li> menu app : gestion del menu, productos y categorias</li>
<li> orders : logica de pedidos, items de pedido y carrito </li>
<li> bookings : reservas de mesas y horarios </li>
<li> notifications: notificaciones para usuarios y staff </li>
<li> admin_custom: panel de administracion personalizado para staff </li>
<li> templates: plantillas HTML, para front y backend</li>

---

# Grupo 6, Integrantes

Aguila Tayra
Alvarado Micaela
Criniti Teresa
Frers Pamela
Sarmiento Ximena

---

## Aplicar entorno virtual
python -m venv env

## Activar entorno virtual
- Linux/Mac: source env/bin/activate
- Windows: source env/Scripts/activate
- Windows (alternativa): ./env/Scripts.activate
en VSC
.\env\Scripts\activate

## Instalar dependencias
pip install -r requirements

## Hacer migraciones
python manage.py migrate

## Llenar base de datos con fixture
python manage.py loaddata events.json

## Correr app
python manage.py runserver
