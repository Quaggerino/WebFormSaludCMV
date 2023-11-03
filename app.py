from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from werkzeug.exceptions import BadRequest
from flask import Flask, render_template_string, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# cagar variables .env
load_dotenv(".env.development")

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# configuracion del mongodb
uri = os.getenv('MONGODB_URI')
client = MongoClient(uri)
#db = client['capstone']
#collection = db['form']
db = client['cmvalparaisoDas']
collection = db['opinionSaludValparaiso']

# Getting the rate limiter MongoDB URI from environment variables
rate_limiter_db_uri = os.getenv('RATE_LIMITER_URI')

# Limiting the number of requests
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    storage_uri=rate_limiter_db_uri,
    strategy='fixed-window'
)


# aplica Content-Security-Policy (CSP) a cada respuesta
@app.after_request
def apply_csp(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:;"
    return response

# ruta home

@app.route('/', methods=['GET', 'POST'])
@limiter.limit("60 per 30 minute")
def home():
   

    if request.method == 'POST':
        try:
            # extraer datos del formulario y validar
            edad = int(request.form.get('edad'))  # convertir edad a entero y validar
            genero = request.form.get('genero')
            cesfam = request.form.get('cesfam')
            frecuencia = request.form.get('frecuencia')
            satisfaccion = int(request.form.get('satisfaccion'))  # convertir satisfaccion a entero y validar
            recomendacion = int(request.form.get('recomendacion'))  # convertir recomendacion a entero y validar
            razon = request.form.get('razon')
            target = 3

            # obtener la fecha del momento que se hizo solicitud
            date = datetime.now()

            # revisar si hay campos vacios
            if not (edad and genero and cesfam and frecuencia and satisfaccion and recomendacion and razon):
                raise BadRequest("Todos los campos deben ser rellenados.")

            # insertar en mongo
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
        except (BadRequest, ValueError) as e:  # error por si algo falla en la conversion o insercion de datos

            error = str(e)
            return render_template('index.html', error=error)
        
    return render_template('index.html')

# pregunta frecuentes

@app.route('/faq')
def faq():
    return render_template('faq.html')

# confirmacion despues de enviar

@app.route('/thankyou')
def thank_you():
    return render_template('thankyou.html')

# estilos css

@app.route('/styles.css')
def css():
    return redirect(url_for('static', filename='styles.css'))

# errores

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
