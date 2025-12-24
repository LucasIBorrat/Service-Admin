"""Controlador base con decoradores y utilidades"""
from functools import wraps
from flask import jsonify
import logging

logger = logging.getLogger(__name__)


def handle_errors(f):
    """
    Decorador para manejar errores en endpoints.
    
    Captura excepciones y retorna respuestas JSON apropiadas.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            logger.warning(f"Validation error in {f.__name__}: {str(e)}")
            return jsonify({
                'success': False,
                'message': str(e)
            }), 400
        except Exception as e:
            logger.error(f"Error in {f.__name__}: {str(e)}", exc_info=True)
            return jsonify({
                'success': False,
                'message': 'Error interno del servidor'
            }), 500
    return decorated_function


def success_response(data=None, message=None, status_code=200):
    """
    Genera una respuesta de éxito estandarizada.
    
    Args:
        data: Datos a incluir en la respuesta
        message: Mensaje descriptivo
        status_code: Código HTTP
        
    Returns:
        Tuple de (response, status_code)
    """
    response = {'success': True}
    if message:
        response['message'] = message
    if data is not None:
        response['data'] = data
    return jsonify(response), status_code


def error_response(message, status_code=400):
    """
    Genera una respuesta de error estandarizada.
    
    Args:
        message: Mensaje de error
        status_code: Código HTTP de error
        
    Returns:
        Tuple de (response, status_code)
    """
    return jsonify({
        'success': False,
        'message': message
    }), status_code
