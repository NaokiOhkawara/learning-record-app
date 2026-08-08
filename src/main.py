from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import sqlite3

app = FastAPI()

def init_db():
    connection = sqlite3.connect("study_records.db")

    connection.execute("""
        CREATE TABLE IF NOT EXISTS study_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            study_date TEXT NOT NULL,
            category TEXT NOT NULL,
            content TEXT NOT NULL,
            study_time INTEGER NOT NULL
        )
    """)

    connection.close()


init_db()

templates = Jinja2Templates(directory="src/templates")


@app.get("/")
def home(request: Request):
    connection = sqlite3.connect("study_records.db")
    connection.row_factory = sqlite3.Row

    records = connection.execute(
        "SELECT * FROM study_records ORDER BY id DESC"
    ).fetchall()

    connection.close()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"records": records}
    )

@app.post("/records")
def create_record(
    study_date: str = Form(...),
    category: str = Form(...),
    content: str = Form(...),
    study_time: int = Form(...)
):
    if study_time < 1:
        return {"error": "学習時間は1分以上で入力してください"}
    connection = sqlite3.connect("study_records.db")

    connection.execute(
        """
        INSERT INTO study_records (
            study_date,
            category,
            content,
            study_time
        )
        VALUES (?, ?, ?, ?)
        """,
        (study_date, category, content, study_time)
    )

    connection.commit()
    connection.close()

    return RedirectResponse(url="/", status_code=303)

@app.get("/records/{record_id}/edit")
def edit_record(request: Request, record_id: int):
    connection = sqlite3.connect("study_records.db")
    connection.row_factory = sqlite3.Row

    record = connection.execute(
        "SELECT * FROM study_records WHERE id = ?",
        (record_id,)
    ).fetchone()

    connection.close()

    return templates.TemplateResponse(
        request=request,
        name="edit.html",
        context={"record": record}
    )
@app.post("/records/{record_id}/edit")
def update_record(
    record_id: int,
    study_date: str = Form(...),
    category: str = Form(...),
    content: str = Form(...),
    study_time: int = Form(...)
):
    connection = sqlite3.connect("study_records.db")

    connection.execute(
        """
        UPDATE study_records
        SET study_date = ?,
            category = ?,
            content = ?,
            study_time = ?
        WHERE id = ?
        """,
        (
            study_date,
            category,
            content,
            study_time,
            record_id
        )
    )

    connection.commit()
    connection.close()

    return RedirectResponse(url="/", status_code=303)

@app.post("/records/{record_id}/delete")
def delete_record(record_id: int):
    connection = sqlite3.connect("study_records.db")

    connection.execute(
        "DELETE FROM study_records WHERE id = ?",
        (record_id,)
    )

    connection.commit()
    connection.close()

    return RedirectResponse(url="/", status_code=303)