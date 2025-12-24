# ServiceAdmin

Sistema de gestión de taller de servicios técnicos desarrollado con Flask.

## 🚀 Inicio Rápido

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
python run_server.py

# Opcional: inicializar con datos de ejemplo
python run_server.py init-db
```

Acceder a: **http://localhost:5000**

## 📁 Estructura

```
ServiceAdmin/
├── run_server.py          # Punto de entrada
├── requirements.txt       # Dependencias
└── src/
    ├── main.py            # Factory Flask
    ├── config/            # Configuración
    ├── models/            # Modelos ORM
    ├── repositories/      # Capa de datos
    ├── services/          # Lógica de negocio
    ├── api/controllers/   # Endpoints REST
    ├── templates/         # Vistas HTML
    └── utils/             # Utilidades
```

## 🔧 Características

- **Gestión de Clientes**: CRUD completo
- **Servicios de Reparación**: Seguimiento de estados (Pendiente → Revisado → Reparado → Entregado)
- **Presupuestos**: Generación y aceptación
- **API REST**: Endpoints documentados en `/api`
- **Interfaz Web**: Diseño moderno con glassmorphism

## 🗄️ Base de Datos

Por defecto usa SQLite. Para MySQL, configurar variable de entorno:

```
DATABASE_URL=mysql+pymysql://user:pass@host/serviceAdmin
```

## 📝 API Endpoints

- `GET/POST /api/clientes` - Clientes
- `GET/POST /api/services` - Servicios
- `POST /api/services/{id}/revisar` - Marcar revisado
- `POST /api/services/{id}/reparar` - Marcar reparado
- `POST /api/services/{id}/entregar` - Marcar entregado
- `GET/POST /api/presupuestos` - Presupuestos

## 👤 Autor

**Lucas I. Borrat** - [LucasIBorrat](https://github.com/LucasIBorrat)
