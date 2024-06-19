from app import db
from datetime import datetime, timezone


class AreaAlagada(db.Model):
    __tablename__ = 'area_alagada'
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    logradouro = db.Column(db.String)
    cidade = db.Column(db.String)
    bairro = db.Column(db.String)
    descricao = db.Column(db.String, default='')
    cep = db.Column(db.String, default='')
    data = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    area_confirmada = db.Column(db.Boolean, default=False)

    def __init__(self, logradouro, cidade, bairro, descricao=None, cep=None, data=None, area_confirmada=False):
        self.logradouro = logradouro
        self.cidade = cidade
        self.bairro = bairro
        self.descricao = descricao if descricao is not None else ''
        self.cep = cep if cep is not None else ''
        self.data = data if data is not None else datetime.now(timezone.utc)
        self.area_confirmada = area_confirmada