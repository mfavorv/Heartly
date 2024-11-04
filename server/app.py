from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from sqlalchemy.exc import IntegrityError

from cloudinary.uploader import upload
import cloudinary

from models import Profile, User
from config import app, db, api

# Set up Cloudinary config
cloudinary.config(
    cloud_name="dse7jpq9m",
    api_key="854464158489112",
    api_secret="77oB_ajQ7d_KLELNYBGgh1TN32c"
)

class UploadProfilePicture(Resource):
    def post(self):
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        try:
            upload_result = upload(file)
            profile_picture = upload_result["secure_url"]
            profile_picture_id = upload_result["public_id"]

            user_id = db.session.get('user_id')  
            profile = Profile.query.filter_by(user_id=user_id).first()

            if profile:
                profile.profile_picture = profile_picture
                profile.profile_picture_id = profile_picture_id
                db.session.commit()
            else:
                return jsonify({"error": "Profile not found"}), 404

            return jsonify({
                "url": profile_picture,
                "public_id": profile_picture_id
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
class SignUp(Resource):
    def post(self):
        data = request.get_json()
        name = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not name or not email or not password:
            return jsonify({"error": "All fields are required"}), 422

        new_user = User(
            name=name,
            email=email,
            password=password,
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            return jsonify({"message": "User created successfully"}), 201
        except IntegrityError:
            db.session.rollback()
            return jsonify({"error": "Email already exists"}), 422
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "Failed to create user", "details": str(e)}), 500


class Login(Resource):
    def post(self):
        data = request.json
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'success': False, 'message': 'Email and password are required'}), 400

        user = User.query.filter_by(email=email, password=password).first()

        if not user:
            return jsonify({'success': False, 'message': 'Invalid email or password'}), 401

        db.session['user_id'] = user.id
        return jsonify({'success': True, 'message': 'Login successful'})


class Logout(Resource):
    def post(self):
        db.session.clear()
        return jsonify({"message": "Logged out successfully"}), 200

class CheckSession(Resource):
    def get(self):
        user_id = db.session.get('user_id')
        if user_id:
            user = User.query.filter(User.id == user_id).first()
            if user:
                return jsonify(user.to_dict()), 200
            else:
                return jsonify({"error": "User not found"}), 404
        else:
            return jsonify({"error": "Unauthorized"}), 401

class UserList(Resource):
    def get(self):
        users = User.query.all()
        return jsonify([user.to_dict() for user in users])


class UserDetail(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify(user.to_dict())

    def patch(self, user_id):
        data = request.get_json()
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

            # Update user fields
        address = data.get('address')
        phone_number = data.get('phone_number')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        gender = data.get('gender')
        age = data.get('age')
        bio = data.get('bio')
        location = data.get('location')

        if address:
            user.address = address
        if phone_number:
            user.phone_number = phone_number
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if gender:
            user.gender = gender
        if age:
            user.age = age
        if bio:
            user.bio = bio
        if location:
            user.location = location

        # Handle profile picture upload
        if 'profile_picture' in data:
            try:
                upload_result = upload(data['profile_picture'])
                user.profile_picture = upload_result['secure_url']
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        db.session.commit()
        return jsonify({"message": "User updated successfully", "user": user.to_dict()}), 200

# Add resources to the API
api.add_resource(UploadProfilePicture, '/upload')
api.add_resource(SignUp, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(CheckSession, '/checksession')
api.add_resource(UserList, '/users')
api.add_resource(UserDetail, '/users/<int:user_id>')
