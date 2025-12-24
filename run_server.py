"""Script para ejecutar el servidor ServiceAdmin"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__':
    try:
        from src.main import create_app, init_database
        from src.config.settings import settings
        
        # Verificar si se requiere inicialización
        if len(sys.argv) > 1 and sys.argv[1] == 'init-db':
            print("Inicializando base de datos...")
            init_database()
            print("Base de datos inicializada con datos de ejemplo")
            sys.exit(0)
        
        print("Creando aplicación...")
        app = create_app()
        
        print(f"\n{'='*60}")
        print("--- ServiceAdmin v1.0 ---")
        print(f"Servidor iniciando en http://{settings.app.host}:{settings.app.port}")
        print(f"   Modo debug: {'Activado' if settings.app.debug else 'Desactivado'}")
        print(f"{'='*60}\n")
        
        # En desarrollo usar servidor Flask
        if settings.app.debug:
            app.run(
                host=settings.app.host,
                port=settings.app.port,
                debug=True
            )
        else:
            # En producción usar waitress
            try:
                from waitress import serve
                print("Usando servidor Waitress (producción)")
                serve(
                    app,
                    host=settings.app.host,
                    port=settings.app.port,
                    threads=4
                )
            except ImportError:
                print("Waitress no instalado, usando servidor Flask")
                app.run(
                    host=settings.app.host,
                    port=settings.app.port,
                    debug=False
                )
                
    except KeyboardInterrupt:
        print("\n\n✋ Servidor detenido por el usuario")
    except Exception as e:
        print(f"\n❌ Error al iniciar el servidor: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
