from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Crear la aplicación Flask
app = Flask(__name__)

# Configurar la URI de la base de datos y la clave secreta
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///photo_album.db'
app.config['SECRET_KEY'] = 'secret_key'

# Configuración para manejar las imágenes subidas
app.config['UPLOAD_FOLDER'] = 'static/uploads'  # Carpeta para las imágenes
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limitar el tamaño de las imágenes a 16 MB

# Crear el objeto SQLAlchemy
db = SQLAlchemy(app)

# Importar las rutas después de la configuración de db
from routes import *

# Iniciar la aplicación Flask
if __name__ == '__main__':
    # Crear la carpeta de subida si no existe
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    app.run(debug=True)
