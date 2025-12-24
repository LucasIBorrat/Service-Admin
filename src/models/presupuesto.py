"""Modelo de Presupuesto"""
from sqlalchemy import Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.config.database import db


class Presupuesto(db.Model):
    """
    Representa un presupuesto asociado a un servicio de reparación.
    
    Incluye costos de repuestos, mano de obra y ganancia total.
    El cliente puede aceptar o rechazar el presupuesto.
    """
    __tablename__ = 'presupuestos'
    
    codPresupuesto: Mapped[int] = mapped_column(Integer, primary_key=True)
    codService: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('services.codService'),
        nullable=False,
        unique=True
    )
    costo: Mapped[int] = mapped_column(Integer, default=0)
    manoDeObra: Mapped[int] = mapped_column(Integer, default=0)
    gananciaTotal: Mapped[int] = mapped_column(Integer, default=0)
    aceptado: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Relaciones
    service: Mapped["Service"] = relationship(
        "Service",
        back_populates="presupuesto"
    )
    
    def __init__(self, codService: int, costo: int = 0, 
                 manoDeObra: int = 0, codPresupuesto: int = None):
        """
        Inicializa un nuevo Presupuesto.
        
        Args:
            codService: Código del servicio asociado
            costo: Costo de repuestos
            manoDeObra: Costo de mano de obra
            codPresupuesto: Código único (opcional)
        """
        if codPresupuesto:
            self.codPresupuesto = codPresupuesto
        self.codService = codService
        self.costo = costo
        self.manoDeObra = manoDeObra
        self.gananciaTotal = self._calcular_ganancia()
        self.aceptado = False
    
    def _calcular_ganancia(self) -> int:
        """Calcula la ganancia total (costo + mano de obra)"""
        return self.costo + self.manoDeObra
    
    def actualizar_costos(self, costo: int = None, manoDeObra: int = None) -> None:
        """Actualiza los costos y recalcula la ganancia"""
        if costo is not None:
            self.costo = costo
        if manoDeObra is not None:
            self.manoDeObra = manoDeObra
        self.gananciaTotal = self._calcular_ganancia()
    
    def aceptar(self) -> None:
        """Marca el presupuesto como aceptado"""
        self.aceptado = True
    
    def rechazar(self) -> None:
        """Marca el presupuesto como rechazado"""
        self.aceptado = False
    
    @property
    def estado(self) -> str:
        """Retorna el estado del presupuesto"""
        return "Aceptado" if self.aceptado else "Pendiente"
    
    @property
    def costo_repuestos_actual(self) -> int:
        """Obtiene el costo actual de repuestos directamente del service"""
        if self.service:
            return self.service.total_costo_repuestos
        return self.costo
    
    @property
    def total_actual(self) -> int:
        """Calcula el total usando el costo de repuestos actualizado"""
        return self.costo_repuestos_actual + self.manoDeObra
    
    def to_dict(self) -> dict:
        """Convierte el presupuesto a diccionario"""
        return {
            'codPresupuesto': self.codPresupuesto,
            'codService': self.codService,
            'costo': self.costo,
            'manoDeObra': self.manoDeObra,
            'gananciaTotal': self.gananciaTotal,
            'aceptado': self.aceptado,
            'estado': self.estado
        }
    
    def __repr__(self) -> str:
        return f"<Presupuesto(cod={self.codPresupuesto}, total=${self.gananciaTotal}, aceptado={self.aceptado})>"
