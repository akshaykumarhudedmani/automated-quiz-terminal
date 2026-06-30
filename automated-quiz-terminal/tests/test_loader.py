import unittest
import os
import tempfile
import json
from src.loader import load_questions, QuestionSchemaError, get_questions_dir

class TestQuestionLoader(unittest.TestCase):
    
    def test_load_existing_categories(self):
        """Test that default categories load correctly and have proper fields."""
        categories = ["science", "math", "history", "computer_science"]
        for cat in categories:
            questions = load_questions(cat)
            self.assertIsInstance(questions, list)
            self.assertTrue(len(questions) > 0)
            
            for q in questions:
                self.assertIn("id", q)
                self.assertIn("question", q)
                self.assertIn("options", q)
                self.assertIn("answer", q)
                self.assertIn("explanation", q)
                self.assertIsInstance(q["id"], int)
                self.assertIsInstance(q["options"], list)
                self.assertTrue(len(q["options"]) >= 2)
                self.assertEqual(len(q["answer"]), 1)

    def test_load_nonexistent_category(self):
        """Test loading a non-existent category raises FileNotFoundError."""
        with self.assertRaises(FileNotFoundError):
            load_questions("non_existent_category_xyz")

    def test_invalid_json_format(self):
        """Test that invalid JSON structures raise QuestionSchemaError or ValueError."""
        # We can write a temp invalid question file in the questions folder to test
        q_dir = get_questions_dir()
        temp_file_path = os.path.join(q_dir, "temp_test_invalid.json")
        
        # Test bad structure (not a list)
        with open(temp_file_path, 'w', encoding='utf-8') as f:
            json.dump({"not_a_list": True}, f)
            
        try:
            with self.assertRaises(QuestionSchemaError):
                load_questions("temp_test_invalid")
        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

    def test_invalid_answer_option_mismatch(self):
        """Test that a schema error is raised when the answer option does not match option prefixes."""
        q_dir = get_questions_dir()
        temp_file_path = os.path.join(q_dir, "temp_test_mismatch.json")
        
        bad_data = [{
            "id": 1,
            "question": "Sample Question",
            "options": ["A) Option 1", "B) Option 2"],
            "answer": "C",
            "explanation": "No explanation"
        }]
        
        with open(temp_file_path, 'w', encoding='utf-8') as f:
            json.dump(bad_data, f)
            
        try:
            with self.assertRaises(QuestionSchemaError):
                load_questions("temp_test_mismatch")
        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

if __name__ == "__main__":
    unittest.main()
