from flask import Blueprint, jsonify, request
from flask_login import login_required

scholarships_internships = Blueprint('scholarships_internships', __name__)

# In-memory storage for scholarships and internships
scholarships = []
internships = []

@scholarships_internships.route('/scholarships', methods=['GET'])
@login_required
def get_scholarships():
    # Return the list of scholarships
    return jsonify(scholarships)

@scholarships_internships.route('/scholarships', methods=['POST'])
@login_required
def post_scholarship():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400
    
    scholarship = {
        'id': len(scholarships) + 1,
        'title': data.get('title'),
        'provider': data.get('provider'),
        'description': data.get('description'),
        'amount': data.get('amount'),
        'eligibility': data.get('eligibility'),
        'application_link': data.get('application_link'),
        'deadline': data.get('deadline')
    }#Will add/modify fields when dataset is finalised
    scholarships.append(scholarship)
    return jsonify({"success": "Scholarship posted", "scholarship": scholarship}), 201

@scholarships_internships.route('/internships', methods=['GET'])
@login_required
def get_internships():
    # Return the list of internships
    return jsonify(internships)

@scholarships_internships.route('/internships', methods=['POST'])
@login_required
def post_internship():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400
    
    internship = {
        'id': len(internships) + 1,
        'title': data.get('title'),
        'description': data.get('description'),
        'company': data.get('company'),
        'duration': data.get('duration'),
        'stipend': data.get('hourly_wage'),
    }
    internships.append(internship)
    return jsonify({"success": "Internship posted", "internship": internship}), 201