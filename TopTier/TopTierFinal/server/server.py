from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from passlib.context import CryptContext

# 데이터베이스 연결 정보
DATABASE_URL = "mysql+pymysql://root:mysql@localhost:3307/toptier"

# SQLAlchemy 엔진 및 세션 설정
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 사용자 모델 정의
class User(Base):
    __tablename__ = "user"

    id = Column(String(12), primary_key=True, index=True)
    username = Column(String(20), unique=True, index=True)
    hashed_password = Column(String(60))  # 비밀번호 해시의 길이 수정

# 테이블 생성
Base.metadata.create_all(bind=engine)

# FastAPI 애플리케이션
app = FastAPI()

# 비밀번호 해시 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Pydantic 모델 정의
class UserCreate(BaseModel):
    username: str
    password: str

class UserInDB(UserCreate):
    hashed_password: str

# 비밀번호 해시 및 확인 함수
def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# 데이터베이스 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 회원가입 API
@app.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = hash_password(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully"}

# 로그인 API
@app.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user is None or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful"}
