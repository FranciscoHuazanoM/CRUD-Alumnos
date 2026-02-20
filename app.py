import os
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Crear instancia
app = Flask(__name__)

# ==============================
# CONFIGURACIÓN BASE DE DATOS
# ==============================
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://crud_alumnos_2026_user:1calS9AaCgbDv8Lms5Jzfo4PMNFQVvrn@dpg-d6ai0kfgi27c73b7ibeg-a.oregon-postgres.render.com/crud_alumnos_2026?sslmode=require"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ==============================
# MODELO
# ==============================
class Estudiante(db.Model):
    __tablename__ = 'estudiantes'

    no_control = db.Column(db.String, primary_key=True)
    nombre = db.Column(db.String)
    ap_paterno = db.Column(db.String)
    ap_materno = db.Column(db.String)
    semestre = db.Column(db.Integer)

    def to_dict(self):
        return {
            'no_control': self.no_control,
            'nombre': self.nombre,
            'ap_paterno': self.ap_paterno,
            'ap_materno': self.ap_materno,
            'semestre': self.semestre,
        }

# Crear tablas si no existen
with app.app_context():
    db.create_all()

# ==============================
# RUTAS
# ==============================

@app.route('/')
def index():
    estudiantes = Estudiante.query.all()
    return render_template('index.html', estudiantes=estudiantes)

# Crear estudiante
@app.route('/estudiantes/new', methods=['GET', 'POST'])
def create_estudiante():
    if request.method == 'POST':
        nuevo = Estudiante(
            no_control=request.form['no_control'],
            nombre=request.form['nombre'],
            ap_paterno=request.form['ap_paterno'],
            ap_materno=request.form['ap_materno'],
            semestre=int(request.form['semestre'])
        )

        db.session.add(nuevo)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('create_estudiante.html')

# Eliminar estudiante
@app.route('/estudiantes/delete/<string:no_control>')
def delete_estudiante(no_control):
    estudiante = Estudiante.query.get(no_control)
    if estudiante:
        db.session.delete(estudiante)
        db.session.commit()
    return redirect(url_for('index'))

# Actualizar estudiante
@app.route('/estudiantes/update/<string:no_control>', methods=['GET', 'POST'])
def update_estudiante(no_control):
    estudiante = Estudiante.query.get(no_control)

    if request.method == 'POST':
        estudiante.nombre = request.form['nombre']
        estudiante.ap_paterno = request.form['ap_paterno']
        estudiante.ap_materno = request.form['ap_materno']
        estudiante.semestre = int(request.form['semestre'])
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('update_estudiante.html', estudiante=estudiante)

# Ruta prueba
@app.route('/alumnos')
def getAlumnos():
    return 'Aquí van los alumnos'

# ==============================
# MAIN
# ==============================
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)