import unittest
from unittest.mock import patch, MagicMock
from src.quiz import run_quiz

class TestQuizFlow(unittest.TestCase):
    
    @patch('src.quiz.safe_input')
    @patch('src.quiz.get_choice_with_timeout')
    @patch('src.quiz.save_highscore')
    @patch('src.quiz.log_incorrect_answer')
    @patch('src.quiz.display_leaderboard')
    def test_run_quiz_perfect_score(self, mock_leaderboard, mock_log, mock_save, mock_choice, mock_input):
        """Test a complete quiz where all questions are answered correctly."""
        # Mock inputs: 
        # 1. Player Name: "QuizMaster"
        # 2. Start game: Enter
        # 3. Next questions (after each): Enter
        # 4. View Leaderboard after summary: "N"
        mock_input.side_effect = ["QuizMaster", "", "", "", "n"]
        
        # Mock choice: Return 'A' every time (which we will make the correct answer)
        mock_choice.return_value = 'A'
        
        # Setup mock questions
        mock_questions = [
            {
                "id": 1,
                "question": "Q1",
                "options": ["A) OptA", "B) OptB"],
                "answer": "A",
                "explanation": "Exp1"
            },
            {
                "id": 2,
                "question": "Q2",
                "options": ["A) OptA", "B) OptB"],
                "answer": "A",
                "explanation": "Exp2"
            }
        ]
        
        # Run the quiz (limit 10s)
        run_quiz("science", mock_questions, time_limit=10)
        
        # Verify high score was saved
        mock_save.assert_called_once()
        args, kwargs = mock_save.call_args
        self.assertEqual(args[0], "science") # category
        self.assertEqual(args[1], "QuizMaster") # name
        self.assertTrue(args[2] > 0) # score > 0
        self.assertEqual(args[3], 2) # max_streak = 2
        
        # Log incorrect should not be called since we got all correct
        mock_log.assert_not_called()

    @patch('src.quiz.safe_input')
    @patch('src.quiz.get_choice_with_timeout')
    @patch('src.quiz.save_highscore')
    @patch('src.quiz.log_incorrect_answer')
    @patch('src.quiz.display_leaderboard')
    def test_run_quiz_with_incorrect_and_timeout(self, mock_leaderboard, mock_log, mock_save, mock_choice, mock_input):
        """Test quiz flow when user answers wrong and times out."""
        # Mock inputs
        mock_input.side_effect = ["BadPlayer", "", "", "", "n"]
        
        # Mock choices:
        # Question 1: User chooses 'B' (Incorrect - correct is A)
        # Question 2: None (Timeout)
        mock_choice.side_effect = ['B', None]
        
        mock_questions = [
            {
                "id": 1,
                "question": "Q1",
                "options": ["A) OptA", "B) OptB"],
                "answer": "A",
                "explanation": "Exp1"
            },
            {
                "id": 2,
                "question": "Q2",
                "options": ["A) OptA", "B) OptB"],
                "answer": "A",
                "explanation": "Exp2"
            }
        ]
        
        run_quiz("math", mock_questions, time_limit=10)
        
        # Check that high score is saved with 0 points and 0 max streak
        mock_save.assert_called_once_with("math", "BadPlayer", 0, 0)
        
        # Check that both questions were logged as incorrect
        self.assertEqual(mock_log.call_count, 2)
        mock_log.assert_any_call("math", mock_questions[0])
        mock_log.assert_any_call("math", mock_questions[1])

    @patch('src.quiz.safe_input')
    @patch('src.quiz.save_highscore')
    @patch('src.quiz.display_leaderboard')
    def test_run_quiz_empty_questions(self, mock_leaderboard, mock_save, mock_input):
        """Test quiz summary outputs correctly without crash when questions list is empty."""
        mock_input.side_effect = ["EmptyPlayer", "", "n"]
        
        # Run quiz with empty list
        run_quiz("science", [], time_limit=10)
        
        # Highscore should be saved with 0 score and 0 streak
        mock_save.assert_called_once_with("science", "EmptyPlayer", 0, 0)

if __name__ == "__main__":
    unittest.main()
