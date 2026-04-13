# OrthoShop - Catálogo de Productos de Ortodoncia

Aplicación web completa para la gestión y visualización de productos de ortodoncia. Desarrollada con Python Flask y SQLite.

## 🦷 Características

- **Catálogo público**: Visualización de productos sin necesidad de login
- **Panel de administración**: Gestión completa de productos (CRUD)
- **Autenticación segura**: Login de administrador con sesiones
- **Subida de imágenes**: Soporte para imágenes de productos
- **Diseño responsive**: Adaptado a móviles y escritorio
- **Búsqueda y filtros**: Por nombre, descripción y categoría

## 🚀 Instalación Local

### Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone <tu-repositorio>
cd PAG-W
```

2. **Crear entorno virtual**
```bash
python -m venv venv
```

3. **Activar entorno virtual**

Windows:
```bash
venv\Scripts\activate
```

Linux/Mac:
```bash
source venv/bin/activate
```

4. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

5. **Configurar variables de entorno**

El archivo `.env` ya está configurado con valores por defecto. Puedes modificarlo si es necesario:

```env
SECRET_KEY=ortho-secret-key-change-in-production-2024
ADMIN_USERNAME=admin
ADMIN_PASSWORD=OrthoAdmin2024
DATABASE_URL=sqlite:///orthodoncia.db
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=5242880
```

6. **Inicializar la base de datos**
```bash
python init_db.py
```

7. **Poblar con catálogo inicial**
```bash
python seed_data.py
```

8. **Ejecutar la aplicación**
```bash
python app.py
```

La aplicación estará disponible en: `http://localhost:5000`

## 👤 Credenciales de Administrador

- **Usuario**: `admin`
- **Contraseña**: `OrthoAdmin2024`

Accede al panel de administración en: `http://localhost:5000/login`

## 📦 Catálogo Inicial

La aplicación incluye más de 75 productos pre-cargados:

- **Ligas**: 25 colores diferentes
- **Cadenetas**: 25 colores diferentes
- **Kit de Higiene**: 4 tipos de kits
- **Elásticos**: 9 variantes (medidas 1/8, 3/16, 1/4 con fuerzas variadas)
- **Arcos Ortodónticos**: 14 tipos (Nitinol, acero, térmicos en varios calibres)

## 🌐 Despliegue en Render

### Paso 1: Crear cuenta en Render

1. Ve a [render.com](https://render.com)
2. Crea una cuenta gratuita (puedes usar GitHub)

### Paso 2: Subir código a GitHub

1. Crea un repositorio en GitHub
2. Sube todo el código del proyecto

### Paso 3: Crear Web Service en Render

1. En el dashboard de Render, haz clic en **"New +"** → **"Web Service"**
2. Conecta tu repositorio de GitHub
3. Configura los siguientes ajustes:

**Configuración:**
- **Name**: `orthoshop` (o el nombre que prefieras)
- **Region**: El más cercano a tu ubicación
- **Branch**: `main` o `master`
- **Root Directory**: Déjalo vacío
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt && python init_db.py && python seed_data.py`
- **Start Command**: `gunicorn app:create_app()`

### Paso 4: Variables de Entorno

En la sección **"Environment"** de tu servicio en Render, agrega:

```
SECRET_KEY=<genera-una-clave-segura-aleatoria>
ADMIN_USERNAME=admin
ADMIN_PASSWORD=OrthoAdmin2024
DATABASE_URL=sqlite:///orthodoncia.db
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=5242880
```

### Paso 5: Desplegar

Haz clic en **"Create Web Service"** y espera a que el despliegue se complete.

Tu aplicación estará disponible en: `https://<tu-app>.onrender.com`

## 📁 Estructura del Proyecto

```
PAG-W/
├── app.py                 # Aplicación principal y rutas
├── models.py              # Modelos de base de datos
├── init_db.py             # Script de inicialización de BD
├── seed_data.py           # Catálogo inicial de productos
├── requirements.txt       # Dependencias de Python
├── Procfile               # Configuración para Render
├── runtime.txt            # Versión de Python
├── .env                   # Variables de entorno
├── .gitignore             # Archivos ignorados por Git
├── templates/             # Plantillas HTML
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── product_detail.html
│   ├── 404.html
│   ├── 500.html
│   └── admin/
│       ├── base_admin.html
│       ├── dashboard.html
│       ├── products_list.html
│       └── product_form.html
├── static/
│   └── css/
│       └── style.css      # Hoja de estilos
└── uploads/               # Imágenes de productos
```

## 🛠️ Tecnologías Utilizadas

- **Backend**: Python 3 + Flask
- **Base de Datos**: SQLite (con SQLAlchemy ORM)
- **Autenticación**: Flask-Login + Werkzeug
- **Frontend**: HTML5 + CSS3 + JavaScript vanilla
- **Hosting**: Render (gratuito)

## ⚠️ Notas Importantes

### Imágenes en Producción

Render utiliza un sistema de archivos efímero, lo que significa que las imágenes subidas se perderán en cada despliegue. Para producción, considera:

1. **Cloudinary** (recomendado, tiene tier gratuito)
2. **AWS S3** (capa gratuita disponible)
3. Documentar que las imágenes deben subirse después de cada despliegue

### Seguridad

- Cambia la `SECRET_KEY` en producción por una clave aleatoria segura
- Usa una contraseña fuerte para el administrador
- Considera implementar HTTPS forzado

## 📝 Comandos Útiles

```bash
# Inicializar BD
python init_db.py

# Poblar catálogo
python seed_data.py

# Ejecutar en desarrollo
python app.py

# Ejecutar con gunicorn (producción)
gunicorn app:create_app()
```

## 📄 Licencia

Este proyecto es de uso educativo y personal.

## 🤝 Soporte

Para dudas o problemas, revisa la documentación de:
- [Flask](https://flask.palletsprojects.com/)
- [Render](https://render.com/docs)
- [SQLAlchemy](https://docs.sqlalchemy.org/)
