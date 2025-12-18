import os
from openai import OpenAI
from flask import current_app

class DeepseekAPIService:
    """
    Service layer for handling external API calls to Deepseek (LLM).
    """
    def __init__(self):
        api_key = os.getenv('DEEPSEEK_API_KEY')
        if not api_key:
            current_app.logger.warning('DEEPSEEK_API_KEY not found in environment variables')
        
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )

    def generate_text(self, prompt):
        """
        Generate text response from DeepSeek API.
        
        Args:
            prompt (str): User's input message
            
        Returns:
            str: The AI's response.
        """
        # System prompt: Restrict domain to education and ENFORCE ENGLISH responses
        system_prompt = (
            "You are a professional educational AI assistant specialized in teaching design, student management, and course analysis."
            "You MUST ALWAYS answer in ENGLISH."
            "Only answer questions related to education, teaching, learning, and school management."
            "If the user asks about non-educational topics (e.g., entertainment, sports), politely refuse and guide them back to educational topics."
            "Your tone should be professional, encouraging, and helpful."
        )

        messages = [{"role": "system", "content": system_prompt}]
        messages.append({"role": "user", "content": prompt})

        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,
                stream=False
            )
            return response.choices[0].message.content
        except Exception as e:
            current_app.logger.error(f"DeepSeek API error: {str(e)}")
            return "I apologize, but I'm currently unable to process your request. Please try again later."
