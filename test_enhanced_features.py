# test_enhanced_features.py — Test script for BeluTales enhanced features

import os
import sys
import json
from pathlib import Path

def test_component_imports():
    """Test if enhanced components can be imported"""
    print("🧪 Testing Component Imports...")
    
    try:
        from components.audio_manager import get_audio_manager, play_click_sound, play_success_sound
        print("✅ Audio Manager imported successfully")
    except ImportError as e:
        print(f"❌ Audio Manager import failed: {e}")
        return False
    
    try:
        from components.quiz_enhanced import render_quiz_enhanced, get_quiz_progress
        print("✅ Enhanced Quiz imported successfully")
    except ImportError as e:
        print(f"❌ Enhanced Quiz import failed: {e}")
        return False
    
    try:
        from components.settings_panel import render_settings_panel, render_settings_button
        print("✅ Settings Panel imported successfully")
    except ImportError as e:
        print(f"❌ Settings Panel import failed: {e}")
        return False
    
    return True

def test_audio_files():
    """Test if required audio files exist"""
    print("\n🔊 Testing Audio Files...")
    
    audio_dir = Path("audio")
    if not audio_dir.exists():
        print("❌ Audio directory does not exist")
        return False
    
    required_audio_files = [
        "click.mp3",
        "success.mp3", 
        "error.mp3",
        "notification.mp3",
        "button_hover.mp3",
        "page_turn.mp3",
        "quiz_complete.mp3",
        "perfect_score.mp3",
        "ambience_forest.mp3",
        "ambience_rain.mp3",
        "ambience_ocean.mp3",
        "ambience_night.mp3",
        "ambience_birds.mp3"
    ]
    
    missing_files = []
    existing_files = []
    
    for audio_file in required_audio_files:
        file_path = audio_dir / audio_file
        if file_path.exists():
            existing_files.append(audio_file)
            print(f"✅ {audio_file}")
        else:
            missing_files.append(audio_file)
            print(f"❌ {audio_file} (missing)")
    
    print(f"\nAudio Files Summary:")
    print(f"✅ Existing: {len(existing_files)}/{len(required_audio_files)}")
    print(f"❌ Missing: {len(missing_files)}")
    
    if missing_files:
        print(f"Missing files: {', '.join(missing_files)}")
        print("ℹ️  Run 'python create_audio_assets.py' to create placeholder files")
    
    return len(missing_files) == 0

def test_quiz_data():
    """Test if quiz data is available"""
    print("\n🧠 Testing Quiz Data...")
    
    quiz_file = Path("archive/quizzes.json")
    if not quiz_file.exists():
        print("❌ Quiz data file does not exist (archive/quizzes.json)")
        return False
    
    try:
        with open(quiz_file, "r", encoding="utf-8") as f:
            quiz_data = json.load(f)
        
        print(f"✅ Quiz data loaded successfully")
        print(f"📊 Available quizzes: {len(quiz_data)}")
        
        # Test a few quiz entries
        sample_stories = list(quiz_data.keys())[:3]
        for story_slug in sample_stories:
            quiz = quiz_data[story_slug]
            print(f"  - {story_slug}: {len(quiz)} questions")
            
            # Validate quiz structure
            for i, q in enumerate(quiz[:1]):  # Check first question
                required_fields = ["question", "options", "answer"]
                missing_fields = [field for field in required_fields if field not in q]
                if missing_fields:
                    print(f"    ⚠️  Question {i+1} missing fields: {missing_fields}")
                else:
                    print(f"    ✅ Question {i+1} structure valid")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Quiz data JSON decode error: {e}")
        return False
    except Exception as e:
        print(f"❌ Quiz data loading error: {e}")
        return False

