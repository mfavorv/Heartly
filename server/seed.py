
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

        # Seed matches
        matches = []
        for user in users:
            potential_match = fake.random_element(elements=users)
            if potential_match != user:  # Avoid self-matching
                match = Match(
                    user_id=user.id,
                    potential_match_id=potential_match.id,
                    status=fake.random_element(elements=("pending", "accepted", "rejected"))
                )
                matches.append(match)
        db.session.add_all(matches)
        db.session.commit()
        print(f"Match data seeded successfully. Total matches: {len(matches)}")

        # Seed likes
        likes = []
        for user in users:
            liked_user = fake.random_element(elements=users)
            if liked_user != user:  # Avoid self-liking
                like = Likes(
                    user_id=user.id,
                    liked_user_id=liked_user.id
                )
                likes.append(like)
        db.session.add_all(likes)
        db.session.commit()
        print(f"Like data seeded successfully. Total likes: {len(likes)}")

        # Seed messages
        messages = []
        for user in users:
            recipient = fake.random_element(elements=users)
            if recipient != user:  # Avoid sending messages to self
                message = Message(
                    user_id=user.id,
                    recipient_id=recipient.id,
                    content=fake.sentence()
                )
                messages.append(message)
        db.session.add_all(messages)
        db.session.commit()
        print(f"Message data seeded successfully. Total messages: {len(messages)}")

        # Seed blocked
        blocked = []
        for user in users:
            blocked_user = fake.random_element(elements=users)
            if blocked_user != user:  # Avoid self-blocking
                block = Blocked(
                    user_id=user.id,
                    blocked_user_id=blocked_user.id
                )
                blocked.append(block)
        db.session.add_all(blocked)
        db.session.commit()
        print(f"Blocked data seeded successfully. Total blocked users: {len(blocked)}")

    print("Database seeding completed successfully.")
