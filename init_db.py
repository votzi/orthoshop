"""Script para inicializar la base de datos y crear el usuario administrador."""
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
from models import db
from app import create_app

# Cargar variables de entorno
load_dotenv()


def init_database():
    """Inicializa la BD y crea el usuario admin si no existe."""
    app = create_app()

    with app.app_context():
        # Crear todas las tablas
        print("Creando tablas de la base de datos...")
        db.create_all()
        print("Tablas creadas exitosamente.")

        # Verificar si ya existe un admin
        from models import User
        admin = User.query.filter_by(username=os.getenv('ADMIN_USERNAME', 'admin')).first()

        if not admin:
            admin = User(
                username=os.getenv('ADMIN_USERNAME', 'admin'),
                password_hash=generate_password_hash(os.getenv('ADMIN_PASSWORD', 'OrthoAdmin2024'))
            )
            db.session.add(admin)
            db.session.commit()
            print(f"Usuario administrador '{admin.username}' creado exitosamente.")
        else:
            print("El usuario administrador ya existe.")

        print("Base de datos inicializada correctamente.")


if __name__ == '__main__':
    init_database()
