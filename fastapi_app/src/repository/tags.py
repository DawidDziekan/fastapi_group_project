from sqlalchemy.orm import Session
from typing import List

from fastapi_app.src.database.models import Tag
from fastapi_app.src.database.db import get_db

async def create_tags(names: list[str], db: Session):

    if names == None:
        return None

    final = []
    for name in names:
        existing = db.query(Tag).filter(Tag.name == name).first()
        if existing:
            final.append(existing)
        else:
            new_tag = Tag(name=name)
            db.add(new_tag)
            db.commit()
            final.append(new_tag)

    return final