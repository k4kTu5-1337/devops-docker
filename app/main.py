import os
import logging
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from . import models, schemas
from .database import SessionLocal, engine

# Prepare logging to /logs mount (bind from host)
LOG_DIR = "/logs"
os.makedirs(LOG_DIR, exist_ok=True)
log_path = os.path.join(LOG_DIR, "app.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler(log_path, encoding="utf-8")]
)
logger = logging.getLogger(__name__)

# Create DB tables on startup (simple demo approach)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Minimal Blog API")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/posts")
def read_posts(db: Session = Depends(get_db)):
    return db.query(models.Post).all()

@app.post("/posts", response_model=schemas.PostOut)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    item = models.Post(title=post.title, content=post.content)
    db.add(item)
    db.commit()
    db.refresh(item)
    logger.info("Created post id=%s title=%s", item.id, item.title)
    return item
