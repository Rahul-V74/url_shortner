from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
import string
from fastapi.responses import RedirectResponse
from url_shortner import SessionLocal, engine
from models import Base, Url

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

class URLRequest(BaseModel):
    long_url: str

@app.post("/urls")
def create_url(request: URLRequest):
    db = SessionLocal()
    try:
        existing = db.query(Url).filter(Url.long_url == request.long_url).first()
        if existing:
            return {
                "id": existing.id,
                "long_url": existing.long_url,
                "short_code": existing.short_code,
            }

        while True:
            short_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
            if not db.query(Url).filter(Url.short_code == short_code).first():
                break
        url_record = Url(long_url=request.long_url, short_code=short_code)
        db.add(url_record)
        db.commit()
        db.refresh(url_record)
        return {
            "id": url_record.id,
            "long_url": url_record.long_url,
            "short_code": url_record.short_code,
        }
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "URL shortener API"}

@app.get("/{short_code}")
def get_url(short_code: str):
    db = SessionLocal()
    try:
        url = db.query(Url).filter(Url.short_code == short_code).first()
        if url:
            return RedirectResponse(url.long_url)
        raise HTTPException(status_code=404, detail="URL not found")
    finally:
        db.close()
