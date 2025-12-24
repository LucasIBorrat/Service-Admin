"""Modelo de Repuesto (Spare Part)"""
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.config.database import db


class Repuesto(db.Model):
    """
    Representa un repuesto utilizado en un servicio de reparación.
    
    Un servicio puede tener múltiples repuestos asociados.
    """
    __tablename__ = 'repuestos'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    codService: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('services.codService'),
        nullable=False
    )
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    costo: Mapped[int] = mapped_column(Integer, default=0)
    
    # Relación
    service: Mapped["Service"] = relationship(
        "Service",
        back_populates="repuestos"
    )
    
    def __init__(self, codService: int, nombre: str, costo: int = 0):
        """
        Inicializa un nuevo Repuesto.
        
        Args:
            codService: Código del servicio asociado
            nombre: Nombre o descripción del repuesto
            costo: Costo del repuesto
        """
        self.codService = codService
        self.nombre = nombre
        self.costo = costo
    
    def to_dict(self) -> dict:
        """Convierte el repuesto a diccionario"""
        return {
            'id': self.id,
            'codService': self.codService,
            'nombre': self.nombre,
            'costo': self.costo
        }
    
    def __repr__(self) -> str:
        return f"<Repuesto(id={self.id}, nombre='{self.nombre}', costo=${self.costo})>"
