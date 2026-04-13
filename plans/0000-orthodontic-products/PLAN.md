# Plan: Aplicación Web de Gestión de Productos de Ortodoncia

Aplicación web completa con Flask + SQLite para gestión y visualización de productos de ortodoncia. Sistema con panel de administrador (CRUD productos) y vista pública de catálogo. Despliegue en Render (gratuito).

## Scope

**In:**
- Autenticación de administrador (login/logout con sesión)
- Panel admin: agregar productos (nombre, descripción, categoría, imagen)
- Vista pública: catálogo visual de productos (sin login)
- Catálogo inicial con ~60+ productos investigados (ligas, cadenetas, kit higiene, elásticos, arcos)
- Diseño responsive (móvil + PC)
- Persistencia con SQLite
- Despliegue en Render

**Out:**
- Registro de usuarios (solo admin predefinido)
- Carrito de compras / e-commerce
- Pagos en línea
- Múltiples roles de usuario

## Success Criteria

- [ ] Admin puede loguearse con credenciales `admin / OrthoAdmin2024`
- [ ] Admin puede agregar productos con imagen, nombre, descripción y categoría
- [ ] Usuario no registrado ve todos los productos organizados por categoría
- [ ] Catálogo inicial tiene mínimo 25 ligas, 25 cadenetas, kit higiene, elásticos, arcos
- [ ] Aplicación funciona en móvil y PC (responsive)
- [ ] Datos persisten entre sesiones (SQLite)
- [ ] Aplicación desplegada y accesible públicamente en Render

## Assumptions

- Flask-Login para gestión de sesiones
- Imágenes se almacenan en sistema de archivos local (no CDN externo)
- SQLite es suficiente para escala inicial
- Render free tier es adecuado para este proyecto

## Tech Stack

- **Backend:** Python 3 + Flask
- **Base de datos:** SQLite (con SQLAlchemy ORM)
- **Autenticación:** Flask-Login + werkzeug para hashing de contraseñas
- **Frontend:** HTML5 + CSS3 + JavaScript vanilla (sin frameworks pesados)
- **Estilos:** CSS personalizado con enfoque mobile-first
- **Hosting:** Render (gratuito)
- **Subida de imágenes:** Formularios multipart con almacenamiento local

## Action Items

### Phase 1: Estructura del Proyecto y Configuración

- [ ] Crear estructura de carpetas del proyecto
- [ ] Configurar `requirements.txt` con dependencias (Flask, Flask-Login, Flask-SQLAlchemy, Werkzeug, python-dotenv, gunicorn)
- [ ] Crear `.env` con variables de entorno (SECRET_KEY, ADMIN_PASSWORD)
- [ ] Crear `.gitignore` para Python/Flask
- [ ] Crear `app.py` con inicialización de Flask
- [ ] Configurar SQLAlchemy y Flask-Login en `app.py`
- [ ] Crear `models.py` con modelo User y Product
- [ ] Crear script `init_db.py` para inicializar base de datos y crear admin
- [ ] Ejecutar `init_db.py` y verificar creación de tablas

### Phase 2: Sistema de Autenticación

- [ ] Crear ruta `/login` (GET/POST) con formulario
- [ ] Crear ruta `/logout` (GET)
- [ ] Crear template `templates/login.html` con diseño limpio
- [ ] Implementar verificación de credenciales con werkzeug
- [ ] Proteger rutas de admin con `@login_required`
- [ ] Crear ruta `/admin` como panel principal protegido

### Phase 3: Panel de Administración (CRUD)

- [ ] Crear ruta `/admin/productos` (GET) - listar productos del admin
- [ ] Crear ruta `/admin/productos/nuevo` (GET/POST) - formulario nuevo producto
- [ ] Crear template `templates/admin/base_admin.html` - layout base del panel
- [ ] Crear template `templates/admin/productos_lista.html` - tabla/lista de productos
- [ ] Crear template `templates/admin/producto_formulario.html` - formulario agregar/editar
- [ ] Implementar subida de imágenes con `werkzeug.utils.secure_filename`
- [ ] Configurar carpeta `uploads/` para almacenar imágenes
- [ ] Crear ruta para servir archivos estáticos de uploads
- [ ] Agregar validación de formulario (campos requeridos)
- [ ] Agregar mensajes flash para éxito/error

