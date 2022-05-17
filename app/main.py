from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, File, UploadFile
import aiofiles
from .models.user_data import UserData
import uuid

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile | None = File(description="Upload image here")):
    if not file:
        return {"message": "No upload file sent"}

    file_type = file.filename.split('.')[-1]
    file_prefix = uuid.uuid4().hex
    file_name = f"{file_prefix}.{file_type}"

    async with aiofiles.open(f'static/{file_name}', 'wb') as out_file:
        while content := await file.read(1024):  # async read chunk
            await out_file.write(content)

    return {"path": f"http://localhost:8000/static/{file_name}"}


@app.get("/")
async def root():
    return {"message": "Hello World"}


#TODO: add docker file, add local volume for static files