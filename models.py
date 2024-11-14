from app import db

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    image = db.Column(db.String(100), nullable=False)  # Solo el nombre del archivo de la imagen

    def __repr__(self):
        return f"<Photo {self.title}>"
