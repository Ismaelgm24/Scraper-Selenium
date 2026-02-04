# Scraper simple de hoteles (Málaga)

Este proyecto usa Selenium para extraer información de hoteles desde la web de Turismo de Málaga y guarda los resultados en un CSV dentro de la carpeta de salidas.

## Qué hace

- Abre Chrome con Selenium.
- Acepta el banner de cookies (si aparece).
- Recorre la paginación de resultados.
- Extrae: nombre, enlace, pueblo, estrellas, imagen y descripción.
- Guarda todo en un CSV con timestamp.

## Requisitos

- Windows con Google Chrome instalado.
- Python 3.9+.
- Dependencias de Python:
  - selenium
  - webdriver-manager

## Instalación

```bash
pip install selenium webdriver-manager
```

## Uso

Ejecuta el script:

```bash
python scraper_simple.py
```

Los resultados se guardan en:

- [salidas/csv](salidas/csv)

El archivo generado tendrá un nombre como `hoteles_YYYYMMDD_HHMMSS.csv`.

## Configuración rápida

La URL objetivo está en [scraper_simple.py](scraper_simple.py). Si necesitas cambiarla, edita la variable `url`.

## Estructura del proyecto

```
.
├── scraper_simple.py
└── salidas
    └── csv
```

## Notas

- El script hace esperas con `time.sleep` para dar tiempo a que cargue la página.
- Si el botón de cookies no aparece, el script continúa.

## Licencia

MIT
