import os
import pandas as pd
from flask import Flask, request, jsonify, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, UploadControl, PlanilhaDados
import json
import io
from datetime import datetime
from functools import wraps

# Carregar configurações do secrets.json
with open('secrets.json') as f:
    config = json.load(f)

app = Flask(__name__, template_folder='templates')

# Configuração do banco de dados
DATABASE_URI = config['DATABASE_URI']
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

# Segredo da aplicação
app.config['SECRET_KEY'] = config['SECRET_KEY']

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token or token != app.config['SECRET_KEY']:
            return jsonify({"message": "Token is missing or invalid!"}), 403
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
@token_required
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    upload_date_str = request.form.get('date')
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        upload_date = datetime.strptime(upload_date_str, '%Y-%m-%d').date()
        if not is_file_uploaded_today(file.filename, upload_date):
            data_frame = read_file(file)  # Usar a função read_file para ler o arquivo
            if data_frame is None:
                return jsonify({"error": "Unsupported file format"}), 400
            
            # Formatar a coluna de data para o formato esperado pelo PostgreSQL
            data_frame['data'] = pd.to_datetime(data_frame['data'], errors='coerce').dt.strftime('%Y-%m-%d')
            
            json_data = data_frame.to_json(orient='records')
            insert_data(json_data)
            log_file_upload(file.filename, upload_date)
            
            return jsonify({"message": "File processed and data inserted"}), 200
        else:
            return jsonify({"error": "File already uploaded today"}), 400
    
    return jsonify({"error": "Unsupported file format"}), 400

@app.route('/check_upload', methods=['POST'])
@token_required
def check_upload():
    filename = request.form.get('filename')
    upload_date_str = request.form.get('date')
    
    if not filename or not upload_date_str:
        return jsonify({"error": "Filename and date are required"}), 400
    
    upload_date = datetime.strptime(upload_date_str, '%Y-%m-%d').date()
    if is_file_uploaded_today(filename, upload_date):
        return jsonify({"exists": True}), 200
    else:
        return jsonify({"exists": False}), 200

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['xlsx', 'xls', 'csv']

def read_file(file):
    file_ext = file.filename.rsplit('.', 1)[1].lower()
    if file_ext == 'xlsx' or file_ext == 'xls':
        return pd.read_excel(file)
    elif file_ext == 'csv':
        return pd.read_csv(file)
    else:
        return None

def is_file_uploaded_today(filename, upload_date):
    session = Session()
    count = session.query(UploadControl).filter_by(file_name=filename, upload_date=upload_date).count()
    session.close()
    return count > 0

def log_file_upload(filename, upload_date):
    session = Session()
    new_upload = UploadControl(file_name=filename, upload_date=upload_date)
    session.add(new_upload)
    session.commit()
    session.close()

def insert_data(json_data):
    data = json.loads(json_data)
    session = Session()
    for record in data:
        # Convertendo strings para tipos apropriados
        record['data'] = datetime.strptime(record['data'], '%Y-%m-%d').date()
        record['hora_inicio'] = datetime.strptime(record['hora_inicio'], '%H:%M:%S').time()
        record['hora_fim'] = datetime.strptime(record['hora_fim'], '%H:%M:%S').time()
        
        # Calculando a duração em horas
        hora_inicio = datetime.combine(record['data'], record['hora_inicio'])
        hora_fim = datetime.combine(record['data'], record['hora_fim'])
        duracao = (hora_fim - hora_inicio).total_seconds() / 3600  # Duração em horas
        record['duracao'] = duracao
        
        new_record = PlanilhaDados(**record)
        session.add(new_record)
    session.commit()
    session.close()

if __name__ == '__main__':
    app.run(debug=True)
