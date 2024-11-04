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