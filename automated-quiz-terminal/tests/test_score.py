import unittest
import os
import json
import tempfile
from src.score import calculate_score, load_highscores, save_highscore, get_highscores_path

class TestScoreCalculations(unittest.TestCase):
    
    def test_calculate_score_incorrect(self):
        """Incorrect answers should always yield 0 points."""
        score = calculate_score(correct=False, time_remaining=10, total_time=20, streak=3)
        self.assertEqual(score, 0)
        
    def test_calculate_score_base(self):
        """Correct answer without timer or streak should yield base 100 points."""
        score = calculate_score(correct=True, time_remaining=0, total_time=0, streak=1)
        self.assertEqual(score, 100)

    def test_calculate_score_speed_bonus(self):
        """Speed bonus increases score when answering fast."""
        # 10 seconds remaining of 20 seconds total = 50% remaining.
        # Speed bonus = 50% of 50 = 25 points. Total = 100 + 25 = 125.
        score = calculate_score(correct=True, time_remaining=10, total_time=20, streak=1)
        self.assertEqual(score, 125)

    def test_calculate_score_streak_multiplier(self):
        """Streak multiplier should increase scores proportionally."""
        # Streak 2: multiplier is 1.1x. Base 100 * 1.1 = 110.
        score_s2 = calculate_score(correct=True, time_remaining=0, total_time=0, streak=2)
        self.assertEqual(score_s2, 110)
        
        # Streak 3: multiplier is 1.2x. Base 100 * 1.2 = 120.
        score_s3 = calculate_score(correct=True, time_remaining=0, total_time=0, streak=3)
        self.assertEqual(score_s3, 120)

    def test_highscore_load_save(self):
        """Test highscore list serialization and retrieval."""
        # Load current highscores to verify it functions
        highscores = load_highscores()
        self.assertIsInstance(highscores, dict)
        self.assertIn("science", highscores)
        
        # Save a test score
        test_category = "science"
        save_highscore(test_category, "TestPlayer", 9999, 10)
        
        # Reload and check
        updated_scores = load_highscores()
        matching_entry = None
        for entry in updated_scores.get(test_category, []):
            if entry["name"] == "TestPlayer" and entry["score"] == 9999:
                matching_entry = entry
                break
                
        self.assertIsNotNone(matching_entry)
        self.assertEqual(matching_entry["max_streak"], 10)
        
        # Clean up by removing the test entry
        highscores = load_highscores()
        if test_category in highscores:
            highscores[test_category] = [e for e in highscores[test_category] if not (e["name"] == "TestPlayer" and e["score"] == 9999)]
        
        path = get_highscores_path()
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(highscores, f, indent=2)

if __name__ == "__main__":
    unittest.main()
