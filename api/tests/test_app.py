from fastapi.testclient import TestClient

from api.app import app

client = TestClient(app)
