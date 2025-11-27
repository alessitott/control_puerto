# Port Control API

API REST para la gestión y control de operaciones portuarias marítimas. Desarrollada con Django REST Framework, autenticación JWT y sistema de permisos basado en roles.

---

## Tabla de Contenidos

1. [Requisitos](#requisitos)
2. [Instalacion](#instalacion)
3. [Configuracion](#configuracion)
4. [Ejecucion](#ejecucion)
5. [Autenticacion](#autenticacion)
6. [Roles y Permisos](#roles-y-permisos)
7. [Endpoints](#endpoints)
8. [Ejemplos de Uso](#ejemplos-de-uso)

---

## Requisitos

- Python 3.10 o superior
- PostgreSQL 12 o superior
- pip (gestor de paquetes de Python)

---

## Instalacion

### 1. Clonar el repositorio

```bash
git clone https://github.com/TU_USUARIO/port_control.git
cd port_control
```

### 2. Crear y activar entorno virtual

```bash
python -m venv venv

# En Linux/Mac:
source venv/bin/activate

# En Windows:
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install django djangorestframework djangorestframework-simplejwt django-filter psycopg2-binary python-dotenv
```

### 4. Crear archivo de variables de entorno

Crear un archivo `.env` en la raiz del proyecto:

```env
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=True
DB_NAME=db_puerto
DB_USER=postgres
DB_PASS=tu_password
DB_HOST=localhost
DB_PORT=5432
```

---

## Configuracion

### 1. Crear la base de datos en PostgreSQL

```sql
CREATE DATABASE db_puerto;
```

### 2. Ejecutar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Crear superusuario (administrador)

```bash
python manage.py createsuperuser
```

---

## Ejecucion

### Iniciar el servidor de desarrollo

```bash
python manage.py runserver
```

El servidor estara disponible en: `http://localhost:8000`

---

## Autenticacion

La API utiliza JWT (JSON Web Tokens) para autenticacion.

### Obtener tokens

```
POST /api/auth/login/
```

Request:
```json
{
    "username": "tu_usuario",
    "password": "tu_password"
}
```

Response:
```json
{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Usar el token en peticiones

Incluir el header `Authorization` con el prefijo `Bearer`:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Renovar token de acceso

```
POST /api/auth/refresh/
```

Request:
```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Duracion de tokens

- Access Token: 60 minutos
- Refresh Token: 7 dias

---

## Roles y Permisos

### Roles disponibles

| Rol | Codigo | Descripcion |
|-----|--------|-------------|
| Administrador | ADMIN | Control total del sistema |
| Capitan de Puerto | CAPITAN_PUERTO | Autoridad maxima operativa |
| Operador de Terminal | OPERADOR_TERMINAL | Gestiona movimientos y contenedores |
| Inspector | INSPECTOR | Realiza inspecciones de seguridad |
| Agente Naviero | AGENTE_NAVIERO | Gestiona barcos y tripulacion |
| Vigilante | VIGILANTE | Solo lectura, monitoreo |

### Matriz de permisos por entidad

| Entidad | ADMIN | CAPITAN_PUERTO | OPERADOR_TERMINAL | INSPECTOR | AGENTE_NAVIERO | VIGILANTE |
|---------|-------|----------------|-------------------|-----------|----------------|-----------|
| Barcos | CRUD | CRUD | Leer | Leer | CRUD | Leer |
| Tripulacion | CRUD | Leer | - | Leer | CRUD | Leer |
| Contenedores | CRUD | CRUD | CRUD | Leer | Leer | Leer |
| Zonas Puerto | CRUD | CRUD | Leer | Leer | - | Leer |
| Personal | CRUD | Leer | - | - | - | - |
| Movimientos | CRUD | CRUD | CRUD | Leer | Leer | Leer |
| Inspecciones | CRUD | Leer | - | CRUD | - | Leer |
| Autorizaciones | CRUD | CRUD | Leer | Leer | Leer | Leer |

CRUD = Crear, Leer, Actualizar, Eliminar

---

## Endpoints

### Autenticacion

| Metodo | Endpoint | Descripcion |
|--------|----------|-------------|
| POST | /api/auth/login/ | Iniciar sesion, obtener tokens |
| POST | /api/auth/refresh/ | Renovar access token |
| POST | /api/auth/verify/ | Verificar validez del token |

### Barcos

| Metodo | Endpoint | Descripcion |
|--------|----------|-------------|
| GET | /api/barcos/ | Listar todos los barcos |
| POST | /api/barcos/ | Crear un barco |
| GET | /api/barcos/{id}/ | Obtener detalle de un barco |
| PUT | /api/barcos/{id}/ | Actualizar un barco |
| PATCH | /api/barcos/{id}/ | Actualizar parcialmente un barco |
| DELETE | /api/barcos/{id}/ | Eliminar un barco |

### Tripulacion

| Metodo | Endpoint | Descripcion |
|--------|----------|-------------|
| GET | /api/tripulacion/ | Listar tripulantes |
| POST | /api/tripulacion/ | Crear tripulante |
| GET | /api/tripulacion/{id}/ | Obtener detalle de tripulante |
| PUT | /api/tripulacion/{id}/ | Actualizar tripulante |
| PATCH | /api/tripulacion/{id}/ | Actualizar parcialmente |
| DELETE | /api/tripulacion/{id}/ | Eliminar tripulante |

### Contenedores

| Metodo | Endpoint | Descripcion |
|--------|----------|-------------|
| GET | /api/contenedores/ | Listar contenedores |
| POST | /api/contenedores/ | Crear contenedor |
| GET | /api/contenedores/{id}/ | Obtener detalle |
| PUT | /api/contenedores/{id}/ | Actualizar contenedor |
| PATCH | /api/contenedores/{id}/ | Actualizar parcialmente |
| DELETE | /api/contenedores/{id}/ | Eliminar contenedor |

### Zonas del Puerto

| Metodo | Endpoint | Descripcion |
|--------|----------|-------------|
| GET | /api/zonas-puerto/ | Listar zonas |
| POST | /api/zonas-puerto/ | Crear zona |
| GET | /api/zonas-puerto/{id}/ | Obtener detalle |
| PUT | /api/zonas-puerto/{id}/ | Actualizar zona |
| PATCH | /api/zonas-puerto/{id}/ | Actualizar parcialmente |
| DELETE | /api/zonas-puerto/{id}/ | Eliminar zona |

### Personal

| Metodo | Endpoint | Descripcion |
|--------|----------|-------------|
| GET | /api/personal/ | Listar personal |
| POST | /api/personal/ | Crear personal |
| GET | /api/personal/{id}/ | Obtener detalle |
| PUT | /api/personal/{id}/ | Actualizar personal |
| PATCH | /api/personal/{id}/ | Actualizar parcialmente |
| DELETE | /api/personal/{id}/ | Eliminar personal |
| GET | /api/personal/me/ | Obtener perfil propio |
| PATCH | /api/personal/update_profile/ | Actualizar perfil propio |

### Movimientos

| Metodo | Endpoint | Descripcion |
|--------|----------|-------------|
| GET | /api/movimientos/ | Listar movimientos |
| POST | /api/movimientos/ | Crear movimiento |
| GET | /api/movimientos/{id}/ | Obtener detalle |
| PUT | /api/movimientos/{id}/ | Actualizar movimiento |
| PATCH | /api/movimientos/{id}/ | Actualizar parcialmente |
| DELETE | /api/movimientos/{id}/ | Eliminar movimiento |

### Inspecciones

| Metodo | Endpoint | Descripcion |
|--------|----------|-------------|
| GET | /api/inspecciones/ | Listar inspecciones |
| POST | /api/inspecciones/ | Crear inspeccion |
| GET | /api/inspecciones/{id}/ | Obtener detalle |
| PUT | /api/inspecciones/{id}/ | Actualizar inspeccion |
| PATCH | /api/inspecciones/{id}/ | Actualizar parcialmente |
| DELETE | /api/inspecciones/{id}/ | Eliminar inspeccion |

### Autorizaciones

| Metodo | Endpoint | Descripcion |
|--------|----------|-------------|
| GET | /api/autorizaciones/ | Listar autorizaciones |
| POST | /api/autorizaciones/ | Crear autorizacion |
| GET | /api/autorizaciones/{id}/ | Obtener detalle |
| PUT | /api/autorizaciones/{id}/ | Actualizar autorizacion |
| PATCH | /api/autorizaciones/{id}/ | Actualizar parcialmente |
| DELETE | /api/autorizaciones/{id}/ | Eliminar autorizacion |

---

## Filtros y Busqueda

Todas las listas soportan filtros, busqueda y ordenamiento.

### Filtros por campo exacto

```
GET /api/barcos/?tipo=carguero&bandera=Panama
```

### Busqueda por texto

```
GET /api/barcos/?search=pacific
```

### Ordenamiento

```
GET /api/barcos/?ordering=-fecha_llegada
GET /api/contenedores/?ordering=peso
```

### Paginacion

```
GET /api/barcos/?page=2
```

Por defecto se muestran 10 resultados por pagina.

---

## Ejemplos de Uso

### 1. Iniciar sesion y obtener token

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'
```

Respuesta:
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAwMDAwMDAwfQ.abc123",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcwMDAwMDAwMH0.xyz789"
}
```

### 2. Listar barcos (con autenticacion)

```bash
curl -X GET http://localhost:8000/api/barcos/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

Respuesta:
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "nombre": "Pacific Star",
      "bandera": "Panama",
      "tipo": "carguero",
      "empresa_operadora": "Maersk",
      "fecha_llegada": "2024-01-15",
      "fecha_salida": null
    }
  ]
}
```

### 3. Crear un barco

```bash
curl -X POST http://localhost:8000/api/barcos/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Atlantic Voyager",
    "bandera": "Liberia",
    "tipo": "tanquero",
    "empresa_operadora": "Shell Maritime",
    "fecha_llegada": "2024-01-20"
  }'
```

### 4. Buscar barcos por nombre

```bash
curl -X GET "http://localhost:8000/api/barcos/?search=atlantic" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### 5. Filtrar contenedores por estado

```bash
curl -X GET "http://localhost:8000/api/contenedores/?estado=en_transito" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### 6. Obtener perfil del usuario autenticado

```bash
curl -X GET http://localhost:8000/api/personal/me/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

Respuesta:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "username": "juan_operador",
  "email": "juan@puerto.com",
  "first_name": "Juan",
  "last_name": "Perez",
  "nombre_completo": "Juan Perez",
  "rol": "OPERADOR_TERMINAL",
  "rol_display": "Operador de Terminal",
  "turno": "matutino",
  "numero_empleado": "EMP-001",
  "telefono": "+507 6000-0000",
  "is_active": true,
  "date_joined": "2024-01-01T00:00:00Z",
  "last_login": "2024-01-20T08:00:00Z"
}
```

### 7. Crear una inspeccion (solo ADMIN o INSPECTOR)

```bash
curl -X POST http://localhost:8000/api/inspecciones/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "contenedor": "550e8400-e29b-41d4-a716-446655440002",
    "inspector": "550e8400-e29b-41d4-a716-446655440001",
    "fecha": "2024-01-20",
    "resultado": "aprobado",
    "observaciones": "Contenedor en buen estado, sin anomalias"
  }'
```

### 8. Renovar token de acceso

```bash
curl -X POST http://localhost:8000/api/auth/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }'
```

---

## Manejo de Errores

La API retorna errores en formato estructurado:

```json
{
  "success": false,
  "error": {
    "code": "PERMISSION_DENIED",
    "message": "No tienes permiso para realizar esta accion",
    "details": null
  }
}
```

### Codigos de error comunes

| Codigo | HTTP Status | Descripcion |
|--------|-------------|-------------|
| VALIDATION_ERROR | 400 | Datos invalidos en la peticion |
| NOT_AUTHENTICATED | 401 | Token no proporcionado o invalido |
| AUTHENTICATION_FAILED | 401 | Credenciales incorrectas |
| PERMISSION_DENIED | 403 | Sin permisos para la accion |
| NOT_FOUND | 404 | Recurso no encontrado |
| INTERNAL_SERVER_ERROR | 500 | Error interno del servidor |

---

## Tecnologias Utilizadas

- Django 5.x
- Django REST Framework 3.x
- SimpleJWT (autenticacion)
- django-filter (filtros)
- PostgreSQL
- Python 3.10+

---

## Licencia

Este proyecto es de uso academico.

