import keras, os
_BASE = os.path.join(os.path.dirname(__file__), "models_files")
_cache = {}

def get_model(name):
    if name not in _cache:
        _cache[name] = keras.saving.load_model(os.path.join(_BASE, f"{name}.keras"))
    return _cache[name]