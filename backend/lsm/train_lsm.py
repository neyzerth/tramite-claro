"""
train_lsm.py — Entrenamiento y despliegue del clasificador LSM en Watson Studio.

Carga el dataset de keypoints, entrena un modelo TensorFlow/Keras y
lo despliega en Watson Machine Learning para inferencia en tiempo real.

Ejecutar en Watson Studio (notebook) o localmente con las credenciales
de WML configuradas en el entorno.
"""
import os
import json
import numpy as np
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# ─────────────────────────────────────────────────────────────────────────────
# Parámetros de entrenamiento
# ─────────────────────────────────────────────────────────────────────────────

DATASET_CSV = os.path.join(os.path.dirname(__file__), "dataset", "keypoints.csv")
MODEL_DIR = os.path.join(os.path.dirname(__file__), "modelo_lsm")
EPOCHS = 50
BATCH_SIZE = 32
TEST_SPLIT = 0.2
SEED = 42


# ─────────────────────────────────────────────────────────────────────────────
# 1. Cargar y preparar datos
# ─────────────────────────────────────────────────────────────────────────────

def cargar_datos(csv_path: str):
    """
    Carga el CSV de keypoints y devuelve X (features) e y (labels codificados).

    Returns:
        X        : ndarray de shape (n_muestras, 63)
        y        : ndarray de enteros codificados
        clases   : lista de nombres de señas en el orden del encoder
    """
    df = pd.read_csv(csv_path)
    clases = sorted(df["sena"].unique().tolist())
    label_map = {c: i for i, c in enumerate(clases)}

    X = df.drop(columns=["sena"]).values.astype(np.float32)
    y = df["sena"].map(label_map).values.astype(np.int32)

    # Normalizar entre 0 y 1 (los keypoints ya están en [0,1] pero por mano distinta
    # puede haber variación; normalizar por muestra ayuda)
    X_min = X.min(axis=1, keepdims=True)
    X_max = X.max(axis=1, keepdims=True)
    rango = np.where(X_max - X_min == 0, 1, X_max - X_min)
    X = (X - X_min) / rango

    return X, y, clases


# ─────────────────────────────────────────────────────────────────────────────
# 2. Construir el modelo
# ─────────────────────────────────────────────────────────────────────────────

def construir_modelo(n_clases: int, n_features: int = 63):
    """
    Construye el clasificador Dense para keypoints de mano.

    Arquitectura: Dense(128, relu) → Dropout(0.3) → Dense(64, relu) → Dense(n_clases, softmax)
    """
    import tensorflow as tf  # Importación tardía para evitar carga en módulos que no lo usan

    modelo = tf.keras.Sequential(
        [
            tf.keras.layers.Input(shape=(n_features,)),
            tf.keras.layers.Dense(128, activation="relu"),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(64, activation="relu"),
            tf.keras.layers.Dense(n_clases, activation="softmax"),
        ],
        name="clasificador_lsm",
    )
    modelo.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return modelo


# ─────────────────────────────────────────────────────────────────────────────
# 3. Entrenamiento
# ─────────────────────────────────────────────────────────────────────────────

def entrenar(csv_path: str = DATASET_CSV, model_dir: str = MODEL_DIR):
    """
    Carga datos, entrena el modelo, evalúa y guarda en formato SavedModel.

    Returns:
        (modelo entrenado, lista de clases, historial de entrenamiento)
    """
    import tensorflow as tf
    from sklearn.model_selection import train_test_split  # scikit-learn para el split

    print("📂 Cargando dataset...")
    X, y, clases = cargar_datos(csv_path)
    print(f"   {len(X)} muestras · {len(clases)} clases: {clases}")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SPLIT, random_state=SEED, stratify=y
    )

    print("🏗️  Construyendo modelo...")
    modelo = construir_modelo(n_clases=len(clases))
    modelo.summary()

    print(f"🚀 Entrenando por {EPOCHS} épocas...")
    historial = modelo.fit(
        X_train, y_train,
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        validation_data=(X_test, y_test),
        verbose=1,
    )

    loss, acc = modelo.evaluate(X_test, y_test, verbose=0)
    print(f"✅ Evaluación final — Loss: {loss:.4f} | Accuracy: {acc:.4f}")

    # Guardar el modelo en formato SavedModel
    os.makedirs(model_dir, exist_ok=True)
    modelo.save(model_dir)

    # Guardar el mapeo de clases para uso en predicción
    clases_path = os.path.join(model_dir, "clases.json")
    with open(clases_path, "w", encoding="utf-8") as f:
        json.dump(clases, f, ensure_ascii=False)
    print(f"💾 Modelo guardado en: {model_dir}")
    print(f"💾 Clases guardadas en: {clases_path}")

    return modelo, clases, historial


# ─────────────────────────────────────────────────────────────────────────────
# 4. Despliegue en Watson Machine Learning
# ─────────────────────────────────────────────────────────────────────────────

def desplegar_en_wml(model_dir: str = MODEL_DIR) -> str:
    """
    Despliega el modelo SavedModel en Watson Machine Learning y devuelve el
    deployment ID para uso en lsm_predictor.py.

    Returns:
        deployment_id (str): ID del deployment en WML.
    """
    from ibm_watsonx_ai import APIClient, Credentials

    credentials = Credentials(
        url=os.getenv("WATSONX_URL", ""),
        api_key=os.getenv("WATSONX_API_KEY", ""),
    )
    project_id = os.getenv("WATSONX_PROJECT_ID", "")
    client = APIClient(credentials=credentials, project_id=project_id)

    print("📦 Almacenando modelo en WML...")
    meta_props = {
        client.repository.ModelMetaNames.NAME: "Clasificador LSM — Trámite Claro",
        client.repository.ModelMetaNames.TYPE: "tensorflow_2.12",
        client.repository.ModelMetaNames.SOFTWARE_SPEC_ID: client.software_specifications.get_id_by_name(
            "runtime-22.2-py3.10"
        ),
    }
    modelo_asset = client.repository.store_model(
        model=model_dir, meta_props=meta_props
    )
    model_id = client.repository.get_model_id(modelo_asset)
    print(f"   Model asset ID: {model_id}")

    print("🚀 Desplegando en WML...")
    deploy_props = {
        client.deployments.ConfigurationMetaNames.NAME: "LSM-deployment",
        client.deployments.ConfigurationMetaNames.ONLINE: {},
    }
    deployment = client.deployments.create(model_id, meta_props=deploy_props)
    deployment_id = client.deployments.get_id(deployment)

    print(f"✅ Deployment ID: {deployment_id}")
    print("Agrega esta línea a tu .env:")
    print(f"   WML_LSM_DEPLOYMENT_ID={deployment_id}")

    return deployment_id


# ─────────────────────────────────────────────────────────────────────────────
# Punto de entrada
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Entrenar y/o desplegar el modelo LSM")
    parser.add_argument("--solo-entrenar", action="store_true",
                        help="Solo entrena y guarda el modelo localmente, sin desplegar en WML.")
    args = parser.parse_args()

    modelo, clases, _ = entrenar()

    if not args.solo_entrenar:
        desplegar_en_wml()
