# create.py

from dotenv import load_dotenv
import os
from sqlalchemy import (
    create_engine, Column, Integer, String, Boolean, Text, TIMESTAMP, Enum, ForeignKey, CheckConstraint
)
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime, timezone
from flask_login import UserMixin
from ..config import INITIAL_CREDITS
from enum import Enum as PyEnum
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError
from typing import Optional, Union
from werkzeug.security import generate_password_hash, check_password_hash


# Load environment variables
load_dotenv()

# Initialize SQLite engine and base class
engine = create_engine(os.environ.get("db_uri"))
Base = declarative_base()



# Users Table
class User(UserMixin, Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(100))
    mentorship_availability = Column(Boolean, default=False)
    profile_picture = Column(String(255))
    bio = Column(Text)
    credits = Column(Integer, default=INITIAL_CREDITS)  # Add this line for initial credits
    created_at = Column(TIMESTAMP, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(TIMESTAMP, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    school = Column(Text)
    company = Column(Text)
    role = Column(Text)

    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    votes = relationship("Vote", back_populates="user")
    following = relationship("Follow", foreign_keys='Follow.follower_id', back_populates="follower")
    followed = relationship("Follow", foreign_keys='Follow.followed_id', back_populates="followed_user")
    internships = relationship("Internship", foreign_keys='Internship.user_id', back_populates="user")
    scholarships = relationship("Scholarship", foreign_keys='Scholarship.user_id', back_populates="user")

    def get_id(self):
        return self.user_id
    
    # Method to set the password and salt it
    def set_password(self, password: str):
        """Hashing and salting the password before storing it in the database"""
        self.password_hash = generate_password_hash(password)

    # Method to check if the password matches
    def check_password(self, password: str) -> bool:
        """Checking the given password against the stored hash"""
        return check_password_hash(self.password_hash, password)

# Posts Table
class Post(Base):
    __tablename__ = 'posts'
    post_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    image_url = Column(String(255))
    created_at = Column(TIMESTAMP, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(TIMESTAMP, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
    votes = relationship("Vote", back_populates="post")

# Comments Table
class Comment(Base):
    __tablename__ = 'comments'
    comment_id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey('posts.post_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    comment_text = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(TIMESTAMP, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    post = relationship("Post", back_populates="comments")
    user = relationship("User", back_populates="comments")

# Votes Table
class Vote(Base):
    __tablename__ = 'votes'
    vote_id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey('posts.post_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    vote_type = Column(Enum('upvote', 'downvote', name='vote_type_enum'), nullable=False)
    created_at = Column(TIMESTAMP, default=lambda: datetime.now(timezone.utc))

    post = relationship("Post", back_populates="votes")
    user = relationship("User", back_populates="votes")

# Follow Table
class Follow(Base):
    __tablename__ = 'follow'
    follow_id = Column(Integer, primary_key=True, autoincrement=True)
    follower_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    followed_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    created_at = Column(TIMESTAMP, default=lambda: datetime.now(timezone.utc))

    follower = relationship("User", foreign_keys=[follower_id], back_populates="following")
    followed_user = relationship("User", foreign_keys=[followed_id], back_populates="followed")

    __table_args__ = (
        CheckConstraint('follower_id != followed_id', name='check_follower_not_self'),
    )

class Organization(Base):
    __tablename__ = 'organizations'
    organization_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text)
    website = Column(String(255))
    created_at = Column(TIMESTAMP, default=lambda: datetime.now(timezone.utc))

    internships = relationship("Internship", back_populates="organization")
    scholarships = relationship("Scholarship", back_populates="organization")

# Status of Scholarship and Internship
class ListingStatus(PyEnum):
    ACTIVE = "active"
    EXPIRED = "expired"
    CLOSED = "closed"

class DeletionMixin:
    """Mixin to add safe deletion methods to models"""
    
    def can_be_deleted_by(self, user_id: int) -> bool:
        """Check if the given user has permission to delete this record"""
        return hasattr(self, 'user_id') and self.user_id == user_id

    def safe_delete(self, session, user_id: int) -> tuple[bool, Optional[str]]:
        """
        Safely delete the record if the user has permission
        Returns: (success: bool, error_message: Optional[str])
        """
        try:
            if not self.can_be_deleted_by(user_id):
                return False, "Permission denied: You can only delete your own posts"
            
            session.delete(self)
            session.flush()  # Flush to catch any deletion problems before commit
            return True, None
            
        except IntegrityError as e:
            session.rollback()
            return False, f"Cannot delete: The record is being referenced by other data"
        except Exception as e:
            session.rollback()
            return False, f"Deletion failed: {str(e)}"


class Internship(DeletionMixin, Base):
    __tablename__ = 'internships'
    internship_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    organization_id = Column(Integer, ForeignKey('organizations.organization_id'))
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    requirements = Column(Text)
    application_link = Column(String(255))
    deadline = Column(TIMESTAMP, nullable=False)  # Make deadline required
    status = Column(Enum(ListingStatus), default=ListingStatus.ACTIVE)
    created_at = Column(TIMESTAMP, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(TIMESTAMP, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    organization = relationship("Organization", back_populates="internships")
    user = relationship("User", back_populates="internships")

class Scholarship(DeletionMixin, Base):
    __tablename__ = 'scholarships'
    scholarship_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    organization_id = Column(Integer, ForeignKey('organizations.organization_id'))
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    amount = Column(Integer)
    requirements = Column(Text)
    application_link = Column(String(255))
    deadline = Column(TIMESTAMP, nullable=False)  # Make deadline required
    status = Column(Enum(ListingStatus), default=ListingStatus.ACTIVE)
    created_at = Column(TIMESTAMP, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(TIMESTAMP, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    organization = relationship("Organization", back_populates="scholarships")
    user = relationship("User", back_populates="scholarships")

class MentorshipSession(Base):
    __tablename__ = 'mentorship_sessions'
    session_id = Column(Integer, primary_key=True, autoincrement=True)
    mentor_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    mentee_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    scheduled_time = Column(TIMESTAMP, nullable=False)  # Required field for scheduling
    status = Column(Enum('scheduled', 'completed', 'canceled', name='mentorship_session_status'), default='scheduled')
    created_at = Column(TIMESTAMP, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(TIMESTAMP, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    #event_id is a unique identifier for the event created in Google Calendar. It is assigned by Google and will be useful if we want to edit the event later.
    event_id = Column(String(200))

    # Relationships for Mentor and Mentee
    mentor = relationship("User", foreign_keys=[mentor_id], back_populates="mentorship_sessions_as_mentor")
    mentee = relationship("User", foreign_keys=[mentee_id], back_populates="mentorship_sessions_as_mentee")

# Update the User table to include reverse relationships
User.mentorship_sessions_as_mentor = relationship(
    "MentorshipSession",
    foreign_keys=[MentorshipSession.mentor_id],
    back_populates="mentor"
)

User.mentorship_sessions_as_mentee = relationship(
    "MentorshipSession",
    foreign_keys=[MentorshipSession.mentee_id],
    back_populates="mentee"
)

# Create all tables in the database
Base.metadata.create_all(bind=engine)
