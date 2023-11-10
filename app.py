from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Initialize Firestore
cred = credentials.Certificate('service_account.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

app = Flask(__name__)

# This dictionary will store the moderation data in memory
moderation_data = {
    'picture_moderation': [],
    'name_moderation': []
}

@app.route('/picture-moderation', methods=['POST'])
def picture_moderation():
    if not request.json or 'pictureBlob' not in request.json or 'action' not in request.json:
        return jsonify({'error': 'Invalid data, pictureBlob and action are required'}), 400

    picture_blob = request.json['pictureBlob']
    action = request.json['action']

    if action not in ['approve', 'reject']:
        return jsonify({'error': 'Invalid action. Must be approve or reject.'}), 400

    # Store the moderation data
    moderation_entry = {
        'pictureBlob': picture_blob,
        'action': action
    }
    moderation_data['picture_moderation'].append(moderation_entry)

    # Send data to Firestore
    doc_ref = db.collection('picture_moderation').document()
    doc_ref.set(moderation_entry)

    return jsonify({'message': 'Picture moderation data stored successfully'}), 200

@app.route('/name-moderation', methods=['GET'])
def name_moderation():
    name = request.args.get('name')
    action = request.args.get('action')

    if not name or action not in ['approve', 'reject']:
        return jsonify({'error': 'Invalid data'}), 400

    # Store the moderation data
    moderation_entry = {
        'name': name,
        'action': action
    }
    moderation_data['name_moderation'].append(moderation_entry)

    # Send data to Firestore
    doc_ref = db.collection('name_moderation').document()
    doc_ref.set(moderation_entry)

    return jsonify({'message': 'Name moderation data stored successfully'}), 200

if __name__ == '__main__':
    app.run(debug=False,port=5000)
