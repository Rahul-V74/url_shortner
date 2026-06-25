from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from url_shortner import SessionLocal, engine
from models import Base, Url
from base62 import encode

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


@app.get("/")
def home():
    return {"message": "URL Shortener API"}


@app.post("/urls")
def create_url(request: URLRequest):

    db = SessionLocal()

    try:
        existing = (
            db.query(Url)
            .filter(Url.long_url == request.long_url)
            .first()
        )

        if existing:
            return existing

        url_record = Url(
            long_url=request.long_url,
            short_code=""
        )

        db.add(url_record)
        db.commit()
        db.refresh(url_record)

        url_record.short_code = encode(url_record.id)

        db.commit()
        db.refresh(url_record)

        return url_record

    finally:
        db.close()


@app.get("/{short_code}")
def get_url(short_code: str):

    db = SessionLocal()

    try:
        url = (
            db.query(Url)
            .filter(Url.short_code == short_code)
            .first()
        )

        if url:
            return RedirectResponse(url.long_url)

        raise HTTPException(
            status_code=404,
            detail="URL not found"
        )

    finally:
        db.close()