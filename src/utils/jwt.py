from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta,UTC

from src import exceptions
from src.models.tortoise import Team
from src.configs import SECRET_KEY, ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def jwt_encode_content(content:dict):
    return jwt.encode(content, SECRET_KEY, algorithm=ALGORITHM)

def create_team_access_token(team:Team):
    to_encode = {
        "sub": team.id,
        "name": team.name,
        "iat": 1516239022
    }
    return jwt_encode_content(to_encode)

def create_access_token(data: dict, expires_delta: float= ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    return jwt_encode_content(to_encode)

async def decode_jwt(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        jwt_id: str = payload.get("sub")
        if jwt_id is None:
            raise exceptions.CredentialsDataWrong()
    except JWTError:
        raise exceptions.CredentialsDataWrong()
    return payload