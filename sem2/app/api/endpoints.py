from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from app.schemas.graph import Graph, PathResult
from app.services.tsp import solve_tsp
from app.cruds.user import create_user, get_user_by_id, authenticate_user
from app.core.auth import create_access_token, get_current_user
from app.db.database import get_db
from app.models.user import User

router = APIRouter()

@router.post("/sign-up/")
def sign_up(email: str = Body(...), password: str = Body(...), db: Session = Depends(get_db)):
    user = create_user(db, email, password)
    token = create_access_token(data={"sub": str(user.id)})  # передаём id в токен
    return {"id": user.id, "email": user.email, "token": token}

@router.post("/login/")
def login(email: str = Body(...), password: str = Body(...), db: Session = Depends(get_db)):
    user = authenticate_user(db, email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Некорректный email или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": str(user.id)})  # передаём id в токен
    return {'id': user.id, 'email': user.email, "access_token": access_token}

@router.get("/users/me/")
def read_users_me(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email}

@router.post("/shortest-path/", response_model=PathResult)
def get_shortest_path(graph: Graph, current_user: User = Depends(get_current_user)): #
    result = solve_tsp(graph)
    return result




