"""Servicio para la gestión de Clientes"""
from typing import Dict, Any, List, Optional
from src.models.cliente import Cliente
from src.repositories.cliente_repository import ClienteRepository


class ClienteService:
    """
    Servicio que maneja la lógica de negocio para Clientes.
    """
    
    def __init__(self):
        self.cliente_repository = ClienteRepository()
    
    def crear_cliente(self, data: Dict[str, Any]) -> Cliente:
        """
        Crea un nuevo cliente validando reglas de negocio.
        
        Args:
            data: Diccionario con los datos del cliente
            
        Returns:
            El cliente creado
            
        Raises:
            ValueError: Si el email ya está registrado
        """
        # Validar campos requeridos
        if not data.get('nombre'):
            raise ValueError("El nombre del cliente es requerido")
        
        # Validar unicidad de email si se proporciona
        email = data.get('email')
        if email:
            existing = self.cliente_repository.find_by_email(email)
            if existing:
                raise ValueError(f"Ya existe un cliente con el email {email}")
        
        # Crear el cliente
        cliente = Cliente(
            nombre=data['nombre'],
            direccion=data.get('direccion'),
            tel=data.get('tel'),
            email=email
        )
        
        return self.cliente_repository.create(cliente)
    
    def actualizar_cliente(self, cod_cliente: int, data: Dict[str, Any]) -> Cliente:
        """
        Actualiza un cliente existente.
        
        Args:
            cod_cliente: Código del cliente a actualizar
            data: Diccionario con los datos a actualizar
            
        Returns:
            El cliente actualizado
            
        Raises:
            ValueError: Si el cliente no existe o el email ya está en uso
        """
        cliente = self.cliente_repository.get_by_id(cod_cliente)
        if not cliente:
            raise ValueError(f"No existe cliente con código {cod_cliente}")
        
        # Validar email si se está cambiando
        new_email = data.get('email')
        if new_email and new_email != cliente.email:
            existing = self.cliente_repository.find_by_email(new_email)
            if existing:
                raise ValueError(f"Ya existe un cliente con el email {new_email}")
            cliente.email = new_email
        
        # Actualizar campos
        if 'nombre' in data:
            cliente.nombre = data['nombre']
        if 'direccion' in data:
            cliente.direccion = data['direccion']
        if 'tel' in data:
            cliente.tel = data['tel']
        
        return self.cliente_repository.save(cliente)
    
    def eliminar_cliente(self, cod_cliente: int) -> bool:
        """
        Elimina un cliente.
        
        Args:
            cod_cliente: Código del cliente a eliminar
            
        Returns:
            True si se eliminó correctamente
            
        Raises:
            ValueError: Si el cliente tiene servicios pendientes
        """
        cliente = self.cliente_repository.get_by_id(cod_cliente)
        if not cliente:
            raise ValueError(f"No existe cliente con código {cod_cliente}")
        
        # Verificar si tiene servicios pendientes
        if cliente.services_pendientes > 0:
            raise ValueError(
                f"No se puede eliminar el cliente porque tiene "
                f"{cliente.services_pendientes} servicios pendientes"
            )
        
        return self.cliente_repository.delete(cod_cliente)
    
    def obtener_cliente(self, cod_cliente: int) -> Optional[Cliente]:
        """Obtiene un cliente por su código"""
        return self.cliente_repository.get_by_id(cod_cliente)
    
    def obtener_todos(self) -> List[Cliente]:
        """Obtiene todos los clientes"""
        return self.cliente_repository.get_all()
    
    def buscar_por_nombre(self, nombre: str) -> List[Cliente]:
        """Busca clientes por nombre"""
        return self.cliente_repository.find_by_nombre(nombre)
