import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
load_dotenv()
from sqlalchemy.orm import sessionmaker, Session

def get_url():
    print(os.getenv("DB_PASSWORD", "no esta tomandola"))
    return "postgresql://%s:%s@%s:%s/%s" % (
        os.getenv("DB_USER", "none"),
        os.getenv("DB_PASSWORD", "none"),
        os.getenv("DB_HOST", "none"),
        os.getenv("DB_PORT", "none"),
        os.getenv("DB_NAME", "none"),
    )

SQLALCHEMY_DATABASE_URI = get_url()


engine = create_engine(  # 2
    # "postgresql://postgres:admin@localhost:5432/test"
    SQLALCHEMY_DATABASE_URI,
    # required for sqlite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
