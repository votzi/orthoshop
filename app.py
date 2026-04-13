import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from models import db, User, Product

# Cargar variables de entorno
load_dotenv()


def _ensure_database_and_seed(app):
    """Inicializa la BD y carga datos iniciales si no existen."""
    with app.app_context():
        # Crear tablas si no existen
        db.create_all()

        # Crear admin si no existe
        admin = User.query.filter_by(username=os.getenv('ADMIN_USERNAME', 'admin')).first()
        if not admin:
            admin = User(
                username=os.getenv('ADMIN_USERNAME', 'admin'),
                password_hash=generate_password_hash(os.getenv('ADMIN_PASSWORD', 'OrthoAdmin2024'))
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin creado: " + admin.username)

        # Seed data solo si no hay productos
        if Product.query.first():
            return

        products = []

        # Ligas (25 colores)
        ligas = [
            ("Liga Roja", "Liga elastica de color rojo intenso para brackets ortodonticos. Material de alta calidad con excelente elasticidad y resistencia. Compatible con todos los sistemas de brackets estandar.", "Ligas"),
            ("Liga Azul Oscuro", "Liga elastica azul marino profesional. Color sobrio y elegante, muy popular entre pacientes adultos. Excelente fuerza de retencion.", "Ligas"),
            ("Liga Azul Claro", "Liga elastica en tono azul cielo. Color fresco y juvenil que mantiene su intensidad durante todo el tratamiento.", "Ligas"),
            ("Liga Verde", "Liga elastica verde brillante. Color vibrante y energetico, ideal para pacientes jovenes que buscan un look divertido.", "Ligas"),
            ("Liga Rosa", "Liga elastica rosa pastel. Color suave y delicado, especialmente popular entre pacientes adolescentes.", "Ligas"),
            ("Liga Rosa Fuerte", "Liga elastica en tono rosa fuerte/fucsia. Color llamativo y moderno con excelente durabilidad.", "Ligas"),
            ("Liga Naranja", "Liga elastica naranja brillante. Color energetico y divertido, perfecto para combinar con tematicas festivas.", "Ligas"),
            ("Liga Amarilla", "Liga elastica amarilla brillante. Color alegre y luminoso que aporta un toque de alegria a la sonrisa.", "Ligas"),
            ("Liga Morada", "Liga elastica morada/violeta. Uno de los colores mas populares, combina bien con todos los tonos de piel.", "Ligas"),
            ("Liga Blanca", "Liga elastica blanca translucida. Color discreto y limpio que simula la apariencia de brackets ceramicos.", "Ligas"),
            ("Liga Negra", "Liga elastica negra. Color elegante y discreto que hace que los dientes se vean mas blancos por contraste.", "Ligas"),
            ("Liga Gris", "Liga elastica gris plateado. Color neutro y profesional, excelente alternativa al negro.", "Ligas"),
            ("Liga Turquesa", "Liga elastica turquesa. Color tropical y vibrante, muy popular entre adolescentes.", "Ligas"),
            ("Liga Dorada", "Liga elastica color dorado/oro. Color premium y sofisticado que aporta un toque de lujo.", "Ligas"),
            ("Liga Plateada", "Liga elastica color plata. Discreta y elegante, combina perfectamente con brackets metalicos.", "Ligas"),
            ("Liga Verde Lima", "Liga elastica verde lima neon. Color fluorescente y llamativo, ideal para pacientes atrevidos.", "Ligas"),
            ("Liga Lavanda", "Liga elastica lavanda suave. Color pastel tranquilo y elegante, muy estetico.", "Ligas"),
            ("Liga Coral", "Liga elastica color coral. Tono calido entre rosa y naranja, muy popular y favorecedor.", "Ligas"),
            ("Liga Celeste", "Liga elastica celeste claro. Color suave y relajante, alternativa delicada al azul intenso.", "Ligas"),
            ("Liga Fucsia", "Liga elastica fucsia intenso. Color vibrante y atrevido con gran poder de expresion.", "Ligas"),
            ("Liga Cafe", "Liga elastica color cafe/marron. Color neutro y discreto, poco comun pero elegante.", "Ligas"),
            ("Liga Vino", "Liga elastica color vino/borgona. Color elegante y maduro, muy sofisticado.", "Ligas"),
            ("Liga Verde Bosque", "Liga elastica verde bosque oscuro. Color natural y profundo, alternative al verde brillante.", "Ligas"),
            ("Liga Arcoiris", "Liga elastica con colores tornasolados efecto arcoiris. Color especial y unico que cambia con la luz.", "Ligas"),
            ("Liga Transparente", "Liga elastica transparente/cristal. La mas discreta de todas, practicamente invisible.", "Ligas"),
        ]
        for name, desc, cat in ligas:
            products.append(Product(name=name, description=desc, category=cat))

        # Cadenetas (25 colores)
        cadenetas = [
            ("Cadeneta Roja", "Cadena elastica roja para ortodoncia de cierre continuo. Excelente para cerrar espacios y mantener fuerza constante. Paquete de una cadena completa.", "Cadenetas"),
            ("Cadeneta Azul Oscuro", "Cadena elastica azul marino de cierre continuo. Color profesional y sobrio, ideal para adultos. Alta resistencia a la decoloracion.", "Cadenetas"),
            ("Cadeneta Azul Claro", "Cadena elastica azul cielo. Color fresco y juvenil con fuerza de cierre optima para tratamiento ortodontico.", "Cadenetas"),
            ("Cadeneta Verde", "Cadena elastica verde brillante. Color energetico con excelente memoria elastica y durabilidad.", "Cadenetas"),
            ("Cadeneta Rosa", "Cadena elastica rosa pastel. Color suave y popular entre adolescentes. Cierre espaciado uniforme.", "Cadenetas"),
            ("Cadeneta Rosa Fuerte", "Cadena elastica fucsia intensa. Color atrevido y llamativo con fuerza de cierre constante.", "Cadenetas"),
            ("Cadeneta Naranja", "Cadena elastica naranja brillante. Color vibrante y divertido para pacientes con personalidad.", "Cadenetas"),
            ("Cadeneta Amarilla", "Cadena elastica amarilla. Color alegre y luminoso que aporta energia a la sonrisa.", "Cadenetas"),
            ("Cadeneta Morada", "Cadena elastica morada/violeta. Color popular y versatil que favorece a todo tipo de pacientes.", "Cadenetas"),
            ("Cadeneta Blanca", "Cadena elastica blanca translucida. Discreta y limpia, ideal para brackets ceramicos.", "Cadenetas"),
            ("Cadeneta Negra", "Cadena elastica negra. Elegante y discreta, hace que los dientes resalten mas blancos.", "Cadenetas"),
            ("Cadeneta Gris", "Cadena elastica gris. Color neutro y profesional, excelente balance entre discrecion y estilo.", "Cadenetas"),
            ("Cadeneta Turquesa", "Cadena elastica turquesa. Color tropical y moderno con excelente fuerza de retencion.", "Cadenetas"),
            ("Cadeneta Dorada", "Cadena elastica dorada. Color premium y sofisticado para un look diferenciado.", "Cadenetas"),
            ("Cadeneta Plateada", "Cadena elastica plateada. Discreta y elegante, combina con brackets metalicos.", "Cadenetas"),
            ("Cadeneta Verde Lima", "Cadena elastica verde lima neon. Color fluorescente atrevido para pacientes expresivos.", "Cadenetas"),
            ("Cadeneta Lavanda", "Cadena elastica lavanda. Color pastel suave y elegante, muy estetico.", "Cadenetas"),
            ("Cadeneta Coral", "Cadena elastica coral. Tono calido y favorecedor entre rosa y naranja.", "Cadenetas"),
            ("Cadeneta Celeste", "Cadena elastica celeste. Color suave y delicado, alternativa al azul intenso.", "Cadenetas"),
            ("Cadeneta Fucsia", "Cadena elastica fucsia. Color intenso y vibrante con gran impacto visual.", "Cadenetas"),
            ("Cadeneta Cafe", "Cadena elastica cafe. Color neutro y poco comun pero elegante.", "Cadenetas"),
            ("Cadeneta Vino", "Cadena elastica vino/borgona. Color maduro y sofisticado.", "Cadenetas"),
            ("Cadeneta Verde Bosque", "Cadena elastica verde oscuro. Color profundo y natural.", "Cadenetas"),
            ("Cadeneta Arcoiris", "Cadena elastica con efecto tornasol. Color especial que cambia con la luz.", "Cadenetas"),
            ("Cadeneta Transparente", "Cadena elastica transparente/cristal. La mas discreta, practicamente invisible.", "Cadenetas"),
        ]
        for name, desc, cat in cadenetas:
            products.append(Product(name=name, description=desc, category=cat))

        # Kit de Higiene
        kits = [
            ("Kit de Higiene Basico", "Kit completo de higiene para pacientes de ortodoncia. Incluye cepillo dental de cabezal pequeno, cepillo interproximal, hilo dental especial para brackets y cera ortodontica protectora. Todo lo esencial para mantener una limpieza optima durante el tratamiento.", "Kit de Higiene"),
            ("Kit de Higiene Premium", "Kit premium de higiene ortodontica con accesorios avanzados. Incluye cepillo electrico compatible con brackets, irrigador bucal de viaje, cepillos interproximales de varios tamanos, hilo dental Super Floss, cera ortodontica con sabor y estuche de transporte. Ideal para viajeros.", "Kit de Higiene"),
            ("Kit de Higiene de Viaje", "Kit compacto de higiene ortodontica para llevar. Estuche portatil con cepillo plegable, mini pasta dental, cepillo interproximal y cera ortodontica. Perfecto para llevar al colegio, trabajo o viajes. Cabe en cualquier bolsillo.", "Kit de Higiene"),
            ("Kit de Higiene Infantil", "Kit de higiene disenado para ninos en ortodoncia. Incluye cepillo de mangos ergonomicos para manos pequenas, cepillo interproximal suave, hilo dental con guia para ninos, cera con sabores divertidos y guia ilustrada de cepillado. Hace que la higiene sea divertida.", "Kit de Higiene"),
        ]
        for name, desc, cat in kits:
            products.append(Product(name=name, description=desc, category=cat))

        # Elasticos
        elasticos = [
            ("Elasticos 1/4 - Ligeros", "Elasticos ortodonticos medida 1/4 de pulgada (6.35mm). Fuerza ligera de 2oz. Ideales para movimientos dentales suaves y correcciones menores de mordida. Paquete de 100 unidades. Latex-free.", "Elasticos"),
            ("Elasticos 1/4 - Medianos", "Elasticos ortodonticos medida 1/4 de pulgada (6.35mm). Fuerza mediana de 3.5oz. Para correcciones estandar de mordida clase II y III. Excelente elasticidad y fuerza consistente. Paquete de 100 unidades.", "Elasticos"),
            ("Elasticos 1/4 - Fuertes", "Elasticos ortodonticos medida 1/4 de pulgada (6.35mm). Fuerza fuerte de 4.5oz. Para correcciones avanzadas de mordida que requieren mayor presion. Duracion prolongada. Paquete de 100 unidades.", "Elasticos"),
            ("Elasticos 1/8 - Ligeros", "Elasticos ortodonticos medida 1/8 de pulgada (3.17mm). Fuerza ligera de 2oz. Diseno compacto para movimientos precisos en espacios reducidos. Alta resistencia a la rotura. Paquete de 100 unidades.", "Elasticos"),
            ("Elasticos 1/8 - Medianos", "Elasticos ortodonticos medida 1/8 de pulgada (3.17mm). Fuerza mediana de 3.5oz. Para correcciones de mordida en espacios reducidos con fuerza moderada. Calidad premium. Paquete de 100 unidades.", "Elasticos"),
            ("Elasticos 1/8 - Fuertes", "Elasticos ortodonticos medida 1/8 de pulgada (3.17mm). Fuerza fuerte de 4.5oz. Maxima potencia en tamano reducido para correcciones exigentes. Paquete de 100 unidades.", "Elasticos"),
            ("Elasticos 3/16 - Ligeros", "Elasticos ortodonticos medida 3/16 de pulgada (4.76mm). Fuerza ligera de 2oz. Tamano intermedio versatil para multiples aplicaciones ortodonticas. Excelente relacion tamano-fuerza. Paquete de 100 unidades.", "Elasticos"),
            ("Elasticos 3/16 - Medianos", "Elasticos ortodonticos medida 3/16 de pulgada (4.76mm). Fuerza mediana de 3.5oz. El tamano mas versatil para correcciones de mordida estandar. Fuerza constante y duradera. Paquete de 100 unidades.", "Elasticos"),
            ("Elasticos 3/16 - Fuertes", "Elasticos ortodonticos medida 3/16 de pulgada (4.76mm). Fuerza fuerte de 4.5oz. Para correcciones de mordida que requieren fuerza significativa. Alta durabilidad. Paquete de 100 unidades.", "Elasticos"),
        ]
        for name, desc, cat in elasticos:
            products.append(Product(name=name, description=desc, category=cat))

        # Arcos Ortodonticos
        arcos = [
            ("Arco Nitinol 0.012", "Arco ortodontico de Nitinol (NiTi) super elastico calibre 0.012 pulgadas. Ideal para nivelacion inicial. Memoria de forma excepcional y fuerza constante. Longitud: arco superior e inferior. Unidad.", "Arcos Ortodonticos"),
            ("Arco Nitinol 0.014", "Arco ortodontico de Nitinol calibre 0.014 pulgadas. Segunda fase de nivelacion. Excelente relacion flexibilidad-fuerza. Compatible con brackets de ranura 0.018 y 0.022. Unidad.", "Arcos Ortodonticos"),
            ("Arco Nitinol 0.016", "Arco ortodontico de Nitinol calibre 0.016 pulgadas. Versatil para multiples fases del tratamiento. Fuerza suave y continua para movimiento dental eficiente. Unidad.", "Arcos Ortodonticos"),
            ("Arco Nitinol 0.018", "Arco ortodontico de Nitinol calibre 0.018 pulgadas. Para fases intermedias de alineacion. Mayor rigidez que calibres menores manteniendo la super elasticidad. Unidad.", "Arcos Ortodonticos"),
            ("Arco Nitinol 0.020", "Arco ortodontico de Nitinol calibre 0.020 pulgadas. Para fases avanzadas de nivelacion. Alta resistencia con elasticidad controlada. Unidad.", "Arcos Ortodonticos"),
            ("Arco Acero 0.012", "Arco ortodontico de acero inoxidable calibre 0.012 pulgadas. Para fases de finished y detalado. Maximo control y precision en los movimientos finales. Unidad.", "Arcos Ortodonticos"),
            ("Arco Acero 0.014", "Arco ortodontico de acero inoxidable calibre 0.014 pulgadas. Excelente para control de torque y cierre de espacios. Rigidez superior al Nitinol. Unidad.", "Arcos Ortodonticos"),
            ("Arco Acero 0.016", "Arco ortodontico de acero inoxidable calibre 0.016 pulgadas. Versatil para detallado y acabados. Alta estabilidad dimensional. Unidad.", "Arcos Ortodonticos"),
            ("Arco Acero 0.018", "Arco ortodontico de acero inoxidable calibre 0.018 pulgadas. Para brackets de ranura 0.018 en fase final. Maxima precision. Unidad.", "Arcos Ortodonticos"),
            ("Arco Acero 0.020", "Arco ortodontico de acero inoxidable calibre 0.020 pulgadas. Ideal para arcos de trabajo y finalizacion. Excelente control tridimensional. Unidad.", "Arcos Ortodonticos"),
            ("Arco Acero 0.022", "Arco ortodontico de acero inoxidable calibre 0.022 pulgadas. Para brackets de ranura 0.022 en fase final. Maxima rigidez y control. Unidad.", "Arcos Ortodonticos"),
            ("Arco Nitinol Termico 0.016", "Arco ortodontico de Nitinol termico-activado calibre 0.016 pulgadas. Se activa con la temperatura bucal para ejercer fuerza progresiva. Tecnologia de ultima generacion. Unidad.", "Arcos Ortodonticos"),
            ("Arco Nitinol Termico 0.018", "Arco ortodontico de Nitinol termico-activado calibre 0.018 pulgadas. Activacion termica para fuerza constante y suave. Comodidad superior para el paciente. Unidad.", "Arcos Ortodonticos"),
            ("Arco Nitinol Termico 0.020", "Arco ortodontico de Nitinol termico-activado calibre 0.020 pulgadas. Tecnologia termica avanzada para movimientos eficientes. Menos visitas de ajuste necesarias. Unidad.", "Arcos Ortodonticos"),
        ]
        for name, desc, cat in arcos:
            products.append(Product(name=name, description=desc, category=cat))

        db.session.add_all(products)
        db.session.commit()
        print(f"Seed: {len(products)} productos cargados.")


def create_app():
    """Factory para crear la aplicacion Flask."""
    app = Flask(__name__)

    # Configuracion
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///orthodoncia.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 5 * 1024 * 1024))  # 5MB max

    # Inicializar extensiones
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message = 'Por favor inicia sesion para acceder al panel de administracion.'
    login_manager.login_message_category = 'warning'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Asegurar que existe la carpeta de uploads
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Inicializar BD y seed data
    _ensure_database_and_seed(app)

    # Allowed extensions para imagenes
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    # ==================== RUTAS PUBLICAS ====================

    @app.route('/')
    def index():
        """Pagina principal con catalogo de productos."""
        category = request.args.get('category', None)
        search = request.args.get('search', None)

        if category:
            products = Product.query.filter_by(category=category).order_by(Product.created_at.desc()).all()
        elif search:
            products = Product.query.filter(
                db.or_(
                    Product.name.ilike(f'%{search}%'),
                    Product.description.ilike(f'%{search}%')
                )
            ).order_by(Product.created_at.desc()).all()
        else:
            products = Product.query.order_by(Product.created_at.desc()).all()

        # Obtener todas las categorias para el filtro
        categories = db.session.query(Product.category).distinct().order_by(Product.category).all()
        categories = [cat[0] for cat in categories]

        return render_template('index.html', products=products, categories=categories,
                             current_category=category, search=search)

    @app.route('/producto/<int:product_id>')
    def product_detail(product_id):
        """Detalle de un producto."""
        product = Product.query.get_or_404(product_id)
        return render_template('product_detail.html', product=product)

    # ==================== AUTENTICACION ====================

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """Pagina de login para administradores."""
        if current_user.is_authenticated:
            return redirect(url_for('admin_dashboard'))

        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            user = User.query.filter_by(username=username).first()

            if user and check_password_hash(user.password_hash, password):
                login_user(user)
                next_page = request.args.get('next')
                flash('Sesion iniciada correctamente.', 'success')
                return redirect(next_page if next_page else url_for('admin_dashboard'))
            else:
                flash('Usuario o contrasena incorrectos.', 'error')

        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        """Cerrar sesion."""
        logout_user()
        flash('Sesion cerrada correctamente.', 'info')
        return redirect(url_for('index'))

    # ==================== PANEL DE ADMINISTRACION ====================

    @app.route('/admin')
    @login_required
    def admin_dashboard():
        """Panel principal de administracion."""
        total_products = Product.query.count()
        categories = db.session.query(Product.category, db.func.count(Product.id)).group_by(Product.category).all()
        recent_products = Product.query.order_by(Product.created_at.desc()).limit(5).all()
        return render_template('admin/dashboard.html', total=total_products,
                             categories=categories, recent=recent_products)

    @app.route('/admin/productos')
    @login_required
    def admin_products():
        """Lista todos los productos en el panel admin."""
        category = request.args.get('category', None)
        if category:
            products = Product.query.filter_by(category=category).order_by(Product.created_at.desc()).all()
        else:
            products = Product.query.order_by(Product.created_at.desc()).all()

        categories = db.session.query(Product.category).distinct().order_by(Product.category).all()
        categories = [cat[0] for cat in categories]

        return render_template('admin/products_list.html', products=products,
                             categories=categories, current_category=category)

    @app.route('/admin/productos/nuevo', methods=['GET', 'POST'])
    @login_required
    def admin_new_product():
        """Crear nuevo producto."""
        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            description = request.form.get('description', '').strip()
            category = request.form.get('category', '').strip()

            # Validaciones
            if not name or not description or not category:
                flash('Todos los campos son obligatorios.', 'error')
                return render_template('admin/product_form.html', product=None)

            # Manejar subida de imagen
            image_filename = None
            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename != '' and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    # Agregar timestamp para evitar nombres duplicados
                    import time
                    name_parts = filename.rsplit('.', 1)
                    filename = f"{name_parts[0]}_{int(time.time())}.{name_parts[1]}"
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    image_filename = filename
                elif file and file.filename != '':
                    flash('Formato de imagen no valido. Use PNG, JPG, JPEG, GIF o WEBP.', 'error')
                    return render_template('admin/product_form.html', product=None)

            product = Product(
                name=name,
                description=description,
                category=category,
                image_filename=image_filename
            )
            db.session.add(product)
            db.session.commit()
            flash(f'Producto "{name}" creado exitosamente.', 'success')
            return redirect(url_for('admin_products'))

        return render_template('admin/product_form.html', product=None)

    @app.route('/admin/productos/editar/<int:product_id>', methods=['GET', 'POST'])
    @login_required
    def admin_edit_product(product_id):
        """Editar producto existente."""
        product = Product.query.get_or_404(product_id)

        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            description = request.form.get('description', '').strip()
            category = request.form.get('category', '').strip()

            if not name or not description or not category:
                flash('Todos los campos son obligatorios.', 'error')
                return render_template('admin/product_form.html', product=product)

            product.name = name
            product.description = description
            product.category = category

            # Manejar nueva imagen
            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename != '' and allowed_file(file.filename):
                    # Eliminar imagen anterior si existe
                    if product.image_filename:
                        old_path = os.path.join(app.config['UPLOAD_FOLDER'], product.image_filename)
                        if os.path.exists(old_path):
                            os.remove(old_path)

                    import time
                    filename = secure_filename(file.filename)
                    name_parts = filename.rsplit('.', 1)
                    filename = f"{name_parts[0]}_{int(time.time())}.{name_parts[1]}"
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    product.image_filename = filename

            db.session.commit()
            flash(f'Producto "{name}" actualizado exitosamente.', 'success')
            return redirect(url_for('admin_products'))

        return render_template('admin/product_form.html', product=product)

    @app.route('/admin/productos/eliminar/<int:product_id>', methods=['POST'])
    @login_required
    def admin_delete_product(product_id):
        """Eliminar producto."""
        product = Product.query.get_or_404(product_id)

        # Eliminar imagen asociada
        if product.image_filename:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], product.image_filename)
            if os.path.exists(image_path):
                os.remove(image_path)

        db.session.delete(product)
        db.session.commit()
        flash(f'Producto "{product.name}" eliminado exitosamente.', 'success')
        return redirect(url_for('admin_products'))

    # ==================== SERVE UPLOADS ====================

    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        """Servir archivos subidos."""
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    @app.route('/uploads/<path:filename>')
    def uploads(filename):
        """Servir archivos subidos con ruta completa."""
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    # ==================== ERRORES ====================

    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def server_error(error):
        return render_template('500.html'), 500

    return app


# Instancia de la aplicacion para produccion (gunicorn app:app)
app = create_app()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
