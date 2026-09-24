"""
rag_service.py — Pipeline RAG sobre las fichas del catálogo RETyS BC.

Expone tres funciones públicas:
  - indice_existe()        → bool   (¿ya hay datos en el vector store?)
  - construir_indice()     → None   (vectoriza fichas y persiste en ChromaDB)
  - recuperar_contexto()   → list   (búsqueda semántica ante una pregunta)

El vector store se persiste en backend/vectorstore/ entre reinicios.
Las fichas se leen desde backend/fichas/ (generadas por descargar_fichas.py).
El modelo de embeddings es ibm/granite-embedding-278m-multilingual via watsonx.ai.
"""
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import Embeddings
import chromadb

load_dotenv()

# ─────────────────────────────────────────────────────────────────────────────
# Rutas y configuración
# ─────────────────────────────────────────────────────────────────────────────

_BASE_DIR = Path(__file__).resolve().parent
_FICHAS_DIR = _BASE_DIR / "fichas"
_INDEX_FILE = _BASE_DIR / "fichas_index.json"
_VECTORSTORE_DIR = _BASE_DIR / "vectorstore"
_COLLECTION_NAME = "tramites_retys"
_EMBEDDING_MODEL = "ibm/granite-embedding-278m-multilingual"
_DISTANCIA_UMBRAL = 0.70  # distancia L2 máxima para considerar un resultado relevante
                           # (calibrado: correctos < 0.65, falsos positivos > 0.80)
_MAX_CHARS = 1800          # ~450 tokens en español; límite del modelo de embeddings: 512 tokens

# ─────────────────────────────────────────────────────────────────────────────
# Inicialización lazy de credenciales y cliente ChromaDB
# ─────────────────────────────────────────────────────────────────────────────

def _get_embeddings() -> Embeddings:
    """Crea y devuelve el cliente de embeddings de watsonx.ai."""
    return Embeddings(
        model_id=_EMBEDDING_MODEL,
        credentials=Credentials(
            url=os.getenv("WATSONX_URL", ""),
            api_key=os.getenv("WATSONX_API_KEY", ""),
        ),
        project_id=os.getenv("WATSONX_PROJECT_ID", ""),
    )


def _get_collection() -> chromadb.Collection:
    """Devuelve la colección ChromaDB (crea el directorio si no existe)."""
    client = chromadb.PersistentClient(path=str(_VECTORSTORE_DIR))
    return client.get_or_create_collection(
        name=_COLLECTION_NAME,
        metadata={"hnsw:space": "l2"},
    )


# ─────────────────────────────────────────────────────────────────────────────
# API pública
# ─────────────────────────────────────────────────────────────────────────────

def indice_existe() -> bool:
    """
    Retorna True si el vector store ya fue construido y contiene documentos.

    Returns:
        True si hay al menos un documento indexado, False en caso contrario.
    """
    if not _VECTORSTORE_DIR.exists():
        return False
    try:
        col = _get_collection()
        return col.count() > 0
    except Exception:
        return False


def construir_indice() -> None:
    """
    Lee las fichas .txt de fichas_index.json, las vectoriza y las persiste en ChromaDB.

    Imprime progreso en terminal durante la construcción.
    No hace nada si fichas_index.json no existe.
    """
    if not _INDEX_FILE.exists():
        print("[RAG] fichas_index.json no encontrado — omitiendo construcción.")
        return

    with open(_INDEX_FILE, encoding="utf-8") as f:
        fichas = json.load(f)

    print(f"[RAG] Construyendo índice de fichas RETyS ({len(fichas)} fichas)...")

    col = _get_collection()
    emb_client = _get_embeddings()

    textos, ids, metadatos = [], [], []

    for ficha in fichas:
        ruta_txt = _BASE_DIR / ficha["txt"]
        if not ruta_txt.exists():
            print(f"[RAG] Advertencia: no se encontró {ruta_txt}, omitiendo.")
            continue

        texto_completo = ruta_txt.read_text(encoding="utf-8").strip()
        # Truncar al límite de tokens del modelo de embeddings (512 tokens ≈ 1800 chars)
        texto = texto_completo[:_MAX_CHARS]
        doc_id = str(ficha["id"])

        textos.append(texto)
        ids.append(doc_id)
        metadatos.append({
            "nombre":    ficha.get("nombre", ""),
            "organismo": ficha.get("organismo", ""),
            "homoclave": ficha.get("homoclave", ""),
            "id_retys":  doc_id,
        })
        print(f"[RAG] Indexando: {ficha.get('nombre', doc_id)}")

    if not textos:
        print("[RAG] No se encontraron fichas para indexar.")
        return

    # embed_documents devuelve directamente una lista de vectores (list[list[float]])
    embeddings_list = emb_client.embed_documents(texts=textos)

    col.add(
        documents=textos,
        embeddings=embeddings_list,
        ids=ids,
        metadatas=metadatos,
    )

    print(f"[RAG] Índice construido con {len(textos)} fichas. Listo.")


def _leer_texto_completo(id_retys: str) -> str:
    """Lee el texto completo del .txt original dado el id del trámite."""
    if not _INDEX_FILE.exists():
        return ""
    with open(_INDEX_FILE, encoding="utf-8") as f:
        fichas = json.load(f)
    for ficha in fichas:
        if str(ficha["id"]) == id_retys:
            ruta = _BASE_DIR / ficha["txt"]
            if ruta.exists():
                return ruta.read_text(encoding="utf-8").strip()
    return ""


def recuperar_contexto(pregunta: str, n_resultados: int = 3) -> list[dict]:
    """
    Busca semánticamente en el vector store las fichas más relevantes.

    Devuelve el texto completo de cada ficha (no el truncado usado para indexar),
    para que el agente tenga toda la información disponible.

    Args:
        pregunta:     Texto de la consulta del ciudadano.
        n_resultados: Número máximo de documentos a recuperar.

    Returns:
        Lista de dicts con claves: texto, nombre, organismo, homoclave, distancia.
        Lista vacía si no hay resultados por encima del umbral o el índice no existe.
    """
    if not indice_existe():
        return []

    col = _get_collection()
    emb_client = _get_embeddings()

    query_vector = emb_client.embed_query(text=pregunta)

    resultados = col.query(
        query_embeddings=[query_vector],
        n_results=min(n_resultados, col.count()),
        include=["documents", "metadatas", "distances"],
    )

    salida = []
    for _, meta, distancia in zip(
        resultados["documents"][0],
        resultados["metadatas"][0],
        resultados["distances"][0],
    ):
        if distancia <= _DISTANCIA_UMBRAL:
            texto_completo = _leer_texto_completo(meta.get("id_retys", ""))
            salida.append({
                "texto":     texto_completo,
                "nombre":    meta.get("nombre", ""),
                "organismo": meta.get("organismo", ""),
                "homoclave": meta.get("homoclave", ""),
                "distancia": distancia,
            })

    return salida
