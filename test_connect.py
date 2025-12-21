#!/usr/bin/env python3
"""
Crystal Agent - Connection Verification Script

This script tests the connectivity of both Gemini AI and Notion API
to ensure the backend is production-ready.

Usage:
    python test_connect.py
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

# Load environment variables
load_dotenv()

# Import Crystal Agent modules
from config.settings import Settings
from utils.ai_brain import AIBrain
from utils.notion_handler import NotionHandler
from utils.text_analyzer import TextAnalyzer

# ANSI color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    """Print formatted header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(60)}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")

def print_success(text):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")

def print_error(text):
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")

def print_warning(text):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.RESET}")

def print_info(text):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ {text}{Colors.RESET}")

def check_env_variables():
    """Check if required environment variables are set"""
    print_header("Environment Variables Check")

    all_ok = True

    # Check Gemini API Key
    if Settings.GEMINI_API_KEY and len(Settings.GEMINI_API_KEY) > 20:
        print_success(f"GEMINI_API_KEY: Set (length: {len(Settings.GEMINI_API_KEY)})")
    else:
        print_error("GEMINI_API_KEY: Not set or invalid")
        all_ok = False

    # Check Notion API Key
    if Settings.NOTION_API_KEY and len(Settings.NOTION_API_KEY) > 20:
        print_success(f"NOTION_API_KEY: Set (length: {len(Settings.NOTION_API_KEY)})")
    else:
        print_warning("NOTION_API_KEY: Not set (Notion features will be disabled)")

    # Check Notion Database IDs
    if Settings.USER_PROFILE_DB_ID:
        print_success(f"USER_PROFILE_DB_ID: Set ({Settings.USER_PROFILE_DB_ID[:8]}...)")
    else:
        print_warning("USER_PROFILE_DB_ID: Not set")

    if Settings.LIFE_LOG_DB_ID:
        print_success(f"LIFE_LOG_DB_ID: Set ({Settings.LIFE_LOG_DB_ID[:8]}...)")
    else:
        print_warning("LIFE_LOG_DB_ID: Not set")

    # Check AI Model
    print_info(f"AI Model: {Settings.AI_MODEL}")
    print_info(f"App Version: {Settings.APP_VERSION}")
    print_info(f"Mock Mode: {Settings.MOCK_MODE}")

    return all_ok

def test_gemini_connection():
    """Test Gemini AI connection"""
    print_header("Gemini AI Connection Test")

    if not Settings.GEMINI_API_KEY:
        print_error("Gemini API Key not configured")
        return False

    try:
        print_info(f"Initializing Gemini model: {Settings.AI_MODEL}")
        ai_brain = AIBrain(Settings.GEMINI_API_KEY, Settings.AI_MODEL)
        print_success("Gemini model initialized successfully")

        # Test query
        test_message = "こんにちは！接続テストです。簡潔に挨拶を返してください。"
        print_info(f"Sending test query: {test_message}")

        response = ai_brain.generate_response(test_message)

        if response and len(response) > 5:
            print_success("Gemini AI response received successfully!")
            print(f"\n{Colors.BOLD}Response:{Colors.RESET}")
            print(f"  {response}\n")
            return True
        else:
            print_error("Gemini AI returned empty or invalid response")
            return False

    except Exception as e:
        print_error(f"Gemini AI connection failed: {str(e)}")
        print_error(f"Error type: {type(e).__name__}")
        return False

def test_notion_connection():
    """Test Notion API connection"""
    print_header("Notion API Connection Test")

    if not Settings.NOTION_API_KEY:
        print_warning("Notion API Key not configured - skipping test")
        return None  # Not a failure, just not configured

    if not Settings.LIFE_LOG_DB_ID:
        print_warning("Notion Life Log Database ID not configured - skipping test")
        return None

    try:
        print_info("Initializing Notion client...")
        print_info(f"Life Log DB ID: {Settings.LIFE_LOG_DB_ID[:8]}...")

        notion = NotionHandler(
            Settings.NOTION_API_KEY,
            Settings.USER_PROFILE_DB_ID,
            Settings.LIFE_LOG_DB_ID
        )

        if notion.is_connected:
            print_success("Notion API connection successful!")

            # Test writing to Notion
            test_content = f"[TEST] Connection verification at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            print_info(f"Writing test log: {test_content}")

            success = notion.add_life_log(
                content=test_content,
                type_="日記",
                emotion="普通"
            )

            if success:
                print_success("Test log written to Notion successfully!")
                print_info("Check your Notion database to see the test entry")
                return True
            else:
                print_error("Failed to write test log to Notion")
                return False
        else:
            print_error("Notion API connection failed during initialization")
            return False

    except Exception as e:
        print_error(f"Notion API connection failed: {str(e)}")
        print_error(f"Error type: {type(e).__name__}")
        return False

