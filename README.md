# Sistema de Ventas - Supabase API Client

##  Autores
- Alejandro Umaña
- Allan Bolaños
- Brian Ramírez
- Santiago Valverde

Sistema de gestión de ventas con interfaz gráfica (Tkinter) que se conecta a Supabase para implementar un modelo de base de datos transaccional con Row-Level Security (RLS), vistas materializadas y control de autorización basado en roles.

##  Descripción del Proyecto

Este proyecto implementa un sistema completo de ventas que incluye:

- ** Autenticación y Autorización**: Sistema de login con múltiples usuarios y control de acceso basado en Row-Level Security (RLS)
- ** Reportes y Analíticas**: Vistas materializadas para análisis de ventas por categoría, país y productos
- ** Control Geográfico**: Restricción de datos por países permitidos para cada usuario
- ** Control por Categorías**: Filtrado de productos según categorías autorizadas
- ** Interfaz Gráfica**: GUI completa con Tkinter para administración y consultas
- ** Gestión de Usuarios**: Funciones administrativas usando Service Role Key

##  Arquitectura de la Base de Datos

### Tablas Principales

#### 1. **Dominios**
- `countries`: Catálogo de países
- `categories`: Catálogo de categorías de productos

#### 2. **Comercial**
- `products`: Productos con categoría y precio unitario
- `customers`: Clientes con país de origen
- `invoices`: Facturas asociadas a clientes
- `invoice_lines`: Líneas de detalle de cada factura

#### 3. **Autorización (RLS)**
- `user_allowed_country`: Países permitidos por usuario
- `user_allowed_category`: Categorías permitidas por usuario

### Políticas de Seguridad (RLS)

El sistema implementa Row-Level Security para:
- **Productos**: Filtrados por categorías autorizadas del usuario
- **Clientes**: Filtrados por países autorizados
- **Facturas**: Filtradas según el país del cliente
- **Líneas de Factura**: Filtradas por país y categoría simultáneamente

##  Requisitos del Sistema

