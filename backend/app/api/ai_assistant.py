from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from app.services.ai_service import DeepseekAPIService
from app.services.document_service import DocumentAnalysisService

ai = Blueprint('ai', __name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

@ai.route('/analyze-document', methods=['POST'])
def analyze_document():
    """
    Analyze uploaded courseware document.
    Expects: multipart/form-data with 'file' field
    Returns: JSON with analysis results
    """
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Only .docx files are supported'}), 400
        
        # Create upload directory if it doesn't exist
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        
        # Save file securely
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        try:
            # Analyze document
            doc_service = DocumentAnalysisService()
            text_content = doc_service.extract_text_from_docx(filepath)
            analysis = doc_service.analyze_document(text_content)
            
            return jsonify({
                'success': True,
                'analysis': analysis
            }), 200
            
        finally:
            # Clean up uploaded file
            if os.path.exists(filepath):
                os.remove(filepath)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
