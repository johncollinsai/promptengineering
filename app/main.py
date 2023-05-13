import random
import asyncio

from flask import Blueprint, render_template, request, jsonify
from .completions import generate_gpt4_response, get_api_key

bp = Blueprint("main", __name__)

@bp.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@bp.route('/get_completion', methods=["POST"])
async def get_completion():
    try:
        prompt = request.form['prompt']
        api_key = get_api_key()

        # Generate responses for the both modalities
        raw_response = await generate_gpt4_response(prompt, "raw", api_key)
        engineered_response = await generate_gpt4_response(prompt, "engineered", api_key)

        response = {
            'raw': raw_response,
            'engineered': engineered_response
        }

        return jsonify({"success": True, "response": response})
    
    except ValueError as e:
        # jsonify() converts Python dictionary to JSON for the specific modality
        return jsonify({"success": False, "error": str(e)})



