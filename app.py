from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
import os
from werkzeug.exceptions import BadRequest
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import Flask, render_template_string, request

# Load environment variables from the .env.development file
# Cargar variables de entorno del archivo .env.development
load_dotenv(".env.development")

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# MongoDB configuration
# Configuración de MongoDB
uri = os.getenv('MONGODB_URI')
client = MongoClient(uri)
db = client['cmvalparaisoDas']
collection = db['opinionSaludValparaiso']

# MongoDB URI from the .env for Flask rate limiter
# URI de MongoDB desde el .env para el limitador de tasa de Flask
rate_limiter_db_uri = os.getenv('RATE_LIMITER_URI')

# Defining the rate limiter to limit requests per IP
# Definiendo el limitador de tasa para limitar solicitudes por IP
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    storage_uri=rate_limiter_db_uri,
    strategy='fixed-window'
)

# Apply Content-Security-Policy (CSP) to each response
# Aplica la Política de Seguridad de Contenido (CSP) a cada respuesta
@app.after_request
def apply_csp(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:;"
    return response

# Home route
# Ruta de inicio
@app.route('/', methods=['GET', 'POST'])
@limiter.limit("60 per 30 minute")
def home():
    if request.method == 'POST':
        try:
            # Extract data from the form and validate
            # Extraer datos del formulario y validar
            edad = int(request.form.get('edad'))  # Convert age to integer and validate
            genero = request.form.get('genero')
            cesfam = request.form.get('cesfam')
            frecuencia = request.form.get('frecuencia')
            satisfaccion = int(request.form.get('satisfaccion'))  # Convert satisfaction to integer and validate
            recomendacion = int(request.form.get('recomendacion'))  # Convert recommendation to integer and validate
            razon = request.form.get('razon')
            target = 3

            # Get the current date and time
            # Obtener la fecha y hora actuales
            date = datetime.now()

            # Check for empty fields
            # Verificar si hay campos vacíos
            if not (edad and genero and cesfam and frecuencia and satisfaccion and recomendacion and razon):
                raise BadRequest("Todos los campos deben ser rellenados.")

            # Insert data into MongoDB
            # Insertar datos en MongoDB
            collection.insert_one({
                'edad': edad,
                'genero': genero,
                'cesfam': cesfam,
                'frecuencia': frecuencia,
                'satisfaccion': satisfaccion,
                'recomendacion': recomendacion,
                'razon': razon,
                'date': date,
                'target': target
            })

            return redirect(url_for('thank_you'))
        except (BadRequest, ValueError) as e:  # Error handling for data conversion or insertion
            error = str(e)
            return render_template('index.html', error=error)
        
    return render_template('index.html')

# Frequently Asked Questions route
# Ruta de Preguntas Frecuentes
@app.route('/faq')
def faq():
    return render_template('faq.html')

# Thank you page after submission
# Página de agradecimiento después de enviar
@app.route('/thankyou')
def thank_you():
    return render_template('thankyou.html')

# Route for CSS styles
# Ruta para estilos CSS
@app.route('/styles.css')
def css():
    return redirect(url_for('static', filename='styles.css'))

# Error handlers
# Manejadores de errores
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.errorhandler(429)
def ratelimit_error(e):
    return render_template_string("Haz alcanzado el límite de solicitudes"), 429

if __name__ == "__main__":
    app.run(debug=True)