### Software Necesario
- Python 3.7 o superior
- Cuenta en [Supabase](https://supabase.com)
- Windows (PowerShell) / macOS / Linux

### Dependencias Python
```
requests==2.31.0
tkinter-tooltip==2.2.0
python-dateutil==2.8.2
```

##  Instalación

### 1. Clonar o Descargar el Proyecto
```powershell
git clone <tu-repositorio>
cd DB2_P
```

### 2. Instalar Dependencias
```powershell
pip install -r requirements.txt
```

### 3. Configurar Supabase

#### a) Crear el Proyecto en Supabase
1. Ve a [supabase.com](https://supabase.com) y crea una cuenta
2. Crea un nuevo proyecto
3. Espera a que el proyecto se inicialice completamente

#### b) Ejecutar el Schema SQL
1. En tu proyecto de Supabase, ve a **SQL Editor**
2. Copia el contenido de `database_squema.sql`
3. Ejecuta el script para crear todas las tablas y políticas RLS

#### c) Obtener las Credenciales
1. Ve a **Settings** > **API** en tu dashboard de Supabase
2. Copia:
   - **Project URL**: URL base de tu proyecto
   - **anon/public key**: API Key pública
   - **service_role key**: Key administrativa (¡MANTÉNLA SECRETA!)

#### d) Configurar Credenciales en la Aplicación
Puedes configurar las credenciales de dos formas:

**Opción 1 - Desde la GUI (Recomendado)**:
1. Ejecuta la aplicación: `python main.py`
2. Ve a la pestaña **⚙️ Configuración**
3. Ingresa tus credenciales de Supabase
4. Haz clic en **💾 Guardar Configuración**

**Opción 2 - Editar config.py**:
```python
DEFAULT_SUPABASE_URL = "https://tu-proyecto.supabase.co"
DEFAULT_SUPABASE_KEY = "tu-anon-key"
DEFAULT_SERVICE_ROLE_KEY = "tu-service-role-key"
```

### 4. Crear Usuarios de Prueba

#### Opción A - Desde la GUI
1. Ejecuta la aplicación
2. Ve a **Administración**
3. Completa el formulario "Crear Usuario"
4. Haz clic en **Crear Usuario**

#### Opción B - Desde Supabase Dashboard
1. Ve a **Authentication** > **Users**
2. Clic en **Add user** > **Create new user**
3. Ingresa email y contraseña

### 5. Asignar Permisos (Países y Categorías)

Debes insertar registros en las tablas de autorización:

```sql
-- Permitir al usuario acceder a Costa Rica (CR)
INSERT INTO user_allowed_country (user_id, country_code)
VALUES ('uuid-del-usuario', 'CR');

-- Permitir al usuario ver la categoría Electrónicos (ID 1)
INSERT INTO user_allowed_category (user_id, category_id)
VALUES ('uuid-del-usuario', 1);
```

**Nota**: Obtén el `user_id` (UUID) desde **Authentication** > **Users** en Supabase.

## 🎮 Uso de la Aplicación

### Iniciar la Aplicación
```powershell
python main.py
```

### Funcionalidades Principales

####  **Autenticación**
1. Selecciona un usuario del dropdown
2. Haz clic en **Iniciar Sesión**
3. El estado cambiará a "Autenticado" en verde

####  **Pestaña: Reportes**
- **Sales Fact View**: Vista completa de ventas con joins
- **Sales by Category**: Análisis de ventas agrupadas por categoría
- **Sales by Country**: Ventas filtradas por país (ejemplo: CR)
- **Top Products (30d)**: Productos más vendidos en los últimos 30 días

####  **Pestaña: Autorización**
- **Mis Países Permitidos**: Lista de países a los que tienes acceso
- **Mis Categorías Permitidas**: Categorías de productos autorizadas

####  **Pestaña: Consultas Avanzadas**
- **Productos por Rango de Precio**: Búsqueda con filtros de precio mínimo/máximo
- **Búsqueda de Clientes**: Filtrar clientes por nombre
- **Facturas Este Mes**: Facturas del mes actual
- **Líneas Alto Valor**: Líneas de factura superiores a $1000

####  **Pestaña: Administración** (Requiere Service Role Key)
- **Ver Todos los Usuarios**: Lista completa de usuarios del sistema
- **Crear Usuario**: Registro de nuevos usuarios
- **Asignar Permisos**: Otorgar acceso a países y categorías

##  Estructura del Proyecto

```
DB2_P/
│
├── main.py                              # Aplicación principal con GUI
├── supabase_client.py                   # Cliente para interactuar con Supabase API
├── config.py                            # Configuración de credenciales y usuarios
├── database_squema.sql                  # Schema SQL para crear la BD
├── requirements.txt                     # Dependencias Python
├── test_app.py                          # Script de pruebas
├── Supabase_postman_collection.json     # Colección de Postman para pruebas API
├── Test con 2 usuarios diferentes.pdf   # Documentación de pruebas
└── README.md                            # Este archivo
```

##  Seguridad

### Row-Level Security (RLS)
El proyecto implementa RLS para garantizar que:
- Los usuarios **solo vean datos** de los países y categorías permitidas
- No se puede acceder a datos sin autorización explícita
- Las políticas se aplican a nivel de base de datos, no solo en la UI

### Buenas Prácticas
-  **NUNCA** compartas tu `service_role_key` públicamente
-  Usa `anon key` para operaciones de usuario estándar
-  Usa `service_role key` solo para operaciones administrativas
-  Mantén las credenciales fuera del control de versiones (agrega `config.py` a `.gitignore`)

##  Pruebas

### Ejecutar Tests Automatizados
```powershell
python test_app.py
```

### Pruebas con Postman
1. Importa `Supabase_postman_collection.json` en Postman
2. Configura las variables de entorno:
   - `base_url`: URL de tu proyecto Supabase
   - `api_key`: Tu anon key
   - `jwt_token`: Token obtenido después del login
3. Ejecuta las requests de la colección

### Casos de Prueba Sugeridos
1. **Login con diferentes usuarios**: Verificar que cada usuario ve solo sus datos permitidos
2. **Consultas sin autenticación**: Deben fallar o retornar datos limitados
3. **Intentar acceder a países/categorías no autorizados**: Deben retornar resultados vacíos
4. **Operaciones administrativas sin service_role_key**: Deben fallar

##  Usuarios de Prueba por Defecto

| Email | Password | Descripción |
|-------|----------|-------------|
| brianramirez0farias@gmail.com | password123 | Brian Ramirez |
| usertest@email.com | {Bases@1234} | User Test |
| adbyb.es@gmail.com | {Dep@2022} | ADBYB ES |

**Nota**: Estos usuarios deben existir en tu proyecto de Supabase y tener permisos asignados.

##  Troubleshooting

### Error de Conexión
- Verifica que la URL de Supabase sea correcta
- Comprueba que las API keys sean válidas
- Asegúrate de que el proyecto de Supabase esté activo

### No se Muestran Datos
- Verifica que el usuario tenga permisos asignados en `user_allowed_country` y `user_allowed_category`
- Comprueba que las políticas RLS estén habilitadas
- Revisa que existan datos en las tablas principales

### Error "Policy violation" o "403 Forbidden"
- El usuario no tiene permisos para acceder a esos datos
- Verifica las políticas RLS en Supabase
- Asigna los permisos necesarios en las tablas de autorización

### Tkinter No Disponible
En algunos sistemas, Tkinter no viene instalado por defecto:

**Ubuntu/Debian**:
```bash
sudo apt-get install python3-tk
```

**macOS** (con Homebrew):
```bash
brew install python-tk
```

##  Conceptos de Base de Datos Implementados

-  **Row-Level Security (RLS)**: Seguridad a nivel de fila
-  **Vistas Materializadas**: Para optimizar consultas analíticas
-  **Políticas de Acceso**: Control granular de permisos
-  **Relaciones y Constraints**: Integridad referencial
-  **Autenticación JWT**: Tokens de sesión seguros
-  **API REST**: Interfaz programática con Supabase
-  **Triggers y Functions**: Automatización de procesos

## 📚 Recursos Adicionales

- [Documentación de Supabase](https://supabase.com/docs)
- [Row Level Security en PostgreSQL](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)
- [Supabase Auth](https://supabase.com/docs/guides/auth)
- [Supabase Database](https://supabase.com/docs/guides/database)



- **Proyecto de Base de Datos 2**
- Universidad: Instituto Tecnológico de Costa Rica
- Curso: BD2

##  Licencia

Este proyecto es con fines educativos.

---

**¿Tienes preguntas?** Revisa la documentación de Supabase o consulta con tu instructor.

**¡Buena suerte con el proyecto! **
