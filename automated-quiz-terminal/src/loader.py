import os
import json

class QuestionSchemaError(Exception):
    """Custom exception raised when question JSON does not match the required schema."""
    pass

def get_questions_dir() -> str:
    """
    Returns the absolute path to the questions directory.
    
    Returns:
        str: Absolute system path to the questions folder.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    return os.path.join(project_root, "questions")

def load_questions(category: str) -> list:
    """
    Loads questions for a given category from its JSON file.
    Validates the structure of the JSON file against the expected schema.
    
    Args:
        category (str): The filename category to load (e.g. 'science').
        
    Returns:
        list: A list of validated question dictionaries.
    """
    questions_dir = get_questions_dir()
    file_path = os.path.join(questions_dir, f"{category}.json")
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Question file not found for category: '{category}' at {file_path}")
        
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON for category '{category}': {str(e)}")
        
    if not isinstance(data, list):
        raise QuestionSchemaError("Invalid JSON structure: Root element must be a list of questions.")
        
    validated_questions = []
    for idx, item in enumerate(data):
        # Validate schema fields
        for field in ["id", "question", "options", "answer", "explanation"]:
            if field not in item:
                raise QuestionSchemaError(f"Question at index {idx} is missing required field: '{field}'")
                
        if not isinstance(item["id"], (int, float)):
            raise QuestionSchemaError(f"Question at index {idx}: 'id' must be a number.")
            
        if not isinstance(item["question"], str):
            raise QuestionSchemaError(f"Question at index {idx}: 'question' must be a string.")
            
        if not isinstance(item["options"], list) or len(item["options"]) < 2:
            raise QuestionSchemaError(f"Question at index {idx}: 'options' must be a list with at least 2 choices.")
            
        for opt in item["options"]:
            if not isinstance(opt, str):
                raise QuestionSchemaError(f"Question at index {idx}: all 'options' must be strings.")
                
        if not isinstance(item["answer"], str) or len(item["answer"]) != 1:
            raise QuestionSchemaError(f"Question at index {idx}: 'answer' must be a single character string.")
            
        # Verify that the answer letter matches one of the option letter prefixes (e.g., 'A', 'B')
        option_prefixes = [opt[0].upper() for opt in item["options"] if opt and opt[0].isalpha()]
        if item["answer"].upper().strip() not in option_prefixes:
            raise QuestionSchemaError(f"Question at index {idx}: answer '{item['answer']}' must match one of the option letters: {option_prefixes}.")
            
        if not isinstance(item["explanation"], str):
            raise QuestionSchemaError(f"Question at index {idx}: 'explanation' must be a string.")
            
        validated_questions.append({
            "id": int(item["id"]),
            "question": item["question"],
            "options": item["options"],
            "answer": item["answer"].upper().strip(),
            "explanation": item["explanation"]
        })
        
    return validated_questions
