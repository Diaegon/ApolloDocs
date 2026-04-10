from fastapi import APIRouter, Depends
from typing import List
import os
from pydantic import BaseModel
from api.security import get_current_user

router = APIRouter(prefix="/inversores", tags=["Inversores"])

class InversorModel(BaseModel):
    name: str
    files: List[str]

class InversorBrand(BaseModel):
    brand: str
    models: List[InversorModel]

BASE_DIR = "/app/INMETRO_INVERSORES"

@router.get("/list", response_model=List[InversorBrand])
def list_inversores(current_user=Depends(get_current_user)):
    target_dir = BASE_DIR if os.path.exists(BASE_DIR) else "./INMETRO_INVERSORES"
    brands = []
    
    if not os.path.exists(target_dir):
        return []
        
    for brand_name in sorted(os.listdir(target_dir)):
        brand_path = os.path.join(target_dir, brand_name)
        if not os.path.isdir(brand_path):
            continue
            
        brand_models = []
        for model_name in sorted(os.listdir(brand_path)):
            model_path = os.path.join(brand_path, model_name)
            if not os.path.isdir(model_path):
                continue
                
            files = []
            for file_name in sorted(os.listdir(model_path)):
                if os.path.isfile(os.path.join(model_path, file_name)) and file_name.endswith('.pdf'):
                    files.append(file_name)
                    
            if files:
                brand_models.append(InversorModel(name=model_name, files=files))
                
        if brand_models:
            brands.append(InversorBrand(brand=brand_name, models=brand_models))
            
    return brands
