from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from api.routers import auth, clientes, docs, procuradores, projetistas, projetos, users, inversores
import os
from fastapi.middleware.cors import CORSMiddleware

IMAGE_PATH = "apollodocs_image.png"
app = FastAPI(title="ApolloDocs API", version="1.0.0")

origins = os.getenv("CORS_ORIGINS", "").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(docs.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(clientes.router)
app.include_router(procuradores.router)
app.include_router(projetistas.router)
app.include_router(projetos.router)
app.include_router(inversores.router)

app.mount("/inversores", StaticFiles(directory="/app/INMETRO_INVERSORES"), name="inversores")

@app.get("/", tags=["Landing Page"])
def landing_page():
    return FileResponse(path=IMAGE_PATH, media_type="image/png")
