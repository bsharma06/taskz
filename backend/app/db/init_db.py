from app.models import user, task, tenant
from app.models.base import Base
from app.db.session import engine


print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("All tables created!")