from flask import Flask, request, jsonify
import os

# Set your Cloudinary credentials
# ==============================
from dotenv import load_dotenv
load_dotenv()

# Import the Cloudinary libraries
# ==============================
import cloudinary
from cloudinary import CloudinaryImage
import cloudinary.uploader
import cloudinary.api

# Configure Cloudinary
config = cloudinary.config(secure=True)

app = Flask(__name__)

def retrieve_image_ids(image_url):
    try:
        # Extract the public_id from the URL if available
        public_id = None
        if image_url:
            # Simple extraction - adjust as needed based on your URL format
            parts = image_url.split('/')
            filename = parts[-1]
            if '.' in filename:
                public_id = filename.split('.')[0]
        
        # Get the resource details from Cloudinary
        if public_id:
            result = cloudinary.api.resource(public_id)
            return {
                'public_id': result.get('public_id'),
                'resource_id': result.get('asset_id'),
                'resource_type': result.get('resource_type', 'image')
            }
        else:
            return {'error': 'No public_id could be extracted from the URL'}
    
    except Exception as e:
        print(f"Error retrieving image IDs: {str(e)}")
        return {'error': str(e)}

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
    return 'Hello, world!'

@app.route('/get_ids', methods=['POST'])
def get_ids():
    try:
        request_data = request.get_json()
        image_url = request_data.get('image_url')
        
        if not image_url:
            return jsonify({"error": "Missing required parameter: image_url"}), 400
        
        result = retrieve_image_ids(image_url)
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": f"Error retrieving image IDs: {str(e)}"}), 500

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

# Backward compatibility for old delete action
@app.route('/delete', methods=['POST'])
def delete():
    try:
        request_data = request.get_json()
        action = request_data.get('action')
        
        if action != 'delete':
            return jsonify({"error": "Invalid action"}), 400
            
        public_id = request_data.get('public_id')
        
        if not public_id:
            return jsonify({"error": "Missing required parameter: public_id"}), 400
        
        result = delete_image(public_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": f"Error deleting image: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)