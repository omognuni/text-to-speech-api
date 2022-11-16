from fastapi import APIRouter, Depends, HTTPException

from db import engine, SessionLocal
from sqlalchemy.orm import Session

import os
import shutil

import db
import config
from schemas import project as schemas
from models import project as models


router = APIRouter(
    prefix="/project",
    tags=['project']
)

db.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
        
@router.get("/")
async def get_projects(db: Session = Depends(get_db)):
    return db.query(models.Project).all()

@router.get("/{project_id}")
async def get_project_detail(project_id:int, db: Session = Depends(get_db)):
    return db.query(models.Project).filter(models.Project.id == project_id).first()

@router.delete("/{project_id}")
async def delete_project_detail(project_id:int, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if project is None:
        raise HTTPException(status_code=404)
    
    for audio in project.audios:
        shutil.rmtree(os.path.join(config.MEDIA_ROOT, f'{audio.id}'))
        
    db.delete(project)
    db.commit()
    return {"status": 204}

@router.post("/")
async def create_project(project: schemas.Project, db: Session = Depends(get_db)):
    db_project = models.Project(title=project.title)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project