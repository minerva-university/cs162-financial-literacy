from sqlalchemy import (
    create_engine, Column, Integer, String, Boolean, Text, TIMESTAMP, Enum, ForeignKey, CheckConstraint
)
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from datetime import datetime

# Initialize SQLite engine and base class
engine = create_engine('sqlite:///app_database.db')
Base = declarative_base()

# Users Table
# Users Table
class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(100))
    mentorship_availability = Column(Boolean, default=False)
    profile_picture = Column(String(255))
    bio = Column(Text)
    created_at = Column(TIMESTAMP, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(TIMESTAMP, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    school = Column(String(255))
    company = Column(String(255))
    role = Column(String(255))

    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    votes = relationship("Vote", back_populates="user")
    following = relationship("Follow", foreign_keys='Follow.follower_id', back_populates="follower")
    followed = relationship("Follow", foreign_keys='Follow.followed_id', back_populates="followed_user")

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

    # Relationships
    internships = relationship("Internship", back_populates="organization")
    scholarships = relationship("Scholarship", back_populates="organization")


class Internship(Base):
    __tablename__ = 'internships'
    internship_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    organization_id = Column(Integer, ForeignKey('organizations.organization_id'))
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    requirements = Column(Text)
    application_link = Column(String(255))
    created_at = Column(TIMESTAMP, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(TIMESTAMP, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    organization = relationship("Organization", back_populates="internships")
    user = relationship("User", back_populates="internships")


# Scholarships Table
class Scholarship(Base):
    __tablename__ = 'scholarships'
    scholarship_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    organization_id = Column(Integer, ForeignKey('organizations.organization_id'))
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    requirements = Column(Text)
    application_link = Column(String(255))
    created_at = Column(TIMESTAMP, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(TIMESTAMP, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    organization = relationship("Organization", back_populates="scholarships")
    user = relationship("User", back_populates="scholarships")


# Mentorship Table
class Mentorship(Base):
    __tablename__ = 'mentorship'
    mentorship_id = Column(Integer, primary_key=True, autoincrement=True)
    mentor_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    mentee_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    status = Column(Enum('active', 'pending', 'completed', name='mentorship_status'), default='pending')
    created_at = Column(TIMESTAMP, default=lambda: datetime.now(timezone.utc))

    mentor = relationship("User", foreign_keys=[mentor_id])
    mentee = relationship("User", foreign_keys=[mentee_id])


# Create all tables in the database
Base.metadata.create_all(bind=engine)

# Create a new session
Session = sessionmaker(bind=engine)
session = Session()
