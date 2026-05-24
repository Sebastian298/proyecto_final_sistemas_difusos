# Proyecto Final - Sistemas Difusos

Proyecto en Python para el curso de sistemas difusos.

## Requisitos

- Python 3.10 o superior

## Instalación

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
```

## Uso

```bash
sistemas-difusos
```

O directamente:

```bash
python -m sistemas_difusos.main
```

## Pruebas

```bash
pytest
```

## Estructura del proyecto

```
proyecto_final_sistemas_difusos/
├── src/
│   └── sistemas_difusos/   # Código fuente del paquete
├── tests/                  # Pruebas con pytest
├── pyproject.toml          # Configuración y dependencias
└── README.md
```
