"""Energy Planner web interface and API."""
from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI(title="Energy Planner")


@app.get("/")
def read_root():
    return FileResponse("api/index.html", media_type="text/html")


@app.get("/api")
def get_api():
    return {"data": "Hello World"}
