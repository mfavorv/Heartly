
from config import db, app
from models import User, Profile, Preference, Match, Likes, Message, Blocked
from faker import Faker

if __name__ == '__main__':
    fake = Faker()
    
    with app.app_context():  # Ensure app context is active throughout seeding
        print("Starting seed...")

        # Drop and recreate all tables
        db.drop_all()
        db.create_all()

        # Seed users
        users = []
        for _ in range(14):
            user = User(
                name=fake.name(),
                email=fake.email(),
                password=fake.password()
            )
            users.append(user)
        db.session.add_all(users)
        db.session.commit()
        print(f"User data seeded successfully. Total users: {len(users)}")


        # Seed profiles
        profiles = []
        for user in users:
            profile = Profile(
                user_id=user.id,
                address=fake.address(),
                phone_number=fake.phone_number(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                gender=fake.random_element(elements=("Male", "Female")),
                age=fake.random_int(min=18, max=80),
                bio=fake.sentence(),
                profile_picture=fake.image_url(),
                profile_picture_id=fake.uuid4(),
                location=fake.city()
            )
            profiles.append(profile)
        db.session.add_all(profiles)
        db.session.commit()
        print(f"Profile data seeded successfully. Total profiles: {len(profiles)}")

        # Seed preferences
        preferences = []
        for user in users:
            preference = Preference(
                user_id=user.id,
                preferred_age_min=fake.random_int(min=18, max=30),
                preferred_age_max=fake.random_int(min=31, max=80),
                preferred_gender=fake.random_element(elements=("Male", "Female")),
                preferred_location=fake.city()
            )
            preferences.append(preference)
        db.session.add_all(preferences)
        db.session.commit()
        print(f"Preference data seeded successfully. Total preferences: {len(preferences)}")
