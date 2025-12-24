"""Controlador REST para Presupuestos"""
from flask import Blueprint, request, jsonify
from src.services.presupuesto_service import PresupuestoService
from src.api.controllers.base_controller import handle_errors, success_response, error_response

presupuesto_bp = Blueprint('presupuestos', __name__, url_prefix='/api/presupuestos')
presupuesto_service = PresupuestoService()


@presupuesto_bp.route('', methods=['GET'])
@handle_errors
def listar_presupuestos():
    """
    Lista todos los presupuestos.
    
    Query params:
        pendientes: true para mostrar solo pendientes de aceptación
    
    Returns:
        200: Lista de presupuestos
    """
    solo_pendientes = request.args.get('pendientes', '').lower() == 'true'
    
    if solo_pendientes:
        presupuestos = presupuesto_service.obtener_pendientes()
    else:
        presupuestos = presupuesto_service.obtener_todos()
    
    return jsonify({
        'success': True,
        'count': len(presupuestos),
        'data': [p.to_dict() for p in presupuestos]
    }), 200


@presupuesto_bp.route('/ganancias', methods=['GET'])
@handle_errors
def obtener_ganancias():
    """
    Obtiene el total de ganancias de presupuestos aceptados.
    
    Returns:
        200: Total de ganancias
    """
    total = presupuesto_service.obtener_total_ganancias()
    return success_response({'total_ganancias': total})


@presupuesto_bp.route('/<int:cod_presupuesto>', methods=['GET'])
@handle_errors
def obtener_presupuesto(cod_presupuesto: int):
    """
    Obtiene información detallada de un presupuesto.
    
    Args:
        cod_presupuesto: Código del presupuesto
    
    Returns:
        200: Información del presupuesto
        404: Presupuesto no encontrado
    """
    presupuesto = presupuesto_service.obtener_presupuesto(cod_presupuesto)
    
    if not presupuesto:
        return error_response(
            f'Presupuesto con código {cod_presupuesto} no encontrado', 
            404
        )
    
    return success_response(presupuesto.to_dict())


@presupuesto_bp.route('/service/<int:cod_service>', methods=['GET'])
@handle_errors
def obtener_por_service(cod_service: int):
    """
    Obtiene el presupuesto de un servicio.
    
    Args:
        cod_service: Código del servicio
    
    Returns:
        200: Presupuesto del servicio
        404: No tiene presupuesto
    """
    presupuesto = presupuesto_service.obtener_por_service(cod_service)
    
    if not presupuesto:
        return error_response(
            f'El servicio {cod_service} no tiene presupuesto', 
            404
        )
    
    return success_response(presupuesto.to_dict())


@presupuesto_bp.route('', methods=['POST'])
@handle_errors
def crear_presupuesto():
    """
    Crea un nuevo presupuesto para un servicio.
    
    Body JSON:
        codService: Código del servicio (requerido)
        costo: Costo de repuestos
        manoDeObra: Costo de mano de obra
    
    Returns:
        201: Presupuesto creado
        400: Error de validación
    """
    data = request.get_json()
    
    if not data:
        return error_response('No se enviaron datos JSON')
    
    presupuesto = presupuesto_service.crear_presupuesto(data)
    
    return jsonify({
        'success': True,
        'message': 'Presupuesto creado exitosamente',
        'data': presupuesto.to_dict()
    }), 201


@presupuesto_bp.route('/<int:cod_presupuesto>', methods=['PUT'])
@handle_errors
def actualizar_presupuesto(cod_presupuesto: int):
    """
    Actualiza un presupuesto existente.
    
    Args:
        cod_presupuesto: Código del presupuesto
        
    Body JSON:
        costo: Nuevo costo de repuestos
        manoDeObra: Nuevo costo de mano de obra
    
    Returns:
        200: Presupuesto actualizado
    """
    data = request.get_json()
    
    if not data:
        return error_response('No se enviaron datos JSON')
    
    presupuesto = presupuesto_service.actualizar_presupuesto(cod_presupuesto, data)
    
    return jsonify({
        'success': True,
        'message': 'Presupuesto actualizado exitosamente',
        'data': presupuesto.to_dict()
    }), 200


@presupuesto_bp.route('/<int:cod_presupuesto>/aceptar', methods=['POST'])
@handle_errors
def aceptar_presupuesto(cod_presupuesto: int):
    """
    Marca un presupuesto como aceptado por el cliente.
    
    Returns:
        200: Presupuesto aceptado
    """
    presupuesto = presupuesto_service.aceptar_presupuesto(cod_presupuesto)
    
    return jsonify({
        'success': True,
        'message': 'Presupuesto aceptado',
        'data': presupuesto.to_dict()
    }), 200


@presupuesto_bp.route('/<int:cod_presupuesto>/rechazar', methods=['POST'])
@handle_errors
def rechazar_presupuesto(cod_presupuesto: int):
    """
    Marca un presupuesto como rechazado por el cliente.
    
    Returns:
        200: Presupuesto rechazado
    """
    presupuesto = presupuesto_service.rechazar_presupuesto(cod_presupuesto)
    
    return jsonify({
        'success': True,
        'message': 'Presupuesto rechazado',
        'data': presupuesto.to_dict()
    }), 200


@presupuesto_bp.route('/<int:cod_presupuesto>', methods=['DELETE'])
@handle_errors
def eliminar_presupuesto(cod_presupuesto: int):
    """
    Elimina un presupuesto.
    
    Args:
        cod_presupuesto: Código del presupuesto
    
    Returns:
        200: Presupuesto eliminado
    """
    presupuesto_service.eliminar_presupuesto(cod_presupuesto)
    
    return jsonify({
        'success': True,
        'message': 'Presupuesto eliminado exitosamente'
    }), 200
