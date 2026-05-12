# ciudadlab

quito_ciudad_lab/
├── app.py                  # Entry point · router de páginas · principio: claridad
├── config.py               # Todas las constantes · principio: determinismo
├── runtime.txt             # python-3.11 · constraint Cloud
├── requirements.txt        # versiones pineadas · principio: resiliencia
├── data/
│   ├── __init__.py
│   ├── models.py           # Schema SQLite + init_db · principio: separación
│   └── repository.py       # Queries CRUD · principio: separación + resiliencia
├── logic/
│   ├── __init__.py
│   ├── matching.py         # Motor matching puro · principio: determinismo
│   └── validators.py       # Validación de inputs · principio: determinismo
└── ui/
    ├── __init__.py
    ├── inicio.py           # Página métricas · principio: separación
    ├── proyectos.py        # Listado + filtros · principio: separación
    ├── nuevo_proyecto.py   # Formulario registro · principio: separación
    ├── actores.py          # Directorio actores · principio: separación
    ├── nuevo_actor.py      # Formulario registro · principio: separación
    └── matching_ui.py      # UI motor matching · principio: separación
