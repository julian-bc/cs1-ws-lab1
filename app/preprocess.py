import numpy as np
from PIL import Image

def prep_mnist(file_stream):
    img = Image.open(file_stream).convert("L").resize((28, 28))
    arr = np.asarray(img, dtype="float32") / 255.0
    return arr.reshape(1, 28, 28, 1)

def prep_catsdogs(file_stream, size=(180, 180)):
    img = Image.open(file_stream).convert("RGB").resize(size)
    arr = np.asarray(img, dtype="float32") / 255.0
    return np.expand_dims(arr, 0)