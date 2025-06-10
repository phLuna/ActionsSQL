from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

from src.integrations.sqlalchemy import get_db
from src.models.db_users import User

load_dotenv()

oauth2_scheme = HTTPBearer()

class Auth:
    SECRET_KEY = os.getenv("SECRET_KEY") or "chave-fallback-insegura"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_senha(self, senha: str) -> str:
        return self.pwd_context.hash(senha)

    def verificar_senha(self, senha: str, hash: str) -> bool:
        return self.pwd_context.verify(senha, hash)

    def criar_token(self, dados: dict) -> str:
        dados_copia = dados.copy()
        expira = datetime.utcnow() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        dados_copia.update({"exp": expira})
        return jwt.encode(dados_copia, self.SECRET_KEY, algorithm=self.ALGORITHM)

    def verificar_token(self, token: str):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            return payload
        except JWTError:
            return None

    def get_current_user(self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
        cred_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou ausente.",
            headers={"WWW-Authenticate": "Bearer"},
        )
        payload = self.verificar_token(token.credentials)
        if payload is None:
            raise cred_exception

        user_id = payload.get("sub")
        if user_id is None:
            raise cred_exception

        user = db.query(User).filter(User.id == int(user_id)).first()
        if user is None:
            raise cred_exception

        return user
