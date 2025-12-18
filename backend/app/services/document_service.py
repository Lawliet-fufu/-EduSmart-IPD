import os
from docx import Document
from flask import current_app
from app.services.ai_service import DeepseekAPIService

class DocumentAnalysisService:
    """
    Service for analyzing educational documents using DeepSeek AI.
    """
    
    def __init__(self):
        self.ai_service = DeepseekAPIService()
    
    def extract_text_from_docx(self, file_path):
        """
        Extract text content from a .docx file.
        
        Args:
            file_path (str): Path to the .docx file
            
        Returns:
            str: Extracted text content
        """
        try:
            doc = Document(file_path)
            full_text = []
            
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    full_text.append(paragraph.text)
            
            return '\n'.join(full_text)
        except Exception as e:
            current_app.logger.error(f"Error extracting text from docx: {str(e)}")
            raise
    
    def analyze_document(self, text_content):
        """
        Analyze document content and extract educational insights.
        
        Args:
            text_content (str): The document text to analyze
            
        Returns:
            dict: Analysis results with key_topics, learning_objectives, and activities
        """
        # Create analysis prompt
        analysis_prompt = f"""
Analyze the following educational courseware content and provide:

1. Key Topics: List 3-5 main topics covered
2. Learning Objectives: List 3-5 specific learning objectives
3. Suggested Activities: List 3-5 teaching activities that would complement this content

Format your response as JSON with these exact keys:
- key_topics: array of strings
- learning_objectives: array of strings
- suggested_activities: array of strings

Content to analyze:
{text_content[:3000]}  

Provide ONLY the JSON response, no additional text.
"""
        
        try:
            # Get AI analysis
            response = self.ai_service.generate_text(analysis_prompt)
            
            # Debug: Log the response
            current_app.logger.info(f"AI Response: {response}")
            print(f"\n=== AI RESPONSE ===\n{response}\n===================\n")
            
            # Parse JSON response
            import json
            try:
                analysis = json.loads(response)
                return {
                    'key_topics': analysis.get('key_topics', []),
                    'learning_objectives': analysis.get('learning_objectives', []),
                    'suggested_activities': analysis.get('suggested_activities', [])
                }
            except json.JSONDecodeError as e:
                current_app.logger.warning(f"JSON decode failed: {e}, using fallback parser")
                print(f"JSON decode failed, using fallback parser")
                # Fallback: parse text response
                return self._parse_text_response(response)
                
        except Exception as e:
            current_app.logger.error(f"Error analyzing document: {str(e)}")
            raise
    
    def _parse_text_response(self, response):
        """
        Fallback parser for non-JSON responses.
        """
        lines = response.split('\n')
        result = {
            'key_topics': [],
            'learning_objectives': [],
            'suggested_activities': []
        }
        
        current_section = None
        for line in lines:
            line = line.strip()
            
            # Detect section headers
            line_lower = line.lower()
            if 'key topic' in line_lower:
                current_section = 'key_topics'
                continue
            elif 'learning objective' in line_lower:
                current_section = 'learning_objectives'
                continue
            elif ('suggested activit' in line_lower or 
                  'teaching activit' in line_lower or
                  'recommended activit' in line_lower):
                current_section = 'suggested_activities'
                continue
            
            # Extract list items
            if line and current_section:
                # Check if it's a list item (starts with -, •, number, or *)
                if (line.startswith('-') or 
                    line.startswith('•') or 
                    line.startswith('*') or
                    (len(line) > 0 and line[0].isdigit() and '.' in line[:3])):
                    # Clean the line
                    clean_line = line.lstrip('-•*0123456789. ').strip()
                    if clean_line and len(clean_line) > 3:  # Avoid very short items
                        result[current_section].append(clean_line)
        
        # Debug output
        print(f"\n=== PARSED RESULT ===")
        print(f"Key Topics: {result['key_topics']}")
        print(f"Learning Objectives: {result['learning_objectives']}")
        print(f"Suggested Activities: {result['suggested_activities']}")
        print(f"=====================\n")
        
        return result
