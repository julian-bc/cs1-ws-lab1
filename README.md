# cs1-ws-lab1 API

API REST para la clasificación de imágenes alojada en Azure Functions.

**Base URL:** `https://cs1-ws-lab1-guhsfnbgecejg8ed.brazilsouth-01.azurewebsites.net`

---

## Endpoints

| Método | Endpoint | Parámetro Query | Content-Type | Campo Body | Descripción |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `POST` | `/mnist` | `code=<TU_FUNCTION_KEY>` | `multipart/form-data` | `image` *(Archivo)* | Reconoce un dígito manuscrito (0-9). |
| `POST` | `/catsdogs` | `code=<TU_FUNCTION_KEY>` | `multipart/form-data` | `image` *(Archivo)* | Clasifica la probabilidad entre gato o perro. |

---

## Parámetros de la Petición

| Nombre | Ubicación | Tipo | Requerido | Descripción |
| :--- | :--- | :--- | :--- | :--- |
| `code` | **Query Param** | String | ✔️ | Clave de autenticación de Azure Function (*Function Key*). |
| `image` | **Form-Data Body** | File | ✔️ | Archivo de imagen a procesar (máx. 5 MB). |

---

## Ejemplos de Respuesta (200 OK)

| Endpoint | Respuesta JSON |
| :--- | :--- |
| `/mnist` | `{"digit": 7, "confidence": 0.9845}` |
| `/catsdogs` | `{"cat_percent": 12.34, "dog_percent": 87.66, "message": "This image is 12.34% cat and 87.66% dog."}` |