import os
import datetime
import threading
from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

# Obtém a DATABASE_URL do ambiente e ajusta se necessário
DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Cria a conexão com o banco de dados
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Modelos do banco de dados
class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    range_start = Column(String, nullable=False)
    range_end = Column(String, nullable=False)
    assigned_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    status = Column(String, default="pending")

class Metadata(Base):
    __tablename__ = "metadata"
    key = Column(String, primary_key=True, index=True)
    value = Column(String)

class FoundWallet(Base):
    __tablename__ = "found_wallets"
    id = Column(Integer, primary_key=True, index=True)
    hex_private_key = Column(String)
    wif_private_key = Column(String)
    public_key = Column(String)
    uncompressed_address = Column(String)
    full_db_address = Column(String)
    status = Column(String)
    tested_candidate = Column(Integer)
    substring = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

# Cria as tabelas no banco de dados, se ainda não existirem
Base.metadata.create_all(bind=engine)

# Configurações para distribuição de tarefas
TASK_SIZE = 1000000  # 1 milhão de candidatos por tarefa
ASSIGNED_TASKS_FILE = "last_assigned_task.txt"
task_lock = threading.Lock()
current_range_start = 0

def load_last_assigned():
    global current_range_start
    if os.path.exists(ASSIGNED_TASKS_FILE):
        with open(ASSIGNED_TASKS_FILE, "r") as f:
            line = f.read().strip()
            if line:
                try:
                    current_range_start = int(line)
                except Exception as e:
                    print("Erro ao ler last_assigned_task.txt:", e)
                    current_range_start = 0
    else:
        current_range_start = 0

def save_last_assigned(value):
    with open(ASSIGNED_TASKS_FILE, "w") as f:
        f.write(str(value))

# Carrega o último valor atribuído
load_last_assigned()

@app.route('/')
def index():
    return "Projeto Jupiter - Servidor online. Use /get_task para obter uma tarefa."

@app.route('/get_task', methods=['GET'])
def get_task():
    """
    Distribui um intervalo (range) de tarefas para um worker.
    """
    global current_range_start
    with task_lock:
        # Limite total (5 bytes): 2**40
        if current_range_start >= 2**40:
            return jsonify({"message": "No more tasks available"}), 404
        start = current_range_start
        end = start + TASK_SIZE
        current_range_start = end
        save_last_assigned(current_range_start)
    print(f"Assigned task range: {start} to {end}")
    # Usa o valor de start como task_id (para simplicidade)
    return jsonify({"task_id": start, "start": str(start), "end": str(end)})

@app.route('/task_complete', methods=['POST'])
def task_complete():
    """
    Recebe e registra a conclusão de uma tarefa pelos workers.
    """
    data = request.json
    # Aqui, você pode atualizar o status da tarefa no banco de dados, se necessário.
    print("Completed task:", data)
    return jsonify({"message": "Task completion recorded"})

@app.route('/found', methods=['POST'])
def found():
    """
    Recebe os dados de uma carteira encontrada (ou quase encontrada) e os registra na tabela FoundWallet.
    """
    data = request.json
    session = SessionLocal()
    wallet = FoundWallet(
        hex_private_key=data.get("hex private key"),
        wif_private_key=data.get("WIF private key"),
        public_key=data.get("public key"),
        uncompressed_address=data.get("uncompressed address"),
        full_db_address=data.get("full_db_address"),
        status=data.get("status"),
        tested_candidate=data.get("tested_candidate"),
        substring=data.get("substring"),
        timestamp=datetime.datetime.utcnow()
    )
    session.add(wallet)
    session.commit()
    session.close()
    print("Wallet found reported:")
    print("Generated address:".ljust(22), data.get("uncompressed address"))
    print("Database address: ".ljust(22), data.get("full_db_address"))
    return jsonify({"message": "Wallet result recorded"})

if __name__ == '__main__':
    app.run(debug=True)
