"""Modelo de Cliente"""
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from src.config.database import db


class Cliente(db.Model):
    """
    Representa un cliente del sistema.
    
    Un cliente puede tener múltiples servicios de reparación asociados.
    """
    __tablename__ = 'clientes'
    
    codCliente: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(90), nullable=False)
    direccion: Mapped[str] = mapped_column(String(50), nullable=True)
    tel: Mapped[str] = mapped_column(String(15), nullable=True)
    email: Mapped[str] = mapped_column(String(50), nullable=True)
    
    # Relaciones
    services: Mapped[List["Service"]] = relationship(
        "Service",
        back_populates="cliente",
        cascade="all, delete-orphan"
    )
    
    def __init__(self, nombre: str, direccion: str = None, 
                 tel: str = None, email: str = None, codCliente: int = None):
        """
        Inicializa un nuevo Cliente.
        
        Args:
            nombre: Nombre completo del cliente
            direccion: Dirección del cliente
            tel: Teléfono de contacto
            email: Email de contacto
            codCliente: Código único (opcional, se genera automáticamente)
        """
        if codCliente:
            self.codCliente = codCliente
        self.nombre = nombre
        self.direccion = direccion
        self.tel = tel
        self.email = email
    
    @property
    def total_services(self) -> int:
        """Retorna el total de servicios del cliente"""
        return len(self.services)
    
    @property
    def services_pendientes(self) -> int:
        """Retorna la cantidad de servicios no entregados"""
        return len([s for s in self.services if not s.entregado])
    
    def to_dict(self) -> dict:
        """Convierte el cliente a diccionario"""
        return {
            'codCliente': self.codCliente,
            'nombre': self.nombre,
            'direccion': self.direccion,
            'tel': self.tel,
            'email': self.email,
            'total_services': self.total_services,
            'services_pendientes': self.services_pendientes
        }
    
    def __repr__(self) -> str:
        return f"<Cliente(cod={self.codCliente}, nombre='{self.nombre}')>"
