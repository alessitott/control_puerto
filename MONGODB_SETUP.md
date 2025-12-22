# Configuración de MongoDB para Sistema de Ubicación de Buques

Este documento explica cómo configurar MongoDB para el sistema de ubicación en tiempo real de buques.

## Requisitos

- MongoDB 4.4 o superior (local o MongoDB Atlas)
- Python 3.10+
- pymongo instalado (ya incluido en requirements.txt)

## Opción 1: MongoDB Local

### 1. Instalar MongoDB

**macOS (con Homebrew):**
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install -y mongodb
sudo systemctl start mongodb
sudo systemctl enable mongodb
```

**Windows:**
Descargar e instalar desde: https://www.mongodb.com/try/download/community

### 2. Configurar variables de entorno

Agregar al archivo `.env` en la raíz del proyecto:

```env
# MongoDB Local (sin autenticación)
MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_DATABASE=control_puerto

# MongoDB Local (con autenticación)
MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_DATABASE=control_puerto
MONGO_USERNAME=admin
MONGO_PASSWORD=tu_password
MONGO_AUTH_SOURCE=admin
```

## Opción 2: MongoDB Atlas (Cloud)

### 1. Crear cuenta en MongoDB Atlas

1. Ir a https://www.mongodb.com/cloud/atlas
2. Crear una cuenta gratuita
3. Crear un cluster (tier gratuito M0 disponible)
4. Crear un usuario de base de datos
5. Configurar IP whitelist (0.0.0.0/0 para desarrollo)

### 2. Obtener connection string

En MongoDB Atlas:
1. Click en "Connect"
2. Seleccionar "Connect your application"
3. Copiar la connection string (URI)

### 3. Configurar variables de entorno

Agregar al archivo `.env`:

```env
# MongoDB Atlas (URI completa)
MONGO_URI=mongodb+srv://usuario:password@cluster0.xxxxx.mongodb.net/control_puerto?retryWrites=true&w=majority
```

O usar variables individuales:

```env
MONGO_HOST=cluster0.xxxxx.mongodb.net
MONGO_DATABASE=control_puerto
MONGO_USERNAME=tu_usuario
MONGO_PASSWORD=tu_password
```

## Instalación y Configuración

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Inicializar índices de MongoDB

```bash
python manage.py init_mongodb
```

Este comando crea los índices necesarios:
- Índice geoespacial 2dsphere para búsquedas por ubicación
- Índice en `barco_id` para búsquedas por barco
- Índice en `timestamp` para búsquedas temporales
- Índice compuesto para búsquedas optimizadas

### 3. Probar conexión

```bash
# Opción 1: Usando el endpoint de la API
curl -X GET http://localhost:8000/api/ubicaciones/test/ \
  -H "Authorization: Bearer TU_TOKEN"

# Opción 2: Usando Python
python manage.py shell
>>> from port_control.mongodb import test_connection
>>> test_connection()
True
```

## Variables de Entorno

| Variable | Descripción | Requerido | Default |
|----------|-------------|-----------|---------|
| `MONGO_URI` | URI completa de conexión (MongoDB Atlas) | No* | - |
| `MONGO_HOST` | Host de MongoDB | No* | `localhost` |
| `MONGO_PORT` | Puerto de MongoDB | No | `27017` |
| `MONGO_DATABASE` | Nombre de la base de datos | No | `control_puerto` |
| `MONGO_USERNAME` | Usuario de MongoDB | No | - |
| `MONGO_PASSWORD` | Contraseña de MongoDB | No | - |
| `MONGO_AUTH_SOURCE` | Base de datos de autenticación | No | `admin` |

*Se requiere `MONGO_URI` O `MONGO_HOST`

## Estructura de Datos

### Colección: `ubicaciones_buques`

```json
{
  "_id": ObjectId("..."),
  "barco_id": "550e8400-e29b-41d4-a716-446655440000",
  "ubicacion": {
    "type": "Point",
    "coordinates": [-79.5199, 8.9824]  // [longitud, latitud]
  },
  "velocidad": 12.5,
  "rumbo": 180.0,
  "timestamp": ISODate("2024-01-20T10:30:00Z"),
  "estado": "en_transito",
  "metadata": {
    "distancia_puerto_km": 15.3,
    "simulado": true
  }
}
```

## Endpoints de la API

### Prueba de conexión
```
GET /api/ubicaciones/test/
```

### Registrar ubicación
```
POST /api/ubicaciones/registrar/
Body: {
  "barco_id": "uuid",
  "latitud": 8.9824,
  "longitud": -79.5199,
  "velocidad": 12.5,
  "rumbo": 180.0,
  "estado": "en_transito"
}
```

### Obtener ubicaciones actuales
```
GET /api/ubicaciones/actuales/
```

### Obtener última ubicación de un barco
```
GET /api/ubicaciones/barco/{barco_id}/
```

### Obtener historial de ubicaciones
```
GET /api/ubicaciones/barco/{barco_id}/historial/?inicio=2024-01-01T00:00:00&fin=2024-01-02T00:00:00
```

### Buscar buques cercanos
```
POST /api/ubicaciones/cercanos/
Body: {
  "latitud": 8.9824,
  "longitud": -79.5199,
  "radio_km": 10.0
}
```

### Simulación en tiempo real
```
POST /api/ubicaciones/simulacion/iniciar/
Body: {"intervalo_segundos": 30}

POST /api/ubicaciones/simulacion/detener/

GET /api/ubicaciones/simulacion/estado/
```

## Simulación de Ubicaciones

El sistema incluye un simulador que genera ubicaciones en tiempo real para todos los barcos registrados en PostgreSQL.

### Características:
- Actualiza ubicaciones cada 30 segundos (configurable)
- Simula movimiento realista basado en velocidad y rumbo
- Detecta cuando un barco está cerca del puerto y cambia su estado
- Calcula distancias y rutas

### Iniciar simulación:

```bash
# Desde la API
curl -X POST http://localhost:8000/api/ubicaciones/simulacion/iniciar/ \
  -H "Authorization: Bearer TU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"intervalo_segundos": 30}'
```

## Solución de Problemas

### Error: "No se pudo conectar a MongoDB"

1. Verificar que MongoDB esté corriendo:
   ```bash
   # macOS/Linux
   brew services list  # o systemctl status mongodb
   
   # Verificar puerto
   lsof -i :27017
   ```

2. Verificar variables de entorno en `.env`

3. Verificar firewall/red (MongoDB Atlas)

### Error: "Authentication failed"

1. Verificar credenciales en `.env`
2. Verificar que el usuario tenga permisos en la base de datos
3. Para MongoDB Atlas, verificar IP whitelist

### Error: "Index creation failed"

1. Ejecutar manualmente:
   ```bash
   python manage.py init_mongodb
   ```

2. Verificar permisos de escritura en la base de datos

## Notas Importantes

- MongoDB se usa SOLO para ubicaciones en tiempo real
- Los datos de barcos, tripulación, etc. siguen en PostgreSQL
- Las ubicaciones se relacionan con barcos mediante `barco_id` (UUID de PostgreSQL)
- Los índices geoespaciales permiten búsquedas eficientes por proximidad
- El simulador es opcional y se puede detener en cualquier momento

