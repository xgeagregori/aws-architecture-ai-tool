from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from app import clean_text, generate_aws_services
from diagram import generate_diagram
from mangum import Mangum

app = FastAPI()
handler = Mangum(app)

origins = ["http://localhost:3000", "http://localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

MAX_INPUT_LENGTH = 350


@app.get("/aws-services")
async def generate_aws_architecture(prompt: str):
    validate_input_length(prompt)

    clean_prompt = clean_text(prompt)
    aws_services = generate_aws_services(clean_prompt)

    return {"aws_services": aws_services}


@app.get("/diagram")
async def generate_diagram_file(services: str):
    services_list = services.split(", ")

    generate_diagram(services_list)

    return FileResponse("/tmp/diagram.png", media_type="image/png")


def validate_input_length(subject: str):
    if len(subject) > MAX_INPUT_LENGTH:
        raise HTTPException(
            status_code=400, detail=f"Input must be less than {MAX_INPUT_LENGTH} characters.")
