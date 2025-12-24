"""Repositorio para la entidad Presupuesto"""
from typing import List, Optional
from src.repositories.base_repository import BaseRepository
from src.models.presupuesto import Presupuesto


class PresupuestoRepository(BaseRepository[Presupuesto]):
    """Repositorio para operaciones con Presupuestos"""
    
    def __init__(self):
        super().__init__(Presupuesto)
    
    def find_by_service(self, cod_service: int) -> Optional[Presupuesto]:
        """
        Encuentra el presupuesto de un servicio.
        
        Args:
            cod_service: Código del servicio
            
        Returns:
            El presupuesto si existe, None en caso contrario
        """
        return self.session.query(Presupuesto).filter_by(
            codService=cod_service
        ).first()
    
    def find_pendientes_aceptacion(self) -> List[Presupuesto]:
        """
        Encuentra presupuestos pendientes de aceptación.
        
        Returns:
            Lista de presupuestos no aceptados
        """
        return self.session.query(Presupuesto).filter_by(
            aceptado=False
        ).all()
    
    def find_aceptados(self) -> List[Presupuesto]:
        """
        Encuentra presupuestos aceptados.
        
        Returns:
            Lista de presupuestos aceptados
        """
        return self.session.query(Presupuesto).filter_by(
            aceptado=True
        ).all()
    
    def get_total_ganancias(self) -> int:
        """
        Calcula el total de ganancias de presupuestos aceptados.
        
        Returns:
            Suma total de ganancias
        """
        from sqlalchemy import func
        resultado = self.session.query(
            func.sum(Presupuesto.gananciaTotal)
        ).filter_by(aceptado=True).scalar()
        return resultado or 0
