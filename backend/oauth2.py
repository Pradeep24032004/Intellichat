from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from . import  models
from datetime import datetime, timedelta
oauth2_scheme = OAuth2PasswordBearer(tokenUrl ="/signin")
SECRET_KEY = "write-your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token_str, credentials_exception):
    try:
        payload = jwt.decode(token_str, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        return {"email": email}
    except JWTError:
        raise credentials_exception

async def get_current_user(token_str: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
        
    )
    return verify_token(token_str, credentials_exception)