"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route('/member/<int:id>', methods=['GET'])
def get_member_to_the_family(id):
    member = jackson_family.get_member(id)
    if member:
        return jsonify(member), 200
    else: 
        return jsonify({'message': 'Member not found.'}), 404

@app.route('/member', methods=['POST'])
def add_to_family():
    data = request.json
    new_member = jackson_family.add_member(data)
    if new_member:
        return jsonify({'message': 'Member added correctly.'}), 200
    else:
        return jsonify({'message': 'Something went wrong... try again later'}), 500
    
@app.route('/member/<int:id>', methods=['DELETE'])
def delete_to_famlily(id):
    result = jackson_family.delete_member(id)
    if result.get('done'):
        return jsonify({'done': True}), 200
    else: 
        return jsonify({'done': False}), 500

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
