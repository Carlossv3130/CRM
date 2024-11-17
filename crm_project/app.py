from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from datetime import datetime
from bson import ObjectId  # Importar ObjectId para manejar identificadores de MongoDB

app = Flask(__name__)

# Configuración de MongoDB
app.config["MONGO_URI"] = "mongodb+srv://carlossv3130:4VJd4yX8viAsDjqB@cluster0.w7fek.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
mongo = PyMongo(app)

# Rutas del sistema
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_client', methods=['GET', 'POST'])
def add_client():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form['telefono']
        cliente = {
            "nombre": nombre,
            "email": email,
            "telefono": telefono,
            "interacciones": [],
            "contratos": []
        }
        mongo.db.clientes.insert_one(cliente)  # Inserta un nuevo cliente en la base de datos
        return redirect(url_for('index'))
    return render_template('add_client.html')

@app.route('/view_client/<client_id>')
def view_client(client_id):
    try:
        cliente = mongo.db.clientes.find_one_or_404({'_id': ObjectId(client_id)})  # Convertir client_id a ObjectId
        return render_template('view_client.html', cliente=cliente)
    except Exception as e:
        return f"Error: {e}"

@app.route('/add_interaction/<client_id>', methods=['POST'])
def add_interaction(client_id):
    try:
        descripcion = request.form['descripcion']
        interaccion = {
            "descripcion": descripcion,
            "fecha": datetime.utcnow()
        }
        mongo.db.clientes.update_one(
            {'_id': ObjectId(client_id)},  # Convertir client_id a ObjectId
            {'$push': {'interacciones': interaccion}}  # Agregar la nueva interacción
        )
        return redirect(url_for('view_client', client_id=client_id))
    except Exception as e:
        return f"Error: {e}"

@app.route('/add_contract/<client_id>', methods=['POST'])
def add_contract(client_id):
    try:
        descripcion = request.form['descripcion']
        contrato = {
            "descripcion": descripcion,
            "fecha_inicio": datetime.utcnow()
        }
        mongo.db.clientes.update_one(
            {'_id': ObjectId(client_id)},  # Convertir client_id a ObjectId
            {'$push': {'contratos': contrato}}  # Agregar el nuevo contrato
        )
        return redirect(url_for('view_client', client_id=client_id))
    except Exception as e:
        return f"Error: {e}"

@app.route('/report')
def report():
    clientes = mongo.db.clientes.find()  # Obtener todos los clientes
    report_data = []
    for cliente in clientes:
        ventas = len(cliente['contratos'])  # Contar la cantidad de contratos (ventas)
        report_data.append({'cliente': cliente['nombre'], 'ventas': ventas})
    return render_template('report.html', report_data=report_data)

if __name__ == '__main__':
    # Ejecutar la aplicación Flask en el puerto 3000
    app.run(debug=True, port=3000)
