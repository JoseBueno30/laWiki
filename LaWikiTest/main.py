from fastapi import FastAPI

# Crear una instancia de FastAPI
app = FastAPI()

# Crear una ruta GET para la raíz del servidor
@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}

# Crear una ruta GET con parámetro
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "query": q}

# uvicorn main:app --reload