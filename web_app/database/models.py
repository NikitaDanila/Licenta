from web_app import db

class Profesor(db.Model):
    id_profesor = db.Column(db.Integer, primary_key=True, unique=True,nullable=False)
    email = db.Column(db.String(30), nullable=False, unique=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    admin = db.Column(db.Integer, nullable=False, default=1)

    def __repr__(self):
        return f"Profesor:\nid_profesor: {self.id_prosefor}\nfirst_name: {self.first_name}\nlast_name: {self.last_name}"


class Student(db.Model):
    id_student = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    email = db.Column(db.String(30), nullable=False, unique=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    admin = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f"Elev:\nid_elev: {self.id_student}\nfirst_name: {self.first_name}\nlast_name: {self.last_name}"