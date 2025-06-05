from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta

from dotenv import load_dotenv
import os

load_dotenv()

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