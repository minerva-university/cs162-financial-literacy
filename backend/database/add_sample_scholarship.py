from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timezone
from create import Scholarship, engine, User

Session = sessionmaker(bind=engine)
session = Session()

try:
    # Check if there's an existing user to associate with the scholarship
    user = session.query(User).filter_by(user_id=1).first()
    if not user:
        print("No user found in the database. Ensure there's a user to associate scholarships with.")
    else:
        # Add a sample scholarship
        scholarship = Scholarship(
            user_id=user.user_id,
            title="Sample Scholarship",
            description="A sample scholarship for testing.",
            amount=1000,
            requirements="Undergraduate students with a GPA above 3.0",
            application_link="http://example.com/apply",
            deadline=datetime(2024, 12, 31, tzinfo=timezone.utc),
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        
        session.add(scholarship)
        session.commit()
        print("Sample scholarship added successfully.")
except SQLAlchemyError as e:
    session.rollback()
    print("Error occurred:", e)
finally:
    session.close()
