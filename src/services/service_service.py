"""Servicio para la gestión de Services (Reparaciones)"""
from typing import Dict, Any, List, Optional
from src.models.service import Service
from src.repositories.service_repository import ServiceRepository
from src.repositories.cliente_repository import ClienteRepository
from src.config.database import db


class ServiceService:
    """
    Servicio que maneja la lógica de negocio para Services de reparación.
    """
    
    def __init__(self):
        self.service_repository = ServiceRepository()
        self.cliente_repository = ClienteRepository()
    
    def crear_service(self, data: Dict[str, Any]) -> Service:
        """
        Crea un nuevo servicio de reparación.
        
        Args:
            data: Diccionario con los datos del servicio
            
        Returns:
            El servicio creado
            
        Raises:
            ValueError: Si el cliente no existe o faltan datos requeridos
        """
        # Validar campos requeridos
        if not data.get('codCliente'):
            raise ValueError("Debe especificar un cliente")
        if not data.get('nomProducto'):
            raise ValueError("Debe especificar el nombre del producto")
        
        # Validar que el cliente exista
        cliente = self.cliente_repository.get_by_id(data['codCliente'])
        if not cliente:
            raise ValueError(f"No existe cliente con código {data['codCliente']}")
        
        # Crear el servicio
        service = Service(
            codCliente=data['codCliente'],
            nomProducto=data['nomProducto'],
            modelo=data.get('modelo'),
            descrip=data.get('descrip'),
            descripFalla=data.get('descripFalla')
        )
        
        return self.service_repository.create(service)
    
    def actualizar_service(self, cod_service: int, data: Dict[str, Any]) -> Service:
        """
        Actualiza un servicio existente.
        
        Args:
            cod_service: Código del servicio a actualizar
            data: Diccionario con los datos a actualizar
            
        Returns:
            El servicio actualizado
        """
        service = self.service_repository.get_by_id(cod_service)
        if not service:
            raise ValueError(f"No existe servicio con código {cod_service}")
        
        # No permitir editar si ya está entregado
        if service.entregado:
            raise ValueError("No se puede editar un servicio ya entregado")
        
        # Actualizar campos básicos
        if 'nomProducto' in data:
            service.nomProducto = data['nomProducto']
        if 'modelo' in data:
            service.modelo = data['modelo']
        if 'descrip' in data:
            service.descrip = data['descrip']
        if 'descripFalla' in data:
            service.descripFalla = data['descripFalla']
        if 'repuesto' in data:
            service.repuesto = data['repuesto']
        if 'costoRepuesto' in data:
            service.costoRepuesto = int(data['costoRepuesto'])
        
        db.session.commit()
        return service
    
    def marcar_revisado(self, cod_service: int, 
                        repuesto: str = None, 
                        costo_repuesto: int = 0) -> Service:
        """
        Marca un servicio como revisado.
        
        Args:
            cod_service: Código del servicio
            repuesto: Repuestos necesarios
            costo_repuesto: Costo de los repuestos
            
        Returns:
            El servicio actualizado
        """
        service = self.service_repository.get_by_id(cod_service)
        if not service:
            raise ValueError(f"No existe servicio con código {cod_service}")
        
        service.marcar_revisado(repuesto, costo_repuesto)
        db.session.commit()
        return service
    
    def marcar_reparado(self, cod_service: int) -> Service:
        """
        Marca un servicio como reparado.
        
        Args:
            cod_service: Código del servicio
            
        Returns:
            El servicio actualizado
        """
        service = self.service_repository.get_by_id(cod_service)
        if not service:
            raise ValueError(f"No existe servicio con código {cod_service}")
        
        service.marcar_reparado()
        db.session.commit()
        return service
    
    def marcar_entregado(self, cod_service: int) -> Service:
        """
        Marca un servicio como entregado.
        
        Args:
            cod_service: Código del servicio
            
        Returns:
            El servicio actualizado
        """
        service = self.service_repository.get_by_id(cod_service)
        if not service:
            raise ValueError(f"No existe servicio con código {cod_service}")
        
        service.marcar_entregado()
        db.session.commit()
        return service
    
    def eliminar_service(self, cod_service: int) -> bool:
        """
        Elimina un servicio.
        
        Args:
            cod_service: Código del servicio
            
        Returns:
            True si se eliminó correctamente
        """
        service = self.service_repository.get_by_id(cod_service)
        if not service:
            raise ValueError(f"No existe servicio con código {cod_service}")
        
        return self.service_repository.delete(cod_service)
    
    def obtener_service(self, cod_service: int) -> Optional[Service]:
        """Obtiene un servicio por su código"""
        return self.service_repository.get_by_id(cod_service)
    
    def obtener_todos(self) -> List[Service]:
        """Obtiene todos los servicios"""
        return self.service_repository.get_all()
    
    def obtener_por_cliente(self, cod_cliente: int) -> List[Service]:
        """Obtiene servicios de un cliente"""
        return self.service_repository.find_by_cliente(cod_cliente)
    
    def obtener_pendientes(self) -> List[Service]:
        """Obtiene servicios pendientes de revisión"""
        return self.service_repository.find_pendientes()
    
    def obtener_listos_para_entregar(self) -> List[Service]:
        """Obtiene servicios reparados pendientes de entrega"""
        return self.service_repository.find_reparados_sin_entregar()
    
    def obtener_estadisticas(self) -> dict:
        """Obtiene estadísticas de servicios"""
        return self.service_repository.count_by_estado()
