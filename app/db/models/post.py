import uuid

from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import UUIDType

from app.db.base import Base


class Post(Base):
    __tablename__ = "posts"

    title: Mapped[str] = mapped_column(String(512), nullable=False)
    slug: Mapped[str] = mapped_column(String(512), unique=True, nullable=False, index=True)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    excerpt: Mapped[str | None] = mapped_column(String(512), nullable=True)
    cover_image_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    author_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(binary=False),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    # Define relationship back to User
    # pyrefly: ignore [unknown-name]
    author: Mapped["User"] = relationship("User", back_populates="posts")  # noqa: F821

    def __repr__(self) -> str:
        return f"<Post id={self.id} title={self.title} slug={self.slug}>"
