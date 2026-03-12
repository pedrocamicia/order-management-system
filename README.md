# Order Management System

Backend de gestión de pedidos desarrollado con FastAPI y PostgreSQL, 
siguiendo una arquitectura en capas inspirada en Domain-Driven Design (DDD).

Incluye autenticación con JWT, control de acceso por roles, 
reglas de negocio sobre pedidos y validación de stock.

El sistema permite:

- Registrar usuarios y autenticarlos con JWT
- Crear y consultar pedidos
- Agregar, modificar y eliminar items de un pedido
- Confirmar pedidos con validacion de stock
- Consultar clientes y productos con paginacion y filtros
- Aplicar permisos segun rol (`customer` y `admin`)

## Stack y tecnologias

- Python
- FastAPI
- PostgreSQL
- psycopg2
- JWT con `python-jose`
- Variables de entorno con `python-dotenv`
- Pytest para tests
- Arquitectura en capas con separacion `domain`, `service`, `infrastructure` y `api`

## Arquitectura

El proyecto esta organizado en las siguientes capas:

- `src/domain`: entidades, reglas de negocio y excepciones del dominio
- `src/service`: casos de uso y coordinacion entre dominio y persistencia
- `src/infrastructure`: acceso a base de datos, repositorios y seguridad
- `src/api`: routers, schemas y dependencias de FastAPI

## Funcionalidad actual

### Autenticacion y usuarios

- `POST /auth/register`: registra un usuario y crea su cliente asociado
- `POST /auth/login`: devuelve `access_token` y `refresh_token`
- `POST /auth/refresh`: genera un nuevo `access_token` a partir del refresh token

La autenticacion se realiza con bearer token. Los endpoints protegidos esperan `Authorization: Bearer <token>`.

### Pedidos

- Crear pedido
- Consultar detalle de pedido
- Agregar o actualizar cantidad de un producto en un pedido
- Eliminar un item de un pedido
- Confirmar pedido

Reglas principales:

- Un pedido solo puede modificarse en estado `carrito`
- Un pedido no puede confirmarse si esta vacio
- El stock se valida antes de modificar o confirmar
- El stock se descuenta unicamente al confirmar
- Si la cantidad de un item pasa a `0`, el item se elimina del pedido
- Un usuario solo puede acceder a sus propios pedidos, salvo `admin`

### Productos

- Crear producto
- Obtener producto por id
- Listar productos con paginacion
- Filtrar productos por `estado`, `min_price` y `max_price`

### Clientes

- Obtener cliente por id
- Listar clientes con paginacion
- Filtrar clientes por `nombre`

## Roles y permisos

### `customer`

- Puede registrarse e iniciar sesion
- Puede crear y gestionar sus propios pedidos
- Puede ver su propio perfil de cliente

### `admin`

- Puede crear productos
- Puede listar clientes
- Puede acceder a recursos de otros usuarios cuando la regla de negocio lo permite

## Endpoints

### Auth

- `POST /auth/register`
- `POST /auth/login`
- `POST /auth/refresh`

### Clientes

- `GET /clientes/{cliente_id}`
- `GET /clientes?limit=10&page=1&nombre=ped`

Notas:

- Requieren autenticacion
- `GET /clientes` requiere rol `admin`
- `GET /clientes/{cliente_id}` permite acceso al propio perfil o a `admin`

### Productos

- `POST /productos`
- `GET /productos/{producto_id}`
- `GET /productos?limit=10&page=1&estado=disponible&min_price=10&max_price=100`

Notas:

- `POST /productos` requiere rol `admin`
- Las consultas de listado permiten paginacion y filtros

### Pedidos

- `POST /pedidos`
- `GET /pedidos/{pedido_id}`
- `PATCH /pedidos/{pedido_id}/items`
- `PATCH /pedidos/{pedido_id}/confirmar`
- `DELETE /pedidos/{pedido_id}/items/{producto_id}`

Notas:

- Todos requieren autenticacion
- El acceso al pedido esta restringido al dueno del recurso o `admin`

## Request bodies principales

### Registro

```json
{
  "email": "user@mail.com",
  "password": "123456",
  "nombre": "Pedro"
}
```

### Login

```json
{
  "email": "user@mail.com",
  "password": "123456"
}
```

### Crear producto

```json
{
  "nombre": "Banana",
  "precio": 10,
  "stock": 20
}
```

### Modificar item de pedido

```json
{
  "producto_id": 1,
  "cantidad": 3
}
```

## Variables de entorno

Configura un archivo `.env` con al menos estas variables:

```env
DB_HOST=
DB_PORT=
DB_NAME=
DB_USER=
DB_PASSWORD=
SECRET_KEY=
```

`SECRET_KEY` se usa para firmar los tokens JWT.

## Ejecucion local

### 1. Crear entorno virtual

```bash
python -m venv .venv
```

### 2. Activarlo

En Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Instalar dependencias

```bash
pip install fastapi uvicorn psycopg2 python-dotenv python-jose[cryptography] pytest
```

Si el modulo de hashing no esta instalado en tu entorno, agrega tambien la libreria correspondiente usada por `src/infrastructure/security/password.py`.

### 4. Configurar PostgreSQL

- Crear una base de datos vacia
- Completar las variables del archivo `.env`

### 5. Levantar la API

```bash
uvicorn main:app --reload
```

Documentacion interactiva:

- `http://localhost:8000/docs`

## Base de datos

Al iniciar la aplicacion se abre la conexion y se crean las tablas necesarias si no existen.

Ese bootstrap ocurre desde `main.py`.

## Tests

El proyecto incluye tests unitarios e integracion.

Para ejecutarlos:

```bash
pytest
```

## Estructura del proyecto

```text
.
+-- main.py
+-- src
|   +-- api
|   +-- domain
|   +-- infrastructure
|   +-- service
+-- tests
```
