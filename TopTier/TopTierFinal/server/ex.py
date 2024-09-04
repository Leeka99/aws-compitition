from fastapi import FastAPI, Depends
from pydantic import BaseModel
from database import engineconn, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import text

app = FastAPI()

@app.get("/")
def printHello():
    return "Hello World"

# 의존성 주입을 통해 데이터베이스 세션을 가져오기 위한 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 데이터베이스 연결을 확인하기 위한 엔드포인트
@app.get("/ping_db")
def ping_db(db: Session = Depends(get_db)):
    try:
        # 간단한 쿼리로 데이터베이스 연결 상태 확인
        db.execute(text("SELECT 1"))
        return {"status": "Database connection successful"}
    except Exception as e:
        return {"status": "Database connection failed", "error": str(e)}


@app.get("/json")
def printJson():
	return {
		"Number" : 12345
	}
    
class Post(BaseModel):
	title: str
	content: str

@app.post("/posts")
def createContents(post : Post):
	title = post.title
	content = post.content