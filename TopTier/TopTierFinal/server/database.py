from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# MySQL 데이터베이스 URL 구성
DATABASE_URL = "mysql+pymysql://root:mysql@localhost:3307/toptier"

# 데이터베이스 엔진 생성
engineconn = create_engine(DATABASE_URL)

# 세션 로컬 클래스
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engineconn)


