"""Punto de entrada principal de la aplicación ServiceAdmin"""
import os
import logging
from flask import Flask, jsonify, render_template, request, redirect, url_for
from src.config.database import init_db, db
from src.config.settings import settings


# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_app():
    """
    Factory function para crear y configurar la aplicación Flask.
    
    Aplica el patrón Application Factory para facilitar testing
    y configuración por ambiente.
    
    Returns:
        Aplicación Flask configurada
    """
    app = Flask(
        __name__,
        template_folder='templates',
        static_folder='static'
    )
    
    # Configuración
    app.config['SECRET_KEY'] = settings.app.secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.database.url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = settings.database.echo
    
    # IMPORTANTE: Importar modelos ANTES de init_db para que SQLAlchemy
    # los conozca al momento de crear las tablas con db.create_all()
    from src.models.cliente import Cliente
    from src.models.service import Service
    from src.models.presupuesto import Presupuesto
    from src.models.repuesto import Repuesto
    
    # Inicializar base de datos (ahora creará las tablas correctamente)
    init_db(app)
    
    # Registrar blueprints (API)
    from src.api.controllers.cliente_controller import cliente_bp
    from src.api.controllers.service_controller import service_bp
    from src.api.controllers.presupuesto_controller import presupuesto_bp
    
    app.register_blueprint(cliente_bp)
    app.register_blueprint(service_bp)
    app.register_blueprint(presupuesto_bp)
    
    # =====================
    # RUTAS DE TEMPLATES
    # =====================
    
    @app.route('/')
    def index():
        """Página principal - Dashboard"""
        from src.services.service_service import ServiceService
        from src.services.cliente_service import ClienteService
        from src.services.presupuesto_service import PresupuestoService
        
        service_service = ServiceService()
        cliente_service = ClienteService()
        presupuesto_service = PresupuestoService()
        
        estadisticas = service_service.obtener_estadisticas()
        total_clientes = len(cliente_service.obtener_todos())
        total_ganancias = presupuesto_service.obtener_total_ganancias()
        
        return render_template('index.html',
            estadisticas=estadisticas,
            total_clientes=total_clientes,
            total_ganancias=total_ganancias
        )
    
    @app.route('/clientes')
    def clientes_page():
        """Página de gestión de clientes"""
        from src.services.cliente_service import ClienteService
        cliente_service = ClienteService()
        clientes = cliente_service.obtener_todos()
        return render_template('clientes.html', clientes=clientes)
    
    @app.route('/services')
    def services_page():
        """Página de listado de servicios"""
        from src.services.service_service import ServiceService
        from src.services.cliente_service import ClienteService
        
        service_service = ServiceService()
        cliente_service = ClienteService()
        
        # Obtener parámetro de filtro
        estado_filtro = request.args.get('estado')
        
        # Aplicar filtro según el estado
        if estado_filtro == 'pendiente':
            services = service_service.obtener_pendientes()
        elif estado_filtro == 'revisado':
            # Revisados pero no reparados
            services = [s for s in service_service.obtener_todos() 
                       if s.revisado and not s.reparado]
        elif estado_filtro == 'reparado':
            services = service_service.obtener_listos_para_entregar()
        elif estado_filtro == 'entregado':
            services = [s for s in service_service.obtener_todos() if s.entregado]
        else:
            services = service_service.obtener_todos()
        
        clientes = cliente_service.obtener_todos()
        
        return render_template('services.html', 
            services=services,
            clientes=clientes
        )
    
    @app.route('/ganancias')
    def ganancias_page():
        """Página de reporte de ganancias por mes"""
        from src.services.service_service import ServiceService
        from datetime import date
        
        service_service = ServiceService()
        
        # Obtener mes y año de los parámetros o usar el actual
        mes = request.args.get('mes', type=int, default=date.today().month)
        anio = request.args.get('anio', type=int, default=date.today().year)
        
        # Nombres de meses en español
        meses = ['', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        
        # Obtener todos los services y filtrar por mes
        todos_services = service_service.obtener_todos()
        services = [s for s in todos_services 
                   if s.fecha and s.fecha.month == mes and s.fecha.year == anio]
        
        # Calcular totales (solo de services con presupuesto)
        total_repuestos = sum(s.total_costo_repuestos for s in services if s.presupuesto)
        total_mano_obra = sum(s.presupuesto.manoDeObra for s in services if s.presupuesto)
        total_general = total_repuestos + total_mano_obra
        
        return render_template('ganancias.html',
            services=services,
            mes=mes,
            anio=anio,
            mes_nombre=meses[mes],
            total_repuestos=total_repuestos,
            total_mano_obra=total_mano_obra,
            total_general=total_general
        )
    
    @app.route('/services/agregar')
    def agregar_service_page():
        """Página para agregar nuevo servicio"""
        from src.services.cliente_service import ClienteService
        cliente_service = ClienteService()
        clientes = cliente_service.obtener_todos()
        return render_template('agregar_service.html', clientes=clientes)
    
    @app.route('/services/<int:cod_service>/editar')
    def editar_service_page(cod_service: int):
        """Página para editar un servicio"""
        from src.services.service_service import ServiceService
        from src.services.cliente_service import ClienteService
        
        service_service = ServiceService()
        cliente_service = ClienteService()
        
        service = service_service.obtener_service(cod_service)
        if not service:
            return redirect(url_for('services_page'))
        
        clientes = cliente_service.obtener_todos()
        
        return render_template('editar_service.html',
            service=service,
            clientes=clientes
        )
    
    # =====================
    # MANEJO DE ERRORES
    # =====================
    
    @app.errorhandler(404)
    def not_found(error):
        """Maneja errores 404"""
        if request.path.startswith('/api/'):
            return jsonify({
                'success': False,
                'message': 'Recurso no encontrado'
            }), 404
        return render_template('index.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Maneja errores internos"""
        logger.error(f"Error interno: {error}")
        db.session.rollback()
        if request.path.startswith('/api/'):
            return jsonify({
                'success': False,
                'message': 'Error interno del servidor'
            }), 500
        return render_template('index.html'), 500
    
    # =====================
    # API INFO
    # =====================
    
    @app.route('/api')
    def api_info():
        """Información de la API"""
        return jsonify({
            'nombre': 'ServiceAdmin API',
            'version': '1.0.0',
            'descripcion': 'API para gestión de servicios técnicos',
            'endpoints': {
                'clientes': '/api/clientes',
                'services': '/api/services',
                'presupuestos': '/api/presupuestos'
            }
        })
    
    @app.route('/api/health')
    def health():
        """Health check"""
        return jsonify({
            'status': 'healthy',
            'database': 'connected'
        })
    
    logger.info("Aplicación ServiceAdmin configurada correctamente")
    return app


def init_database():
    """Inicializa la base de datos con datos de ejemplo"""
    app = create_app()
    
    with app.app_context():
        from src.models.cliente import Cliente
        from src.models.service import Service
        
        # Verificar si ya hay datos
        if Cliente.query.count() > 0:
            logger.info("Base de datos ya inicializada")
            return
        
        # Crear clientes de ejemplo
        clientes_demo = [
            Cliente(nombre="Juan Pérez", direccion="Av. Siempre Viva 123", 
                   tel="1155556666", email="juan.perez@email.com"),
            Cliente(nombre="María García", direccion="Calle Falsa 456",
                   tel="1177778888", email="maria.garcia@email.com"),
            Cliente(nombre="Carlos López", direccion="Boulevard Norte 789",
                   tel="1199990000", email="carlos.lopez@email.com")
        ]
        
        for cliente in clientes_demo:
            db.session.add(cliente)
        
        db.session.commit()
        logger.info(f"Creados {len(clientes_demo)} clientes de ejemplo")
        
        # Crear servicios de ejemplo
        services_demo = [
            Service(codCliente=1, nomProducto="Notebook HP", 
                   modelo="Pavilion 15", descripFalla="No enciende"),
            Service(codCliente=1, nomProducto="Impresora Epson",
                   modelo="L3150", descripFalla="Atascos de papel"),
            Service(codCliente=2, nomProducto="Monitor Samsung",
                   modelo="24 pulgadas", descripFalla="Líneas en pantalla")
        ]
        
        for service in services_demo:
            db.session.add(service)
        
        db.session.commit()
        logger.info(f"Creados {len(services_demo)} servicios de ejemplo")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'init-db':
        logger.info("Ejecutando inicialización de base de datos...")
        init_database()
    else:
        app = create_app()
        app.run(
            debug=settings.app.debug,
            host=settings.app.host,
            port=settings.app.port
        )