### Phase 4: Vista Pública (Catálogo Cliente)

- [ ] Crear ruta `/` (GET) - página principal con catálogo
- [ ] Crear ruta `/producto/<id>` (GET) - detalle de producto
- [ ] Crear template `templates/base.html` - layout base público
- [ ] Crear template `templates/index.html` - catálogo principal
- [ ] Crear template `templates/producto_detalle.html` - vista detalle producto
- [ ] Implementar filtrado por categorías en vista pública
- [ ] Implementar diseño de cards/grid responsive para productos

### Phase 5: Catálogo Inicial de Productos

- [ ] Investigar tipos de ligas ortodónticas (25+ colores)
- [ ] Investigar tipos de cadenetas ortodónticas (25+ colores)
- [ ] Investigar kits de higiene ortodóntica
- [ ] Investigar elásticos ortodónticos (medidas 1/4, 1/8, 3/16)
- [ ] Investigar arcos ortodónticos (Nitinol/acero, varios calibres)
- [ ] Crear script `seed_data.py` con catálogo inicial
- [ ] Ejecutar `seed_data.py` y verificar inserción de datos
- [ ] Verificar que catálogo muestra correctamente en vista pública

### Phase 6: Diseño y UX

- [ ] Crear archivo `static/css/style.css` con estilos globales
- [ ] Implementar diseño mobile-first responsive
- [ ] Crear header con navegación (logo, link admin si logueado)
- [ ] Crear footer con info de contacto
- [ ] Estilizar cards de productos con hover effects
- [ ] Estilizar formularios de admin
- [ ] Estilizar tabla de productos en panel admin
- [ ] Agregar indicador visual de categorías
- [ ] Agregar loading states para subida de imágenes
- [ ] Verificar diseño en viewport móvil (375px) y desktop (1440px)

### Phase 7: Preparación para Despliegue

- [ ] Crear `runtime.txt` especificando versión de Python
- [ ] Crear `Procfile` con comando para gunicorn
- [ ] Crear `README.md` con instrucciones de instalación y despliegue
- [ ] Configurar variable `DATABASE_URL` para producción
- [ ] Crear script de migración de datos para producción
- [ ] Verificar que app funciona en modo producción (gunicorn)
- [ ] Agregar manejo de errores 404 y 500 con templates personalizados

### Phase 8: Testing y Verificación

- [ ] Probar flujo completo de login/logout de admin
- [ ] Probar agregar producto con imagen desde panel admin
- [ ] Probar visualización de catálogo sin login
- [ ] Probar filtrado por categorías en vista pública
- [ ] Probar diseño responsive en navegador (dev tools)
- [ ] Verificar persistencia de datos tras reinicio de servidor
- [ ] Verificar que imágenes se sirven correctamente
- [ ] Ejecutar linter (flake8) y corregir issues

### Phase 9: Despliegue en Render

- [ ] Crear repositorio Git del proyecto
- [ ] Conectar repositorio a Render
- [ ] Configurar variables de entorno en Render (SECRET_KEY, ADMIN_PASSWORD)
- [ ] Desplegar aplicación
- [ ] Verificar despliegue exitoso en URL de Render
- [ ] Probar funcionalidad completa en producción
- [ ] Documentar URL pública de la aplicación

## Riskiest Task

**Subida y manejo de imágenes en producción:** Render tiene limitaciones en el sistema de archivos efímero. Las imágenes subidas se pierden en cada deploy. Solución: considerar Cloudinary (free tier) para almacenamiento de imágenes en producción, o documentar esta limitación claramente.

## Clarifications

> **Q:** ¿Qué stack tecnológico prefieres?
> **A:** Python Flask + SQLite

> **Q:** ¿Dónde alojar la aplicación?
> **A:** Flask + Render (recomendado)

> **Q:** ¿Catálogo inicial detallado o general?
> **A:** Investigar y detallar productos reales

> **Q:** ¿Credenciales del admin?
> **A:** admin / OrthoAdmin2024