def test_story_data():
    """Test if story data is available"""
    print("\n📚 Testing Story Data...")
    
    stories_file = Path("stories.json")
    if not stories_file.exists():
        print("❌ Stories data file does not exist (stories.json)")
        return False
    
    try:
        with open(stories_file, "r", encoding="utf-8") as f:
            stories_data = json.load(f)
        
        if isinstance(stories_data, list):
            stories = stories_data
        elif isinstance(stories_data, dict) and "stories" in stories_data:
            stories = stories_data["stories"]
        else:
            print("❌ Invalid stories data structure")
            return False
        
        print(f"✅ Stories data loaded successfully")
        print(f"📖 Available stories: {len(stories)}")
        
        # Check for required fields
        required_fields = ["title", "slug"]
        stories_with_issues = 0
        
        for i, story in enumerate(stories[:5]):  # Check first 5 stories
            missing_fields = [field for field in required_fields if field not in story]
            if missing_fields:
                print(f"  ⚠️  Story {i+1} missing fields: {missing_fields}")
                stories_with_issues += 1
            else:
                print(f"  ✅ Story: {story.get('title', 'Unknown')}")
        
        if stories_with_issues > 0:
            print(f"⚠️  {stories_with_issues} stories have structural issues")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Stories data JSON decode error: {e}")
        return False
    except Exception as e:
        print(f"❌ Stories data loading error: {e}")
        return False

def test_dependencies():
    """Test if required Python packages are available"""
    print("\n📦 Testing Dependencies...")
    
    required_packages = [
        "streamlit",
        "PIL",
        "pathlib",
        "json",
        "requests",
        "uuid"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == "PIL":
                import PIL
            else:
                __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} (missing)")
            missing_packages.append(package)
    
    # Test optional packages
    optional_packages = {
        "gtts": "Text-to-speech functionality",
        "deep_translator": "Translation functionality"
    }
    
    print("\n📦 Optional Dependencies:")
    for package, description in optional_packages.items():
        try:
            __import__(package)
            print(f"✅ {package} - {description}")
        except ImportError:
            print(f"⚠️  {package} - {description} (optional, not required)")
    
    return len(missing_packages) == 0

def test_file_structure():
    """Test if all required files and directories exist"""
    print("\n📁 Testing File Structure...")
    
    required_structure = {
        "files": [
            "app.py",
            "languages.py",
            "requirements.txt",
            "stories.json"
        ],
        "directories": [
            "components",
            "audio",
            "images",
            "archive"
        ]
    }
    
    missing_items = []
    
    # Check files
    for file_name in required_structure["files"]:
        file_path = Path(file_name)
        if file_path.exists():
            print(f"✅ {file_name}")
        else:
            print(f"❌ {file_name} (missing)")
            missing_items.append(file_name)
    
    # Check directories
    for dir_name in required_structure["directories"]:
        dir_path = Path(dir_name)
        if dir_path.exists() and dir_path.is_dir():
            print(f"✅ {dir_name}/")
        else:
            print(f"❌ {dir_name}/ (missing)")
            missing_items.append(f"{dir_name}/")
    
    return len(missing_items) == 0

def run_comprehensive_test():
    """Run all tests and provide summary"""
    print("🚀 BeluTales Enhanced Features - Comprehensive Test")
    print("=" * 60)
    
    test_results = {
        "Component Imports": test_component_imports(),
        "File Structure": test_file_structure(),
        "Dependencies": test_dependencies(),
        "Story Data": test_story_data(),
        "Quiz Data": test_quiz_data(),
        "Audio Files": test_audio_files()
    }
    
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<20} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Enhanced features are ready to use.")
        print("\nNext steps:")
        print("1. Start the app: streamlit run app.py")
        print("2. Test enhanced features in the web interface")
        print("3. Replace placeholder audio files with actual content")
        print("4. Configure settings through the Settings panel")
    else:
        print("⚠️  Some tests failed. Please address the issues above.")
        print("\nCommon solutions:")
        print("- Run: python create_audio_assets.py")
        print("- Check that all component files are in components/ directory")
        print("- Verify stories.json and archive/quizzes.json exist")
        print("- Install missing dependencies: pip install -r requirements.txt")
    
    return passed == total

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)
