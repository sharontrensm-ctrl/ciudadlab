"""
config.py — todas las constantes del proyecto en un solo lugar.
Nadie más define constantes. Todos los módulos importan desde aquí.
"""

# Paths
DB_PATH = "/tmp/ciudad_lab.db"

# Opciones de dominio
SECTORES = [
    "Movilidad urbana",
    "Seguridad ciudadana",
    "Medio ambiente",
    "Vivienda",
    "Espacio público",
    "Educación",
    "Salud",
    "Cultura y patrimonio",
    "Economía local",
    "Otro",
]

LOCALIDADES = [
    "Norte",
    "Centro histórico",
    "Sur",
    "Valle de los Chillos",
    "Tumbaco",
    "Calderón",
    "La Delicia",
    "Otro",
]

PERFILES = [
    "Ciudadano/a",
    "Sociedad civil",
    "Academia",
    "Sector privado",
    "Gobierno",
]

TIPOS_APOYO = [
    "Financiamiento",
    "Co-ejecución",
    "Expertise técnico",
    "Redes / conexiones",
    "Visibilidad",
]

PRESUPUESTOS = [
    "< $10.000",
    "$10.000 – $50.000",
    "$50.000 – $200.000",
    "> $200.000",
    "Por definir",
]

# Estados de proyecto
ESTADO_ACTIVO = "activo"
ESTADO_INACTIVO = "inactivo"

# Límites de texto
MAX_NOMBRE = 120
MAX_DESCRIPCION = 600

# Navegación
PAGINAS = [
    "inicio",
    "proyectos",
    "nuevo_proyecto",
    "actores",
    "nuevo_actor",
    "matching",
]
