# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import boto3
from bson import ObjectId

# Custom modules
from utils.ocr import extract_text
from utils.aws_upload import upload_to_s3
from ml.recommender import get_similar_docs

# Load .env variables
load_dotenv()

# Initialize Flask
app = Flask(__name__)
CORS(app)

# AWS S3 client setup
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name='ap-south-1'
)
BUCKET_NAME = 'smartdoc1'

# MongoDB setup
client = MongoClient(os.getenv("MONGO_URI"))
db = client["docdb"]

# Ensure MongoDB text index
db.documents.create_index([("content", "text"), ("tags", "text")])
print("✅ Text index ensured on 'content' and 'tags'")


# Home route
@app.route("/")
def home():
    return "Smart Document Manager is running."


# Upload Route
@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files['file']
    tags = request.form.getlist('tags')

    # Extract text
    file.seek(0)
    text = extract_text(file)

    # Upload to S3
    file.seek(0)
    s3_url = upload_to_s3(file, file.filename)

    # Save to MongoDB
    doc = {
        "filename": file.filename,
        "s3_url": s3_url,
        "tags": tags,
        "content": text
    }
    result = db.documents.insert_one(doc)

    return jsonify({
        "message": "File uploaded successfully",
        "doc_id": str(result.inserted_id),
        "url": s3_url
    })


# Search Route
@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "")
    results = db.documents.find({"$text": {"$search": query}})
    return jsonify([{
        "_id": str(doc["_id"]),
        "filename": doc["filename"],
        "tags": doc.get("tags", []),
        "s3_url": doc.get("s3_url", "")
    } for doc in results])


# Recommend Route
@app.route("/recommend/<doc_id>")
def recommend(doc_id):
    results = get_similar_docs(doc_id, db)
    return jsonify(results)


# 🔐 Secure Download using Pre-signed URL
@app.route('/download', methods=['GET'])
def download_file():
    filename = request.args.get('filename')
    if not filename:
        return jsonify({'error': 'Filename is required'}), 400
    try:
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': BUCKET_NAME, 'Key': filename},
            ExpiresIn=3600  # 1 hour
        )
        return jsonify({'url': presigned_url})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Run the Flask app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
