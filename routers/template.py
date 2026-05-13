from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session

from database import get_db
import models
import schemas.template

router = APIRouter(prefix="/template", tags=["Templates"])

@router.post("/", response_model=schemas.template.TemplateResponse)
def create_template(template: schemas.template.TemplateCreate, db: Session = Depends(get_db)):
    concerto = db.query(models.ConcertoDB).filter(models.ConcertoDB.id == template.concerto_id).first()
    if not concerto:
        raise HTTPException(status_code=404, detail="Concerto não encontrado no banco de dados")
        
    db_template = models.TemplateDB(**template.model_dump())
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    return db_template

@router.get("/", response_model=List[schemas.template.TemplateResponse])
def read_templates(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.TemplateDB).offset(skip).limit(limit).all()

@router.get("/{template_id}", response_model=schemas.template.TemplateResponse)
def read_template(template_id: int, db: Session = Depends(get_db)):
    template = db.query(models.TemplateDB).filter(models.TemplateDB.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template não encontrado")
    return template

@router.get("/concert/{concert_id}", response_model=List[schemas.template.TemplateResponse])
def read_templates_by_concert(concert_id: int, db: Session = Depends(get_db)):
    return db.query(models.TemplateDB).filter(models.TemplateDB.concerto_id == concert_id).all()

@router.put("/{template_id}", response_model=schemas.template.TemplateResponse)
def update_template(template_id: int, template_update: schemas.template.TemplateCreate, db: Session = Depends(get_db)):
    db_template = db.query(models.TemplateDB).filter(models.TemplateDB.id == template_id).first()
    if not db_template:
        raise HTTPException(status_code=404, detail="Template não encontrado")
    
    db_template.conteudo = template_update.conteudo
    db.commit()
    db.refresh(db_template)
    return db_template