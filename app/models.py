import os

import keras
from azure.storage.blob import ContainerClient

_BASE = os.path.join(os.path.dirname(__file__), "models_files")
_CONTAINER_URL = os.getenv("MODELS_CONTAINER_URL")
_cache = {}

def _download(name, path):
    if not _CONTAINER_URL:
        raise RuntimeError(f"No existe {path} y MODELS_CONTAINER_URL no está definida")
    os.makedirs(_BASE, exist_ok=True)
    tmp = path + ".part"
    with open(tmp, "wb") as f:
        ContainerClient.from_container_url(_CONTAINER_URL).download_blob(f"{name}.keras").readinto(f)
    os.replace(tmp, path)  # evita dejar un .keras a medio descargar

def get_model(name):
    if name not in _cache:
        path = os.path.join(_BASE, f"{name}.keras")
        if not os.path.exists(path):
            _download(name, path)
        _cache[name] = keras.saving.load_model(path, compile=False)
    return _cache[name]
