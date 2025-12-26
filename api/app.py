from fastapi import FastAPI
from fastapi.responses import FileResponse

from api.routers import docs, users

IMAGE_PATH = "apollodocs_image.png"
app = FastAPI(title="ApolloDocs API", version="1.0.0")
app.include_router(docs.router)
app.include_router(users.router)


@app.get("/")
def landing_page():
    return FileResponse(path=IMAGE_PATH, media_type="image/png")
