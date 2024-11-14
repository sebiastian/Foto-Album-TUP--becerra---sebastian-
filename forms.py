from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SubmitField
from wtforms.validators import DataRequired

class PhotoForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired()])
    description = TextAreaField('Descripción')
    image = FileField('Imagen', validators=[DataRequired()])
    submit = SubmitField('Agregar Foto')
