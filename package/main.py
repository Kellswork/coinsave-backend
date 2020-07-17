from fastapi import Depends, FastAPI, HTTPException
import uvicorn
from sqlalchemy.orm import Session
from package import crud, models, schemas
from package.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post('/users/', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail='email already registered')
    return crud.create_user(db=db, user=user)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8081)