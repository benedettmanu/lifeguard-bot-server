from flask import Blueprint, jsonify, request
from datetime import datetime, timezone
from app import db
from app.models.area_alagada import AreaAlagada

area_alagada_routes = Blueprint('area_alagada_routes', __name__)

@area_alagada_routes.route('/cadastraArea', methods=['POST'])
def cadastraArea():
    data = request.get_json()
    nova_area = AreaAlagada(**data)
    
    area_confirmada_existente = AreaAlagada.query.filter(
        db.func.date(AreaAlagada.data) == db.func.date(datetime.now(timezone.utc)),
        AreaAlagada.bairro == nova_area.bairro,
        AreaAlagada.cidade == nova_area.cidade,
        AreaAlagada.area_confirmada == True
    ).first()
    
    if area_confirmada_existente:
        nova_area.area_confirmada = True
    else:
        existing_areas = AreaAlagada.query.filter(
            db.func.date(AreaAlagada.data) == db.func.date(datetime.now(timezone.utc)),
            AreaAlagada.bairro == nova_area.bairro,
            AreaAlagada.cidade == nova_area.cidade
        ).all()
        
        if len(existing_areas) >= 4:
            for area in existing_areas:
                area.area_confirmada = True
            nova_area.area_confirmada = True
    
    db.session.add(nova_area)
    db.session.commit()
    
    return jsonify({'message': 'Área cadastrada com sucesso!'}), 201


@area_alagada_routes.route('/confirmarAreaAlagada', methods=['PUT'])
def confirmarAreaAlagada():
    data = request.get_json()
    cidade = data['cidade']
    bairro = data['bairro']
    
    areas_to_confirm = AreaAlagada.query.filter(
        db.func.date(AreaAlagada.data) == db.func.date(datetime.now(timezone.utc)),
        AreaAlagada.cidade == cidade,
        AreaAlagada.bairro == bairro,
        AreaAlagada.area_confirmada == False
    ).all()
    
    if areas_to_confirm:
        for area in areas_to_confirm:
            area.area_confirmada = True
        db.session.commit()
        return jsonify({'message': 'Áreas confirmadas com sucesso!'}), 200
    else:
        return jsonify({'message': 'Nenhuma área para confirmar.'}), 404



@area_alagada_routes.route("/listaAreaAlagada")
def listaAreaAlagada():
    areas_alagadas = AreaAlagada.query.all()
    return jsonify([{'id': area._id, 'logradouro': area.logradouro, 'cidade': area.cidade, 'bairro': area.bairro, 'descricao': area.descricao, 'cep': area.cep, 'data': area.data, 'area_confirmada': area.area_confirmada} for area in areas_alagadas])


@area_alagada_routes.route("/listaAreasAlagadasConfirmadas")
def listaAreasAlagadasConfirmadas():
    current_date = db.func.date(datetime.now(timezone.utc))
    confirmed_flooded_areas = AreaAlagada.query.filter(
        db.func.date(AreaAlagada.data) == current_date,
        AreaAlagada.area_confirmada == True
    ).all()

    grouped_by_city_neighborhood = {}
    for area in confirmed_flooded_areas:
        key = (area.cidade, area.bairro)
        if key not in grouped_by_city_neighborhood:
            grouped_by_city_neighborhood[key] = []
        else:
            existing_streets = [d['logradouro'] for d in grouped_by_city_neighborhood[key]]
            if area.logradouro in existing_streets:
                continue 
        grouped_by_city_neighborhood[key].append({
            'logradouro': area.logradouro,
            'descricao': area.descricao
        })

    result = []
    for (city, neighborhood), streets in grouped_by_city_neighborhood.items():
        result.append({
            'bairro': neighborhood,
            'cidade': city,
            'ruas': streets
        })

    return jsonify(result)

