import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from models import db, User, Product

# Cargar variables de entorno
load_dotenv()


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


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
