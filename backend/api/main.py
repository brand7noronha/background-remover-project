from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from rembg import remove
from PIL import Image
import io


app = FastAPI()

# Adding CORS Middleware to allow only specific connections to talk to this api
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://brand7noronha.github.io/background-remover-project/",
    ],
    allow_methods=["POST"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes))

    output = remove(image)

    buffer = io.BytesIO()
    output.save(buffer, format="PNG")
    buffer.seek(0)

    return Response(content=buffer.getvalue(), media_type="image/png")
