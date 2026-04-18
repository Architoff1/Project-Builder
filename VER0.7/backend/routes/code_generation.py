from fastapi import APIRouter
from pydantic import BaseModel
from backend.services.code_generator import generate_code

router = APIRouter()


class CodeGenRequest(BaseModel):
    files: list[str]
    steps: list
    context: dict


@router.post("/generate-code")
def generate_code_api(req: CodeGenRequest):
    return generate_code(req.files, req.steps, req.context)