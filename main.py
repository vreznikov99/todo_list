from typing import List
import uvicorn
from fastapi import FastAPI
from pydantic_settings import BaseSettings
from resources import EntryManager, Entry
from fastapi.middleware.cors import CORSMiddleware


class Settings(BaseSettings):
    data_folder: str = './tmp/'


settings = Settings()

app = FastAPI()

origins = [
    "https://wexler.io"  # адрес на котором работает фронт-энд
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,    # Список разрешенных доменов
    allow_credentials=True,   # Разрешить Cookies и Headers
    allow_methods=["*"],      # Разрешить все HTTP методы
    allow_headers=["*"],      # Разрешить все хедеры
)

@app.get("/")
async def hello_world():
    return {"Hello": "World"}


@app.get("/api/entries/")
async def get_entries():
    entry_manager = EntryManager(settings.data_folder)
    entry_manager.load()
    res_list = []
    for entry in entry_manager.entries:
        res_list.append(entry.json())

    return res_list


@app.get("/api/folder/")
async def get_data_folder():
    return {'folder': settings.data_folder}


@app.post("/api/save_entries/")
async def save_entries(data: List[dict]):
    entry_manager = EntryManager(settings.data_folder)
    for elem in data:
        entry = Entry.from_json(elem)
        entry_manager.entries.append(entry)
    entry_manager.save()
    return {'status': 'success'}

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
