from typing import List

from fastapi import FastAPI
from models import Annonce, Annonce_Pydantic, AnnonceIn_Pydantic
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise
from pydantic import BaseModel
from starlette.exceptions import HTTPException


class Status(BaseModel):
    message : str

app = FastAPI(title="TOR API", debug=True, version="V1", description="API pour l'application des objets perdus ou retrouves")


@app.get("/")
async def home():
    return {"Hello" : "World"}


@app.get("/annonces", response_model=List[Annonce_Pydantic])
async def get_annonces():
    return await Annonce_Pydantic.from_queryset(Annonce.all())


@app.post("/annonce", response_model=Annonce_Pydantic)
async def create_annonce(annonce: AnnonceIn_Pydantic):
    obj = await Annonce.create(**annonce.model_dump(exclude_unset=True))
    return await Annonce_Pydantic.from_tortoise_orm(obj)

@app.get("/annonce/{id}", response_model=AnnonceIn_Pydantic, responses={404:{'model': HTTPNotFoundError}})
async def get_annonce(annonce_id: int):
    return await AnnonceIn_Pydantic.from_queryset_single(Annonce.get(id = annonce_id))

@app.put("/annonce/{id}", response_model=Annonce_Pydantic)
async def update_annonce(annonce_id: int, annonce: AnnonceIn_Pydantic):
    await Annonce.filter(id=annonce_id).update(**annonce.model_dump(exclude_unset=True))
    return await Annonce_Pydantic.from_queryset_single(Annonce.get(id=annonce_id))

@app.delete("/annonce/{id}", response_model=Status)
async def delete_annonce(annonce_id: int):
    deleted_count = await Annonce.filter(id=annonce_id).delete()
    if not deleted_count:
        raise HTTPException(
            status_code= 404,
            detail= f"L'annonce {annonce_id} n'a pas été trouvée"
        )
    return Status(message=f"L'annonce {annonce_id} a été supprimée")


register_tortoise(
    app,
    db_url="sqlite://store.db",
    modules= {"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True
)