from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class Note(Base):
    __tablename__ ="notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))