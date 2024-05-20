from app import db


class AreaAlagada(db.Model):
    __tablename__ = 'area_alagada'
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    logradouro = db.Column(db.String)
    cidade = db.Column(db.String)
    bairro = db.Column(db.String)
    descricao = db.Column(db.String)
    cep = db.Column(db.String)

    def __init__(self, logradouro, cidade, bairro, descricao, cep):
        self.logradouro = logradouro
        self.cidade = cidade
        self.bairro = bairro
        self.descricao = descricao
        self.cep = cep
