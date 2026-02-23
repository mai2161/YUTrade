# Assigned to: Mickey (Michael Byalsky)
# Phase: 1 (B1.2)
#
# TODO: Set up SQLAlchemy database connection.
#
# 1. Import create_engine, sessionmaker, declarative_base from sqlalchemy
# 2. Import settings from config.py
# 3. Create engine using settings.DATABASE_URL
#    - For SQLite, add connect_args={"check_same_thread": False}
# 4. Create SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# 5. Create Base = declarative_base()
#    - All ORM models will inherit from this Base
