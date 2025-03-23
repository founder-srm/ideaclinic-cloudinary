from flask import Flask, request, jsonify
from dotenv import load_dotenv
load_dotenv()

import cloudinary
from cloudinary import CloudinaryImage
import cloudinary.uploader
import cloudinary.api

# Configure Cloudinary
config = cloudinary.config(secure=True)

app = Flask(__name__)

def delete_image(public_id):
    try:
        result = cloudinary.uploader.destroy(public_id)
        if result.get('result') == 'ok':
            print("Image deleted successfully!")
            return {"status": "success", "message": "Image deleted successfully"}
        else:
            print(f"Warning: Cloudinary returned: {result}")
            return {"status": "warning", "message": f"Cloudinary returned: {result}"}
    except Exception as e:
        print(f"Error deleting image: {str(e)}")
        raise Exception(f"Error deleting image: {str(e)}")

@app.route('/')
def home():
    return 'Hello, Founders Club!'

@app.route('/delete/resource', methods=['POST'])
def delete_resource():
    try:
        request_data = request.get_json()
        public_id = request_data.get('public_id')
        
        if not public_id:
            return jsonify({"error": "Missing required parameter: public_id"}), 400
        
        result = delete_image(public_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": f"Error deleting image: {str(e)}"}), 500