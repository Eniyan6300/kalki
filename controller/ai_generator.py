"""
AI Question Generator using OpenRouter API
Generates quiz questions using Claude AI
"""

import requests
import json
from config import Config

class AIQuestionGenerator:
    def __init__(self):
        self.api_key = Config.OPENROUTER_API_KEY
        self.model = Config.OPENROUTER_MODEL
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
    
    def generate_mcq_questions(self, topic: str, num_questions: int) -> list:
        """
        Generate MCQ questions for a given topic
        
        Args:
            topic: The topic/heading for questions
            num_questions: Number of questions to generate
        
        Returns:
            List of question dictionaries with options and correct answer
        """
        
        if not self.api_key:
            raise ValueError("OpenRouter API key not configured. Set OPENROUTER_API_KEY environment variable.")
        
        prompt = f"""Generate {num_questions} multiple choice questions about "{topic}". 
        
For each question, provide:
1. Question text
2. Exactly 4 options (A, B, C, D)
3. The correct answer (A, B, C, or D)
4. The marks (default 1)

Format your response as a JSON array like this:
[
  {{
    "question_text": "What is...?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct_answer": "A",
    "marks": 1
  }}
]

Only return valid JSON array, no other text."""

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {{
                        "role": "user",
                        "content": prompt
                    }}
                ],
                "temperature": 0.7,
                "max_tokens": 4000
            }
            
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if "choices" not in data or len(data["choices"]) == 0:
                raise ValueError("No response from API")
            
            content = data["choices"][0]["message"]["content"]
            
            # Extract JSON from response
            questions = self._parse_questions(content)
            
            return questions
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"API Request failed: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse AI response: {str(e)}")
    
    def _parse_questions(self, response_text: str) -> list:
        """
        Parse AI response to extract questions
        """
        try:
            # Try to extract JSON from response
            start_idx = response_text.find('[')
            end_idx = response_text.rfind(']') + 1
            
            if start_idx == -1 or end_idx == 0:
                raise ValueError("No JSON array found in response")
            
            json_str = response_text[start_idx:end_idx]
            questions = json.loads(json_str)
            
            # Validate questions
            validated = []
            for q in questions:
                if all(key in q for key in ['question_text', 'options', 'correct_answer']):
                    # Ensure correct_answer is index (0-3) not letter (A-D)
                    correct = q.get('correct_answer', 'A')
                    if isinstance(correct, str) and correct.upper() in ['A', 'B', 'C', 'D']:
                        correct = ord(correct.upper()) - ord('A')
                    
                    validated.append({
                        'question_text': q['question_text'],
                        'options': q['options'],
                        'correct_answer_index': int(correct),
                        'marks': q.get('marks', 1)
                    })
            
            return validated
            
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            raise Exception(f"Invalid question format: {str(e)}")


def generate_questions(topic: str, num_questions: int) -> dict:
    """
    Wrapper function to generate questions
    
    Returns:
        {
            'success': bool,
            'questions': list or None,
            'error': str or None
        }
    """
    try:
        generator = AIQuestionGenerator()
        questions = generator.generate_mcq_questions(topic, num_questions)
        
        if not questions:
            return {
                'success': False,
                'questions': None,
                'error': 'No questions generated'
            }
        
        return {
            'success': True,
            'questions': questions,
            'error': None
        }
        
    except Exception as e:
        return {
            'success': False,
            'questions': None,
            'error': str(e)
        }
