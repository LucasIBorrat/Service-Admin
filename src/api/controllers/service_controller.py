"""Controlador REST para Services (Reparaciones)"""
from flask import Blueprint, request, jsonify
from src.services.service_service import ServiceService
from src.api.controllers.base_controller import handle_errors, success_response, error_response

service_bp = Blueprint('services', __name__, url_prefix='/api/services')
service_service = ServiceService()


@service_bp.route('', methods=['GET'])
@handle_errors
def listar_services():
    """
    Lista todos los servicios.
    
    Query params:
        cliente: Filtrar por código de cliente
        estado: Filtrar por estado (pendiente, revisado, reparado, entregado)
    
    Returns:
        200: Lista de servicios
    """
    cliente_filtro = request.args.get('cliente')
    estado_filtro = request.args.get('estado')
    
    if cliente_filtro:
        services = service_service.obtener_por_cliente(int(cliente_filtro))
    elif estado_filtro:
        estado_lower = estado_filtro.lower()
        if estado_lower == 'pendiente':
            services = service_service.obtener_pendientes()
        elif estado_lower == 'entregado':
            services = [s for s in service_service.obtener_todos() if s.entregado]
        elif estado_lower == 'reparado':
            services = service_service.obtener_listos_para_entregar()
        else:
            services = service_service.obtener_todos()
    else:
        services = service_service.obtener_todos()
    
    return jsonify({
        'success': True,
        'count': len(services),
        'data': [s.to_dict() for s in services]
    }), 200


@service_bp.route('/estadisticas', methods=['GET'])
@handle_errors
def obtener_estadisticas():
    """
    Obtiene estadísticas de servicios.
    
    Returns:
        200: Estadísticas agregadas
    """
    stats = service_service.obtener_estadisticas()
    return success_response(stats)


@service_bp.route('/<int:cod_service>', methods=['GET'])
@handle_errors
def obtener_service(cod_service: int):
    """
    Obtiene información detallada de un servicio.
    
    Args:
        cod_service: Código del servicio
    
    Returns:
        200: Información del servicio
        404: Servicio no encontrado
    """
    service = service_service.obtener_service(cod_service)
    
    if not service:
        return error_response(f'Servicio con código {cod_service} no encontrado', 404)
    
    data = service.to_dict()
    # Incluir presupuesto si existe
    if service.presupuesto:
        data['presupuesto'] = service.presupuesto.to_dict()
    
    return success_response(data)


@service_bp.route('', methods=['POST'])
@handle_errors
def crear_service():
    """
    Crea un nuevo servicio de reparación.
    
    Body JSON:
        codCliente: Código del cliente (requerido)
        nomProducto: Nombre del producto (requerido)
        modelo: Modelo del producto
        descrip: Descripción del producto
        descripFalla: Descripción de la falla
    
    Returns:
        201: Servicio creado
        400: Error de validación
    """
    data = request.get_json()
    
    if not data:
        return error_response('No se enviaron datos JSON')
    
    service = service_service.crear_service(data)
    
    return jsonify({
        'success': True,
        'message': 'Servicio creado exitosamente',
        'data': service.to_dict()
    }), 201


@service_bp.route('/<int:cod_service>', methods=['PUT'])
@handle_errors
def actualizar_service(cod_service: int):
    """
    Actualiza un servicio existente.
    
    Args:
        cod_service: Código del servicio
        
    Body JSON (todos opcionales):
        nomProducto, modelo, descrip, descripFalla
        repuesto, costoRepuesto
    
    Returns:
        200: Servicio actualizado
    """
    data = request.get_json()
    
    if not data:
        return error_response('No se enviaron datos JSON')
    
    service = service_service.actualizar_service(cod_service, data)
    
    return jsonify({
        'success': True,
        'message': 'Servicio actualizado exitosamente',
        'data': service.to_dict()
    }), 200


@service_bp.route('/<int:cod_service>/revisar', methods=['POST'])
@handle_errors
def marcar_revisado(cod_service: int):
    """
    Marca un servicio como revisado.
    
    Body JSON (opcional):
        repuesto: Repuestos necesarios
        costoRepuesto: Costo de repuestos
    
    Returns:
        200: Servicio marcado como revisado
    """
    data = request.get_json() or {}
    
    service = service_service.marcar_revisado(
        cod_service,
        repuesto=data.get('repuesto'),
        costo_repuesto=int(data.get('costoRepuesto', 0))
    )
    
    return jsonify({
        'success': True,
        'message': 'Servicio marcado como revisado',
        'data': service.to_dict()
    }), 200


