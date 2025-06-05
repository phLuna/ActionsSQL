from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.integrations.criptography import Auth
from src.integrations.sqlalchemy import get_db
from src.models.schemas import UserLogin, CreateUser
from src.models.users import User

router = APIRouter(prefix="/auth", tags=["Autenticação"])

auth_service = Auth()

@router.post("/login")
def login(dados: UserLogin, db: Session = Depends(get_db)):
    """Autentica um usuário e retorna um token JWT."""
    usuario = db.query(User).filter(User.email == dados.email).first()
    
    if not usuario or not auth_service.verificar_senha(dados.senha, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas"
        )

    token = auth_service.criar_token({"sub": usuario.email})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/registro")
def registrar_usuario(dados: CreateUser, db: Session = Depends(get_db)):
    """Registra um novo usuário no sistema."""
    usuario_existente = db.query(User).filter(User.email == dados.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Email já registrado.")

    senha_hash = auth_service.hash_senha(dados.senha)

    novo_usuario = User(
        nome=dados.nome,
        email=dados.email,
        senha_hash=senha_hash
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return {"mensagem": f"Usuário {novo_usuario.nome} registrado com sucesso!"}