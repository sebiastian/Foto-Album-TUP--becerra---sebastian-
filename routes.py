from flask import render_template, request, redirect, url_for, flash
from app import app, db
from models import Photo
from forms import PhotoForm
import os
from werkzeug.utils import secure_filename

# Configuración de la carpeta de subida de imágenes
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    photos = Photo.query.all()
    return render_template('index.html', photos=photos)

@app.route('/add', methods=['GET', 'POST'])
def add_photo():
    form = PhotoForm()
    if form.validate_on_submit():
        # Verificar si se ha cargado una imagen
        if form.image.data:
            image = form.image.data
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                # Guardar la imagen localmente
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                
                new_photo = Photo(
                    title=form.title.data,
                    description=form.description.data,
                    image=filename  # Guardar solo el nombre del archivo
                )
                db.session.add(new_photo)
                db.session.commit()
                flash('Foto agregada con éxito', 'success')
                return redirect(url_for('index'))
            else:
                flash('Archivo no permitido. Asegúrate de cargar una imagen con formato válido', 'danger')
        else:
            flash('No se ha cargado ninguna imagen', 'danger')
    
    return render_template('photo_form.html', form=form)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_photo(id):
    photo = Photo.query.get_or_404(id)
    form = PhotoForm(obj=photo)  # Prellenar el formulario con los datos de la foto

    if form.validate_on_submit():
        photo.title = form.title.data
        photo.description = form.description.data

        # Verificar si se ha cargado una nueva imagen
        if 'image' in request.files and allowed_file(request.files['image'].filename):
            image = request.files['image']
            filename = secure_filename(image.filename)
            # Eliminar la imagen antigua si existe
            old_image_path = os.path.join(app.config['UPLOAD_FOLDER'], photo.image)
            if os.path.exists(old_image_path):
                os.remove(old_image_path)
            # Guardar la nueva imagen
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            photo.image = filename  # Actualizar el nombre de la imagen

        db.session.commit()
        flash('Foto actualizada con éxito', 'success')
        return redirect(url_for('index'))

    return render_template('photo_form.html', form=form, title="Editar Foto")

@app.route('/delete/<int:id>')
def delete_photo(id):
    photo_to_delete = Photo.query.get_or_404(id)
    
    # Eliminar la imagen del servidor
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], photo_to_delete.image)
    if os.path.exists(image_path):
        os.remove(image_path)  # Eliminar el archivo de la carpeta de uploads
    
    # Eliminar la foto de la base de datos
    db.session.delete(photo_to_delete)
    db.session.commit()
    flash('Foto eliminada con éxito', 'success')
    return redirect(url_for('index'))
