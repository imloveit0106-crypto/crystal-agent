"""TextAnalyzer のテスト"""
import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.text_analyzer import TextAnalyzer

class TestTextAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = TextAnalyzer()

    def test_detect_type_expense(self):
        result = self.analyzer.detect_type("ランチで1000円使った")
        self.assertEqual(result, "支出")

    def test_detect_emotion_good(self):
        result = self.analyzer.detect_emotion("今日は嬉しい")
        self.assertEqual(result, "良好")

if __name__ == '__main__':
    unittest.main()
