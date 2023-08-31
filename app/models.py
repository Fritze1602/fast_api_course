from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Boolean, text
from sqlalchemy.orm import relationship
from app.database import Base

# Defines, how our tables and database
# look like! Hier steuer wir eher die Response


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='true', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete='cascade'), nullable=False)

    # Das macht in der Datenbank nichts! Das ist SQL Alchemy, verweist auf das Model,
    # nicht auf die Tabelle -> So werden automatisch die Joins gesetzt.
    # Sehr mächtig und einfach!
    owner = relationship("User", back_populates="posts")


class User(Base):
    __tablename__ = "users"
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    phone_number = Column(String, unique=True)
    posts = relationship("Post", back_populates="owner")


class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="Cascade"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="Cascade"), primary_key=True)
