from flask import Blueprint, request, jsonify
from app.services.ai_service import DeepseekAPIService

ai = Blueprint('ai', __name__)

@ai.route('/chat', methods=['POST'])
def chat():
    """
    Handle chat requests to the AI assistant.
    Expects JSON: {"message": "user's question"}
    Returns JSON: {"response": "AI's answer"}
    """
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Call DeepSeek API
        ai_service = DeepseekAPIService()
        response = ai_service.generate_text(user_message)
        
        return jsonify({'response': response}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
