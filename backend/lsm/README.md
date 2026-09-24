# LSM — Lenguaje de Señas Mexicana

Scripts para capturar dataset, entrenar y desplegar el clasificador de señas.

## Por qué existe un venv separado

`mediapipe` solo tiene wheels precompilados para **Python ≤ 3.12**.
El backend principal usa Python 3.14, por eso los scripts LSM tienen su propio
entorno en `lsm/venv312/` (Python 3.12).

## Setup (solo la primera vez)

```bash
# Desde la raíz del repositorio:

# 1. Instalar Python 3.12 con pyenv (si no está instalado)
pyenv install 3.12.10

# 2. Crear el venv (ya hecho — incluido en el repo como directorio ignorado)
~/.pyenv/versions/3.12.10/bin/python3.12 -m venv backend/lsm/venv312

# 3. Instalar dependencias LSM
backend/lsm/venv312/bin/pip install \
  "mediapipe==1.0.1" \
  "opencv-python>=4.10.0" \
  "numpy>=1.26.0" \
  "python-dotenv>=1.0.1" \
  "ibm-watsonx-ai>=1.1.0" \
  "tensorflow>=2.16.0" \
  "scikit-learn>=1.4.0"
```

## Uso

```bash
# Siempre desde la raíz del repositorio:

# Activar el venv de Python 3.12
source backend/lsm/venv312/bin/activate

# Capturar dataset (todas las señas: hola, gracias, ayuda, si, no)
python backend/lsm/lsm_capture.py

# Capturar solo una seña
python backend/lsm/lsm_capture.py --sena hola

# Entrenar el clasificador (requiere dataset capturado)
python backend/lsm/train_lsm.py

# Entrenar sin desplegar en WML
python backend/lsm/train_lsm.py --solo-entrenar
```

## Controles durante la captura

| Tecla   | Acción                        |
|---------|-------------------------------|
| `ESPACIO` | Iniciar / pausar grabación  |
| `N`     | Pasar a la siguiente seña     |
| `Q`     | Salir                         |

## Archivos generados

| Archivo                     | Descripción                                  |
|-----------------------------|----------------------------------------------|
| `lsm/dataset/keypoints.csv` | Dataset: 63 keypoints por fila + etiqueta    |
| `lsm/models/hand_landmarker.task` | Modelo MediaPipe (descarga automática ~8MB) |
| `lsm/modelo_lsm/`           | Modelo Keras entrenado (SavedModel)          |
