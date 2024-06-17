from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Time, Float

Base = declarative_base()

class UploadControl(Base):
    __tablename__ = 'upload_control'
    
    id = Column(Integer, primary_key=True)
    file_name = Column(String, nullable=False)
    upload_date = Column(Date, nullable=False)

class PlanilhaDados(Base):
    __tablename__ = 'planilha_dados'
    
    id = Column(Integer, primary_key=True)
    data = Column(Date, nullable=False)
    nome = Column(String, nullable=False)
    matricula = Column(String, nullable=False)
    status = Column(String, nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fim = Column(Time, nullable=False)
    duracao = Column(Float, nullable=False)
