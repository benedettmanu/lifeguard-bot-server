from flask import Blueprint, jsonify, request
from app import db
from app.models.area_alagada import AreaAlagada

area_alagada_routes = Blueprint('area_alagada_routes', __name__)

@area_alagada_routes.route('/cadastraArea', methods=['POST'])
def cadastraArea():
    data = request.get_json()
    nova_area = AreaAlagada(**data)
    db.session.add(nova_area)
    db.session.commit()
    return jsonify({'message': 'Área cadastrada com sucesso!'}), 201


@area_alagada_routes.route("/listaAreaAlagada")
def listaAreaAlagada():
    areas_alagadas = AreaAlagada.query.all()
    return jsonify([{'id': area._id, 'logradouro': area.logradouro, 'cidade': area.cidade, 'bairro': area.bairro, 'descricao': area.descricao, 'cep': area.cep} for area in areas_alagadas])
