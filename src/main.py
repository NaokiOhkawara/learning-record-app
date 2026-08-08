from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="src/templates")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.post("/records")
def create_record(
    study_date: str = Form(...),
    category: str = Form(...),
    content: str = Form(...),
    study_time: int = Form(...)
):
    return {
        "study_date": study_date,
        "category": category,
        "content": content,
        "study_time": study_time
    }