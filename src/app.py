
from flask import Flask, jsonify, request
from flask_cors import CORS
from datastructures import FamilyStructure
from utils import APIException, generate_sitemap

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)


jackson_family = FamilyStructure("Jackson")


John = {
    "first_name": "John",
    "age": 33,
    "lucky_numbers": [7, 13, 22]
}

Jane = {
    "first_name": "Jane",
    "age": 35,
    "lucky_numbers": [10, 14, 3]
}

Jimmy = {
    "first_name": "Jimmy",
    "age": 5,
    "lucky_numbers": [1]
}

jackson_family.add_member(John)
jackson_family.add_member(Jane)
jackson_family.add_member(Jimmy)

# Manejo de errores como un objeto JSON
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route('/member/<int:id>', methods=['GET'])
def get_single_member(id):
    member = jackson_family.get_member(id)
    if member:
        return jsonify(member), 200
    return jsonify({"error": "Member not found"}), 404

@app.route('/member', methods=['POST'])
def create_member():
    member = request.json
    if not member:
        return jsonify({"error": "No data provided"}), 400
    
    jackson_family.add_member(member)
    return jsonify({"message": "Member created"}), 200

@app.route('/member/<int:id>', methods=['DELETE'])
def delete_single_member(id):
    if jackson_family.delete_member(id):
        return jsonify({"done": True}), 200
    return jsonify({"error": "Member not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)

