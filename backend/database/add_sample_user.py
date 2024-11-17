# add_sample_user.py
from sqlalchemy.orm import sessionmaker
from create import User, engine
from werkzeug.security import generate_password_hash

# Create a new session
Session = sessionmaker(bind=engine)
session = Session()

try:
    # Create a sample user
    sample_user = User(
        username='sampleuser',
        email='sample@example.com',
        password_hash=generate_password_hash('samplepassword'),
        name='Sample User'
    )
    
    # Add and commit the user
    session.add(sample_user)
    session.commit()
    print("Sample user added successfully.")
except Exception as e:
    session.rollback()
    print("Error adding sample user:", e)
finally:
    session.close()
