from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from complete_application.db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)

    email: Mapped[str] = mapped_column(unique=True, nullable=False)

    password: Mapped[str] = mapped_column(nullable=False)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow(),nullable=False)