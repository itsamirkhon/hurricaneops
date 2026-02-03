from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from ..db_models import UserDB
from ..utils.security import verify_password, create_access_token, get_password_hash, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "role": user.role}

@router.on_event("startup")
async def create_default_users():
    # Helper to seed users if they don't exist
    from ..database import SessionLocal
    db = SessionLocal()
    try:
        if not db.query(UserDB).first():
            admin = UserDB(
                username="admin", 
                hashed_password=get_password_hash("admin"), 
                role="admin"
            )
            dispatcher = UserDB(
                username="operator", 
                hashed_password=get_password_hash("operator"), 
                role="dispatcher"
            )
            viewer = UserDB(
                username="viewer", 
                hashed_password=get_password_hash("viewer"), 
                role="viewer"
            )
            db.add_all([admin, dispatcher, viewer])
            db.commit()
            print("Default users created: admin/admin, operator/operator")
    finally:
        db.close()
