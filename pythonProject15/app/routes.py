
from .models import db, Patient, Diagnosis, Treatment
from flask import Blueprint, jsonify, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, User
main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def home():
    return "Welcome to the Hybrid Intelligence Platform for Comprehensive Breast Cancer Care"


@main_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    hashed_password = generate_password_hash(data['pwd'])
    new_user = User(name=data['name'], age=data['age'], email=data['email'], pwd=hashed_password, url=data.get('url'))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully", "user": new_user.to_dict()}), 201

@main_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    hashed_password = generate_password_hash(data['pwd'])
    print(hashed_password)
    print(check_password_hash(user.pwd, data['pwd']))
    if user and check_password_hash(user.pwd, data['pwd']):
        session['user_id'] = user.id
        return jsonify({"code": 200, "message": "Login successful", "data": user.to_dict()}), 200
    return jsonify({"code": 401, "message": "Invalid email or password"})


@main_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({"message": "Logout successful"}), 200


@main_bp.route('/profile', methods=['GET'])
def profile():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        return jsonify({"user": user.to_dict()}), 200
    return jsonify({"message": "Not logged in"}), 401

@main_bp.route('/patients', methods=['POST'])
def add_patient():
    data = request.json
    new_patient = Patient(name=data['name'], age=data['age'], medical_history=data['medical_history'])
    db.session.add(new_patient)
    db.session.commit()
    return jsonify({"message": "Patient added successfully", "patient": new_patient.to_dict()}), 201


@main_bp.route('/patients', methods=['GET'])
def get_patients():
    patients = Patient.query.all()
    return jsonify({"patients": [patient.to_dict() for patient in patients]})


@main_bp.route('/diagnoses', methods=['POST'])
def add_diagnosis():
    data = request.json
    new_diagnosis = Diagnosis(patient_id=data['patient_id'], diagnosis=data['diagnosis'], date=data['date'])
    db.session.add(new_diagnosis)
    db.session.commit()
    return jsonify({"message": "Diagnosis added successfully", "diagnosis": new_diagnosis.to_dict()}), 201


@main_bp.route('/diagnoses', methods=['GET'])
def get_diagnoses():
    diagnoses = Diagnosis.query.all()
    return jsonify({"diagnoses": [diagnosis.to_dict() for diagnosis in diagnoses]})


@main_bp.route('/treatments', methods=['POST'])
def add_treatment():
    data = request.json
    new_treatment = Treatment(patient_id=data['patient_id'], treatment=data['treatment'], start_date=data['start_date'],
                              end_date=data.get('end_date'))
    db.session.add(new_treatment)
    db.session.commit()
    return jsonify({"message": "Treatment added successfully", "treatment": new_treatment.to_dict()}), 201


@main_bp.route('/treatments', methods=['GET'])
def get_treatments():
    treatments = Treatment.query.all()
    return jsonify({"treatments": [treatment.to_dict() for treatment in treatments]})
