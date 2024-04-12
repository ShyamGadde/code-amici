from fastapi import FastAPI

app = FastAPI()


@app.get("api/v1/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
