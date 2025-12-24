"""Conversión de números a texto en español"""

UNIDADES = [
    '', 'uno', 'dos', 'tres', 'cuatro', 'cinco', 'seis', 'siete', 'ocho', 'nueve',
    'diez', 'once', 'doce', 'trece', 'catorce', 'quince', 'dieciséis', 'diecisiete',
    'dieciocho', 'diecinueve', 'veinte', 'veintiuno', 'veintidós', 'veintitrés',
    'veinticuatro', 'veinticinco', 'veintiséis', 'veintisiete', 'veintiocho', 'veintinueve'
]

DECENAS = [
    '', '', '', 'treinta', 'cuarenta', 'cincuenta', 
    'sesenta', 'setenta', 'ochenta', 'noventa'
]

CENTENAS = [
    '', 'ciento', 'doscientos', 'trescientos', 'cuatrocientos', 'quinientos',
    'seiscientos', 'setecientos', 'ochocientos', 'novecientos'
]


def _unidades_a_texto(n: int) -> str:
    """Convierte un número del 0 al 99 a texto"""
    if n < 30:
        return UNIDADES[n]
    
    decena = n // 10
    unidad = n % 10
    
    if unidad == 0:
        return DECENAS[decena]
    else:
        return f"{DECENAS[decena]} y {UNIDADES[unidad]}"


def _centenas_a_texto(n: int) -> str:
    """Convierte un número del 0 al 999 a texto"""
    if n == 100:
        return 'cien'
    
    centena = n // 100
    resto = n % 100
    
    if centena == 0:
        return _unidades_a_texto(resto)
    elif resto == 0:
        return CENTENAS[centena]
    else:
        return f"{CENTENAS[centena]} {_unidades_a_texto(resto)}"


def numero_a_texto(n: int) -> str:
    """
    Convierte un número entero a su representación en texto en español.
    
    Útil para facturación donde se requiere mostrar montos en palabras.
    
    Args:
        n: Número entero a convertir (0 a 999,999,999)
        
    Returns:
        Representación en texto del número
        
    Examples:
        >>> numero_a_texto(123)
        'ciento veintitrés'
        >>> numero_a_texto(1500)
        'mil quinientos'
    """
    if n == 0:
        return 'cero'
    
    if n < 0:
        return f"menos {numero_a_texto(abs(n))}"
    
    if n < 1000:
        return _centenas_a_texto(n)
    
    if n < 1000000:
        miles = n // 1000
        resto = n % 1000
        
        if miles == 1:
            texto_miles = 'mil'
        else:
            texto_miles = f"{_centenas_a_texto(miles)} mil"
        
        if resto == 0:
            return texto_miles
        else:
            return f"{texto_miles} {_centenas_a_texto(resto)}"
    
    if n < 1000000000:
        millones = n // 1000000
        resto = n % 1000000
        
        if millones == 1:
            texto_millones = 'un millón'
        else:
            texto_millones = f"{_centenas_a_texto(millones)} millones"
        
        if resto == 0:
            return texto_millones
        else:
            return f"{texto_millones} {numero_a_texto(resto)}"
    
    return str(n)  # Números muy grandes se devuelven como string


def pesos_a_texto(monto: int) -> str:
    """
    Convierte un monto en pesos a texto para facturación.
    
    Args:
        monto: Monto en pesos
        
    Returns:
        Texto formateado para factura
        
    Example:
        >>> pesos_a_texto(1500)
        'Son pesos: mil quinientos'
    """
    return f"Son pesos: {numero_a_texto(monto)}"
