"""Servicio para la gestión de Presupuestos"""
from typing import Dict, Any, List, Optional
from src.models.presupuesto import Presupuesto
from src.repositories.presupuesto_repository import PresupuestoRepository
from src.repositories.service_repository import ServiceRepository
from src.config.database import db


class PresupuestoService:
    """
    Servicio que maneja la lógica de negocio para Presupuestos.
    """
    
    def __init__(self):
        self.presupuesto_repository = PresupuestoRepository()
        self.service_repository = ServiceRepository()
    
    def crear_presupuesto(self, data: Dict[str, Any]) -> Presupuesto:
        """
        Crea un nuevo presupuesto para un servicio.
        
        Args:
            data: Diccionario con los datos del presupuesto
            
        Returns:
            El presupuesto creado
            
        Raises:
            ValueError: Si el servicio no existe o ya tiene presupuesto
        """
        cod_service = data.get('codService')
        if not cod_service:
            raise ValueError("Debe especificar un servicio")
        
        # Validar que el servicio exista
        service = self.service_repository.get_by_id(cod_service)
        if not service:
            raise ValueError(f"No existe servicio con código {cod_service}")
        
        # Validar que no tenga presupuesto ya
        existing = self.presupuesto_repository.find_by_service(cod_service)
        if existing:
            raise ValueError("El servicio ya tiene un presupuesto asociado")
        
        # Usar costo de repuesto del servicio si no se especifica
        costo = data.get('costo', service.costoRepuesto)
        mano_de_obra = data.get('manoDeObra', 0)
        
        presupuesto = Presupuesto(
            codService=cod_service,
            costo=int(costo),
            manoDeObra=int(mano_de_obra)
        )
        
        return self.presupuesto_repository.create(presupuesto)
    
    def actualizar_presupuesto(self, cod_presupuesto: int, 
                                data: Dict[str, Any]) -> Presupuesto:
        """
        Actualiza un presupuesto existente.
        
        Args:
            cod_presupuesto: Código del presupuesto
            data: Diccionario con los datos a actualizar
            
        Returns:
            El presupuesto actualizado
        """
        presupuesto = self.presupuesto_repository.get_by_id(cod_presupuesto)
        if not presupuesto:
            raise ValueError(f"No existe presupuesto con código {cod_presupuesto}")
        
        # No permitir actualizar si ya fue aceptado
        if presupuesto.aceptado:
            raise ValueError("No se puede modificar un presupuesto ya aceptado")
        
        costo = data.get('costo')
        mano_de_obra = data.get('manoDeObra')
        
        presupuesto.actualizar_costos(
            costo=int(costo) if costo is not None else None,
            manoDeObra=int(mano_de_obra) if mano_de_obra is not None else None
        )
        
        db.session.commit()
        return presupuesto
    
    def aceptar_presupuesto(self, cod_presupuesto: int) -> Presupuesto:
        """
        Marca un presupuesto como aceptado.
        
        Args:
            cod_presupuesto: Código del presupuesto
            
        Returns:
            El presupuesto actualizado
        """
        presupuesto = self.presupuesto_repository.get_by_id(cod_presupuesto)
        if not presupuesto:
            raise ValueError(f"No existe presupuesto con código {cod_presupuesto}")
        
        presupuesto.aceptar()
        db.session.commit()
        return presupuesto
    
    def rechazar_presupuesto(self, cod_presupuesto: int) -> Presupuesto:
        """
        Marca un presupuesto como rechazado.
        
        Args:
            cod_presupuesto: Código del presupuesto
            
        Returns:
            El presupuesto actualizado
        """
        presupuesto = self.presupuesto_repository.get_by_id(cod_presupuesto)
        if not presupuesto:
            raise ValueError(f"No existe presupuesto con código {cod_presupuesto}")
        
        presupuesto.rechazar()
        db.session.commit()
        return presupuesto
    
    def eliminar_presupuesto(self, cod_presupuesto: int) -> bool:
        """
        Elimina un presupuesto.
        
        Args:
            cod_presupuesto: Código del presupuesto
            
        Returns:
            True si se eliminó correctamente
        """
        presupuesto = self.presupuesto_repository.get_by_id(cod_presupuesto)
        if not presupuesto:
            raise ValueError(f"No existe presupuesto con código {cod_presupuesto}")
        
        return self.presupuesto_repository.delete(cod_presupuesto)
    
    def obtener_presupuesto(self, cod_presupuesto: int) -> Optional[Presupuesto]:
        """Obtiene un presupuesto por su código"""
        return self.presupuesto_repository.get_by_id(cod_presupuesto)
    
    def obtener_por_service(self, cod_service: int) -> Optional[Presupuesto]:
        """Obtiene el presupuesto de un servicio"""
        return self.presupuesto_repository.find_by_service(cod_service)
    
    def obtener_todos(self) -> List[Presupuesto]:
        """Obtiene todos los presupuestos"""
        return self.presupuesto_repository.get_all()
    
    def obtener_pendientes(self) -> List[Presupuesto]:
        """Obtiene presupuestos pendientes de aceptación"""
        return self.presupuesto_repository.find_pendientes_aceptacion()
    
    def obtener_total_ganancias(self) -> int:
        """Obtiene el total de ganancias de presupuestos aceptados"""
        return self.presupuesto_repository.get_total_ganancias()
