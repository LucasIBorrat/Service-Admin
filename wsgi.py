"""WSGI entry point for production deployment (Render, Gunicorn, etc.)"""
from src.main import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
