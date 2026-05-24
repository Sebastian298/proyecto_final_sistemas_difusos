# Proyecto Final - Sistemas Difusos

Control difuso Mamdani para un purificador de aire. El sistema ajusta la potencia del purificador segun la calidad del aire (AQI) y la ocupacion del espacio.

## Requisitos

- Python 3.10 o superior

## Instalacion

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

Los resultados se guardan en la carpeta `outputs/` del directorio actual:

- `pf_membresias_entradas.png` - Funciones de membresia de AQI y ocupacion
- `pf_membresias_salida.png` - Funciones de membresia de potencia
- `pf_superficie_control.png` - Superficie de control 3D
- `pf_comparacion_umbral_vs_difuso.png` - Comparacion con control por umbral
- `pf_validacion.txt` - Escenarios de validacion

## Pruebas

```bash
pytest
```

## Estructura del proyecto

```
proyecto_final_sistemas_difusos/
├── src/
│   └── sistemas_difusos/
│       ├── controller.py      # Controlador difuso del purificador
│       ├── membership.py      # Funciones de membresia y defuzzificacion
│       ├── visualization.py   # Generacion de graficas y validacion
│       └── main.py            # Punto de entrada
├── tests/
├── outputs/                   # Resultados generados (gitignored)
├── pyproject.toml
└── README.md
```

## Documentacion adicional

El reporte y la presentacion del proyecto estan en `proyecto_final_purificador_difuso/`.
