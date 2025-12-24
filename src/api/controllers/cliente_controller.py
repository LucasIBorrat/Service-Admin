"""Controlador REST para Clientes"""
from flask import Blueprint, request, jsonify
from src.services.cliente_service import ClienteService
from src.api.controllers.base_controller import handle_errors, success_response, error_response

cliente_bp = Blueprint('clientes', __name__, url_prefix='/api/clientes')
cliente_service = ClienteService()


@cliente_bp.route('', methods=['GET'])
@handle_errors
def listar_clientes():
    """
    Lista todos los clientes.
    
    Query params:
        nombre: Filtrar por nombre (búsqueda parcial)
    
    Returns:
        200: Lista de clientes
    """
    nombre_filtro = request.args.get('nombre')
    
    if nombre_filtro:
        clientes = cliente_service.buscar_por_nombre(nombre_filtro)
    else:
        clientes = cliente_service.obtener_todos()
    
    return jsonify({
        'success': True,
        'count': len(clientes),
        'data': [c.to_dict() for c in clientes]
    }), 200


@cliente_bp.route('/<int:cod_cliente>', methods=['GET'])
@handle_errors
def obtener_cliente(cod_cliente: int):
    """
    Obtiene información detallada de un cliente.
    
    Args:
        cod_cliente: Código del cliente
    
    Returns:
        200: Información del cliente
        404: Cliente no encontrado
    """
    cliente = cliente_service.obtener_cliente(cod_cliente)
    
    if not cliente:
        return error_response(f'Cliente con código {cod_cliente} no encontrado', 404)
    
    return success_response(cliente.to_dict())


@cliente_bp.route('', methods=['POST'])
@handle_errors
def crear_cliente():
    """
    Crea un nuevo cliente.
    
    Body JSON:
        nombre: Nombre del cliente (requerido)
        direccion: Dirección
        tel: Teléfono
        email: Email
    
    Returns:
        201: Cliente creado
        400: Error de validación
    """
    data = request.get_json()
    
    if not data:
        return error_response('No se enviaron datos JSON')
    
    cliente = cliente_service.crear_cliente(data)
    
    return jsonify({
        'success': True,
        'message': 'Cliente creado exitosamente',
        'data': cliente.to_dict()
    }), 201


@cliente_bp.route('/<int:cod_cliente>', methods=['PUT'])
@handle_errors
def actualizar_cliente(cod_cliente: int):
    """
    Actualiza un cliente existente.
    
    Args:
        cod_cliente: Código del cliente
        
    Body JSON (todos opcionales):
        nombre: Nuevo nombre
        direccion: Nueva dirección
        tel: Nuevo teléfono
        email: Nuevo email
    
    Returns:
        200: Cliente actualizado
        404: Cliente no encontrado
    """
    data = request.get_json()
    
    if not data:
        return error_response('No se enviaron datos JSON')
    
    cliente = cliente_service.actualizar_cliente(cod_cliente, data)
    
    return jsonify({
        'success': True,
        'message': 'Cliente actualizado exitosamente',
        'data': cliente.to_dict()
    }), 200


@cliente_bp.route('/<int:cod_cliente>', methods=['DELETE'])
@handle_errors
def eliminar_cliente(cod_cliente: int):
    """
    Elimina un cliente.
    
    Args:
        cod_cliente: Código del cliente
    
    Returns:
        200: Cliente eliminado
        400: No se puede eliminar (tiene servicios pendientes)
        404: Cliente no encontrado
    """
    cliente_service.eliminar_cliente(cod_cliente)
    
    return jsonify({
        'success': True,
        'message': 'Cliente eliminado exitosamente'
    }), 200
