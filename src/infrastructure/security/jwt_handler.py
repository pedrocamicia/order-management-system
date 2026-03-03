from jose import jwt
from datetime import datetime, timedelta, timezone
from src.infrastructure.security.config import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE, SECRET_KEY, ALGORITHM


def create_access_token(user_id : int):
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    payload = {
        "sub" : str(user_id),
        "type" : "access",
        "exp" : expire
    }
    
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(user_id : int):
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE)
    
    payload = {
        "sub" : str(user_id),
        "type" : "refresh",
        "exp" : expire
    }
    
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