def test_text_analyzer():
    """Test Text Analyzer functionality"""
    print_header("Text Analyzer Test")

    try:
        analyzer = TextAnalyzer()
        print_success("Text Analyzer initialized")

        # Test cases
        test_cases = [
            ("今日はランチで1500円使った", "支出", 1500.0),
            ("明日までにレポートを書かなきゃ", "タスク", None),
            ("仕事がつらくて不安", "悩み", None),
            ("今日は楽しかった！", "日記", None),
        ]

        passed = 0
        total = len(test_cases)

        for text, expected_type, expected_amount in test_cases:
            result = analyzer.analyze(text)
            detected_type = result.get('type')
            detected_amount = result.get('amount')

            type_match = detected_type == expected_type
            amount_match = detected_amount == expected_amount

            if type_match and amount_match:
                print_success(f"'{text}' → {detected_type} (Amount: {detected_amount})")
                passed += 1
            else:
                print_warning(f"'{text}' → Expected: {expected_type}, Got: {detected_type}")

        accuracy = (passed / total) * 100
        print_info(f"\nAccuracy: {accuracy:.1f}% ({passed}/{total} tests passed)")

        if accuracy >= 75:
            print_success("Text Analyzer is working correctly")
            return True
        else:
            print_warning("Text Analyzer accuracy is below expected threshold")
            return False

    except Exception as e:
        print_error(f"Text Analyzer test failed: {str(e)}")
        return False

def test_integration():
    """Test full integration: Analyze → Gemini → Notion"""
    print_header("Full Integration Test")

    if not Settings.GEMINI_API_KEY:
        print_warning("Skipping integration test (Gemini not configured)")
        return None

    try:
        # Initialize modules
        analyzer = TextAnalyzer()
        ai_brain = AIBrain(Settings.GEMINI_API_KEY, Settings.AI_MODEL)

        # Test message
        test_message = "今日は1200円のランチを食べました。美味しかったです！"
        print_info(f"Test message: {test_message}")

        # Step 1: Analyze
        analysis = analyzer.analyze(test_message)
        print_success(f"Analysis: Type={analysis['type']}, Amount={analysis.get('amount')}, Emotion={analysis['emotion']}")

        # Step 2: Get AI response
        ai_response = ai_brain.generate_response(test_message)
        print_success(f"AI Response: {ai_response}")

        # Step 3: Save to Notion (if configured)
        if Settings.NOTION_API_KEY and Settings.LIFE_LOG_DB_ID:
            notion = NotionHandler(
                Settings.NOTION_API_KEY,
                Settings.USER_PROFILE_DB_ID,
                Settings.LIFE_LOG_DB_ID
            )

            if notion.is_connected:
                success = notion.add_life_log(
                    content=test_message,
                    type_=analysis['type'],
                    amount=analysis.get('amount'),
                    emotion=analysis['emotion']
                )

                if success:
                    print_success("Integration test: Full pipeline successful!")
                    return True
                else:
                    print_warning("Integration test: AI works, but Notion save failed")
                    return False
            else:
                print_warning("Integration test: AI works, Notion not connected")
                return True  # Still a success if AI works
        else:
            print_success("Integration test: AI pipeline successful (Notion not configured)")
            return True

    except Exception as e:
        print_error(f"Integration test failed: {str(e)}")
        return False

def main():
    """Main test execution"""
    print("\n")
    print(f"{Colors.BOLD}{Colors.BLUE}🔮 Crystal Agent - Connection Verification{Colors.RESET}")
    print(f"{Colors.BLUE}Version: {Settings.APP_VERSION}{Colors.RESET}")
    print(f"{Colors.BLUE}Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.RESET}")

    results = {}

    # Run all tests
    results['env'] = check_env_variables()
    results['gemini'] = test_gemini_connection()
    results['notion'] = test_notion_connection()
    results['analyzer'] = test_text_analyzer()
    results['integration'] = test_integration()

    # Summary
    print_header("Test Summary")

    total_tests = 0
    passed_tests = 0

    for test_name, result in results.items():
        if result is None:
            print_warning(f"{test_name.capitalize()}: Skipped (not configured)")
        elif result:
            print_success(f"{test_name.capitalize()}: PASSED")
            passed_tests += 1
            total_tests += 1
        else:
            print_error(f"{test_name.capitalize()}: FAILED")
            total_tests += 1

    print(f"\n{Colors.BOLD}Results: {passed_tests}/{total_tests} tests passed{Colors.RESET}\n")

    if passed_tests == total_tests and total_tests > 0:
        print(f"{Colors.GREEN}{Colors.BOLD}✓ SUCCESS: All configured tests passed!{Colors.RESET}")
        print(f"{Colors.GREEN}Crystal Agent is production-ready! 🚀{Colors.RESET}\n")
        return 0
    elif passed_tests > 0:
        print(f"{Colors.YELLOW}{Colors.BOLD}⚠ PARTIAL: Some tests passed, but check warnings above{Colors.RESET}\n")
        return 1
    else:
        print(f"{Colors.RED}{Colors.BOLD}✗ FAILED: Critical tests failed. Check errors above{Colors.RESET}\n")
        return 2

if __name__ == "__main__":
    sys.exit(main())
