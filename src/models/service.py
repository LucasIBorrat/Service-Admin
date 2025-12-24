"""Modelo de Service (Servicio de reparación)"""
from sqlalchemy import Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from datetime import date
from src.config.database import db


class Service(db.Model):
    """
    Representa un servicio de reparación.
    
    Contiene información del producto a reparar, su estado,
    y puede tener un presupuesto asociado.
    """
    __tablename__ = 'services'
    
    codService: Mapped[int] = mapped_column(Integer, primary_key=True)
    codCliente: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('clientes.codCliente'),
        nullable=False
    )
    fecha: Mapped[date] = mapped_column(Date, nullable=False, default=date.today)
    nomProducto: Mapped[str] = mapped_column(String(50), nullable=False)
    modelo: Mapped[str] = mapped_column(String(50), nullable=True)
    descrip: Mapped[str] = mapped_column(String(100), nullable=True)
    descripFalla: Mapped[str] = mapped_column(String(100), nullable=True)
    revisado: Mapped[bool] = mapped_column(Boolean, default=False)
    repuesto: Mapped[str] = mapped_column(String(80), nullable=True)
    costoRepuesto: Mapped[int] = mapped_column(Integer, default=0)
    reparado: Mapped[bool] = mapped_column(Boolean, default=False)
    entregado: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Relaciones
    cliente: Mapped["Cliente"] = relationship(
        "Cliente",
        back_populates="services"
    )
    presupuesto: Mapped[Optional["Presupuesto"]] = relationship(
        "Presupuesto",
        back_populates="service",
        uselist=False,
        cascade="all, delete-orphan"
    )
    repuestos: Mapped[List["Repuesto"]] = relationship(
        "Repuesto",
        back_populates="service",
        cascade="all, delete-orphan"
    )
    
    def __init__(self, codCliente: int, nomProducto: str, 
                 modelo: str = None, descrip: str = None, 
                 descripFalla: str = None, codService: int = None):
        """
        Inicializa un nuevo Service.
        
        Args:
            codCliente: Código del cliente asociado
            nomProducto: Nombre del producto a reparar
            modelo: Modelo del producto
            descrip: Descripción del producto
            descripFalla: Descripción de la falla
            codService: Código único (opcional)
        """
        if codService:
            self.codService = codService
        self.codCliente = codCliente
        self.nomProducto = nomProducto
        self.modelo = modelo
        self.descrip = descrip
        self.descripFalla = descripFalla
        self.fecha = date.today()
        self.revisado = False
        self.reparado = False
        self.entregado = False
        self.costoRepuesto = 0
    
    @property
    def estado(self) -> str:
        """Retorna el estado actual del servicio"""
        if self.entregado:
            return "Entregado"
        elif self.reparado:
            return "Reparado"
        elif self.revisado:
            return "Revisado"
        else:
            return "Pendiente"
    
    @property
    def estado_badge_class(self) -> str:
        """Retorna la clase CSS para el badge de estado"""
        estados = {
            "Entregado": "badge-success",
            "Reparado": "badge-info",
            "Revisado": "badge-warning",
            "Pendiente": "badge-secondary"
        }
        return estados.get(self.estado, "badge-secondary")
    
    @property
    def total_costo_repuestos(self) -> int:
        """Calcula el costo total de todos los repuestos"""
        return sum(r.costo for r in self.repuestos)
    
    def marcar_revisado(self, repuesto: str = None, costoRepuesto: int = 0) -> None:
        """Marca el servicio como revisado"""
        self.revisado = True
        if repuesto:
            self.repuesto = repuesto
            self.costoRepuesto = costoRepuesto
    
    def marcar_reparado(self) -> None:
        """Marca el servicio como reparado"""
        if not self.revisado:
            raise ValueError("El servicio debe estar revisado antes de marcarlo como reparado")
        self.reparado = True
    
    def marcar_entregado(self) -> None:
        """Marca el servicio como entregado"""
        if not self.reparado:
            raise ValueError("El servicio debe estar reparado antes de marcarlo como entregado")
        self.entregado = True
    
    def to_dict(self) -> dict:
        """Convierte el servicio a diccionario"""
        return {
            'codService': self.codService,
            'codCliente': self.codCliente,
            'cliente_nombre': self.cliente.nombre if self.cliente else None,
            'fecha': self.fecha.isoformat() if self.fecha else None,
            'nomProducto': self.nomProducto,
            'modelo': self.modelo,
            'descrip': self.descrip,
            'descripFalla': self.descripFalla,
            'revisado': self.revisado,
            'repuesto': self.repuesto,
            'costoRepuesto': self.costoRepuesto,
            'reparado': self.reparado,
            'entregado': self.entregado,
            'estado': self.estado,
            'tiene_presupuesto': self.presupuesto is not None,
            'repuestos_lista': [r.to_dict() for r in self.repuestos],
            'total_costo_repuestos': self.total_costo_repuestos
        }
    
    def __repr__(self) -> str:
        return f"<Service(cod={self.codService}, producto='{self.nomProducto}', estado='{self.estado}')>"
