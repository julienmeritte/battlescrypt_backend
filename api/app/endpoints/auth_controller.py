from datetime import datetime , timedelta
from typing import Optional
import jwt
import app.utils.database_utils as database
from fastapi import APIRouter , Depends, HTTPException, status
from app.models.models_all import User
from app.dtos.userDto import userLoginDto , userRegisterDto
from app.utils.token_utils import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    JWT_SECRET_KEY,
    verify_token,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={404: {"description": "Not found"}},
)

db = database.get_db()

@router.get("/testing")
async def testing_authentication():
    json_return = {
        "message": "This is test message"
    }
    return json_return

@router.post("/login")
async def authentication_login(userLoginDto : userLoginDto):
    user: Optional[User] = (
        db.query(User).filter(User.mail == userLoginDto.mail).first()
    )
    if user is None:
        raise HTTPException(status_code=404)
    if user.password != userLoginDto.password:
        raise HTTPException(status_code=403)
    expire_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token_dict = {"exp": expire_time, "sub": userLoginDto.mail}
    return {"access_token": jwt.encode(access_token_dict, JWT_SECRET_KEY, ALGORITHM)}

@router.post("/register")
async def authentication_register(userRegisterDto: userRegisterDto):
    user: Optional[User] = (
        db.query(User).filter(User.mail == userRegisterDto.mail).first()
    )
    if user is not None:
        raise HTTPException(status_code=409)
    hashed = userRegisterDto.password.encode("utf-8")
    result: User = User(
        firstname=userRegisterDto.firstname,
        lastname=userRegisterDto.lastname,
        age=userRegisterDto.age,
        username=userRegisterDto.username,
        mail=userRegisterDto.mail,
        password=hashed,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    if hashed == userRegisterDto.password.encode("utf-8"):
        print("Match")
    else:
        print("Does not match")
    if result is None:
        raise HTTPException(status_code=500)
    db.add(result)
    db.commit()
    json_return = {
        "id": result.id,
        "mail": result.mail,
        "password": result.password,
        "created_at": result.created_at.isoformat(),
        "updated_at": result.updated_at.isoformat(),
    }
    return json_return


@router.get("/token/decode")
async def token_decode(token: str):
    decoded_token = jwt.decode(token , JWT_SECRET_KEY, ALGORITHM)
    return decoded_token
