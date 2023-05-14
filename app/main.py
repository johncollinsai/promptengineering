import random
import asyncio

from flask import Blueprint, render_template, request, jsonify
from .completions import generate_gpt4_response_raw, generate_gpt4_response_engineered, get_api_key

bp = Blueprint("main", __name__)

@bp.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@bp.route('/get_raw_response', methods=["POST"])
def get_raw_response():
    try:
        prompt = request.form['prompt']
        api_key = get_api_key()

        # Generate response for the raw modality
        raw_response = generate_gpt4_response_raw(prompt, api_key)

        return jsonify({"success": True, "response": raw_response})
    
    except ValueError as e:
        # jsonify() converts Python dictionary to JSON for the specific modality
        return jsonify({"success": False, "error": str(e)})


@bp.route('/get_engineered_response', methods=["POST"])
def get_engineered_response():
    try:
        prompt = request.form['prompt']
        api_key = get_api_key()

        # Generate response for the engineered modality
        engineered_response = generate_gpt4_response_engineered(prompt, api_key)

        return jsonify({"success": True, "response": engineered_response})
    
    except ValueError as e:
        # jsonify() converts Python dictionary to JSON for the specific modality
        return jsonify({"success": False, "error": str(e)})