@service_bp.route('/<int:cod_service>/reparar', methods=['POST'])
@handle_errors
def marcar_reparado(cod_service: int):
    """
    Marca un servicio como reparado.
    
    Returns:
        200: Servicio marcado como reparado
    """
    service = service_service.marcar_reparado(cod_service)
    
    return jsonify({
        'success': True,
        'message': 'Servicio marcado como reparado',
        'data': service.to_dict()
    }), 200


@service_bp.route('/<int:cod_service>/entregar', methods=['POST'])
@handle_errors
def marcar_entregado(cod_service: int):
    """
    Marca un servicio como entregado.
    
    Returns:
        200: Servicio marcado como entregado
    """
    service = service_service.marcar_entregado(cod_service)
    
    return jsonify({
        'success': True,
        'message': 'Servicio marcado como entregado',
        'data': service.to_dict()
    }), 200


@service_bp.route('/<int:cod_service>', methods=['DELETE'])
@handle_errors
def eliminar_service(cod_service: int):
    """
    Elimina un servicio.
    
    Args:
        cod_service: Código del servicio
    
    Returns:
        200: Servicio eliminado
    """
    service_service.eliminar_service(cod_service)
    
    return jsonify({
        'success': True,
        'message': 'Servicio eliminado exitosamente'
    }), 200


# =====================
# ENDPOINTS DE REPUESTOS
# =====================

@service_bp.route('/<int:cod_service>/repuestos', methods=['GET'])
@handle_errors
def listar_repuestos(cod_service: int):
    """
    Lista todos los repuestos de un servicio.
    
    Returns:
        200: Lista de repuestos
    """
    from src.models.repuesto import Repuesto
    
    service = service_service.obtener_service(cod_service)
    if not service:
        return error_response(f'Servicio {cod_service} no encontrado', 404)
    
    return jsonify({
        'success': True,
        'data': [r.to_dict() for r in service.repuestos],
        'total': service.total_costo_repuestos
    }), 200


@service_bp.route('/<int:cod_service>/repuestos', methods=['POST'])
@handle_errors
def agregar_repuesto(cod_service: int):
    """
    Agrega un nuevo repuesto a un servicio.
    
    Body JSON:
        nombre: Nombre del repuesto (requerido)
        costo: Costo del repuesto
    
    Returns:
        201: Repuesto agregado
    """
    from src.models.repuesto import Repuesto
    from src.config.database import db
    
    service = service_service.obtener_service(cod_service)
    if not service:
        return error_response(f'Servicio {cod_service} no encontrado', 404)
    
    data = request.get_json()
    if not data or not data.get('nombre'):
        return error_response('El nombre del repuesto es requerido')
    
    repuesto = Repuesto(
        codService=cod_service,
        nombre=data['nombre'],
        costo=int(data.get('costo', 0))
    )
    
    db.session.add(repuesto)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Repuesto agregado exitosamente',
        'data': repuesto.to_dict()
    }), 201


@service_bp.route('/<int:cod_service>/repuestos/<int:repuesto_id>', methods=['PUT'])
@handle_errors
def actualizar_repuesto(cod_service: int, repuesto_id: int):
    """
    Actualiza un repuesto existente.
    
    Body JSON:
        nombre: Nuevo nombre
        costo: Nuevo costo
    
    Returns:
        200: Repuesto actualizado
    """
    from src.models.repuesto import Repuesto
    from src.config.database import db
    
    repuesto = Repuesto.query.filter_by(id=repuesto_id, codService=cod_service).first()
    if not repuesto:
        return error_response(f'Repuesto no encontrado', 404)
    
    data = request.get_json()
    if data.get('nombre'):
        repuesto.nombre = data['nombre']
    if 'costo' in data:
        repuesto.costo = int(data['costo'])
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Repuesto actualizado',
        'data': repuesto.to_dict()
    }), 200


@service_bp.route('/<int:cod_service>/repuestos/<int:repuesto_id>', methods=['DELETE'])
@handle_errors
def eliminar_repuesto(cod_service: int, repuesto_id: int):
    """
    Elimina un repuesto de un servicio.
    
    Returns:
        200: Repuesto eliminado
    """
    from src.models.repuesto import Repuesto
    from src.config.database import db
    
    repuesto = Repuesto.query.filter_by(id=repuesto_id, codService=cod_service).first()
    if not repuesto:
        return error_response(f'Repuesto no encontrado', 404)
    
    db.session.delete(repuesto)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Repuesto eliminado exitosamente'
    }), 200

