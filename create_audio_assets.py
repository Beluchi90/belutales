# create_audio_assets.py — Create missing audio assets for enhanced BeluTales
import os
from pathlib import Path

def create_placeholder_audio_files():
    """Create placeholder audio files for sound effects"""
    
    audio_dir = Path("audio")
    audio_dir.mkdir(exist_ok=True)
    
    # List of sound effects we need
    sound_effects = [
        "success",
        "error", 
        "notification",
        "button_hover",
        "page_turn",
        "quiz_complete",
        "perfect_score"
    ]
    
    # List of ambience tracks
    ambience_tracks = [
        "ambience_forest",
        "ambience_rain", 
        "ambience_ocean",
        "ambience_night",
        "ambience_birds"
    ]
    
    print("Creating placeholder audio files...")
    
    # Create placeholder files if they don't exist
    all_audio_files = sound_effects + ambience_tracks
    
    for audio_file in all_audio_files:
        file_path = audio_dir / f"{audio_file}.mp3"
        if not file_path.exists():
            # Create an empty placeholder file
            file_path.touch()
            print(f"Created placeholder: {file_path}")
        else:
            print(f"Already exists: {file_path}")
    
    # Create a simple HTML file to test audio functionality
    test_html = """
<!DOCTYPE html>
<html>
<head>
    <title>BeluTales Audio Test</title>
</head>
<body>
    <h1>BeluTales Audio Test</h1>
    <p>This page can be used to test audio functionality locally.</p>
    
    <h2>Sound Effects</h2>
"""
    
    for effect in sound_effects:
        test_html += f"""
    <button onclick="playSound('{effect}')">Play {effect}</button><br>
"""
    
    test_html += """
    
    <h2>Ambience Tracks</h2>
"""
    
    for track in ambience_tracks:
        test_html += f"""
    <button onclick="playSound('{track}')">Play {track.replace('ambience_', '')}</button><br>
"""
    
    test_html += """
    
    <script>
    function playSound(soundName) {
        const audio = new Audio(`audio/${soundName}.mp3`);
        audio.play().catch(e => {
            console.log('Audio play prevented or file missing:', e);
            alert(`Audio file audio/${soundName}.mp3 not found or browser prevented playback`);
        });
    }
    </script>
</body>
</html>
"""
    
    # Write test HTML file
    test_file = Path("audio_test.html")
    with open(test_file, "w") as f:
        f.write(test_html)
    
    print(f"Created audio test file: {test_file}")
    print("\nNote: These are placeholder files. For production, replace with actual audio content.")
    print("You can test audio functionality by opening audio_test.html in a web browser.")

def create_readme():
    """Create README for audio assets"""
    readme_content = """# BeluTales Audio Assets

This directory contains audio files for the BeluTales application.

## Sound Effects

- `click.mp3` - Button click sound (already exists)
- `success.mp3` - Success notification (quiz correct answer)
- `error.mp3` - Error notification (quiz wrong answer)
- `notification.mp3` - General notification sound
- `button_hover.mp3` - Button hover effect
- `page_turn.mp3` - Page transition sound
- `quiz_complete.mp3` - Quiz completion sound
- `perfect_score.mp3` - Perfect quiz score celebration

## Ambience Tracks

- `ambience_forest.mp3` - Forest sounds (birds, rustling leaves)
- `ambience_rain.mp3` - Gentle rain sounds
- `ambience_ocean.mp3` - Ocean waves and seagulls
- `ambience_night.mp3` - Crickets and night sounds
- `ambience_birds.mp3` - Various bird songs

## Story Narration

Story narration files are automatically generated using TTS and stored with naming pattern:
`{story-slug}_{language-code}.mp3`

## File Format Requirements

- Format: MP3 (preferred) or WAV
- Sample Rate: 44.1 kHz recommended
- Bit Rate: 128 kbps minimum for speech, 256 kbps for music/ambience
- Duration: 
  - Sound effects: 0.5-2 seconds
  - Ambience: 30-60 seconds (designed to loop)
  - Narration: Variable based on story length

## Implementation Notes

- All audio files should be optimized for web delivery
- Consider creating OGG Vorbis alternatives for better browser compatibility
- Ambience tracks should be designed to loop seamlessly
- Volume levels should be normalized across all files
- Consider fade-in/fade-out for ambience tracks

## Licensing

Ensure all audio content is properly licensed for distribution.
Consider using royalty-free or Creative Commons licensed content.

## Sources for Audio Content

### Free Resources:
- Freesound.org (CC licensed)
- OpenGameArt.org
- Incompetech.com (Kevin MacLeod)
- Zapsplat.com (free tier available)

### Sound Effect Libraries:
- BBC Sound Effects Library
- YouTube Audio Library
- Adobe Audition built-in sounds

### Text-to-Speech:
- Google Text-to-Speech (gTTS) - already implemented
- Amazon Polly
- Azure Cognitive Services Speech
"""
    
    readme_file = Path("audio") / "README.md"
    with open(readme_file, "w") as f:
        f.write(readme_content)
    
    print(f"Created audio README: {readme_file}")

if __name__ == "__main__":
    create_placeholder_audio_files()
    create_readme()
    
    print("\nAudio asset setup complete!")
    print("Next steps:")
    print("1. Replace placeholder MP3 files with actual audio content")
    print("2. Test audio functionality using audio_test.html")
    print("3. Adjust volume levels in the settings panel")
    print("4. Consider adding more sound effects based on user feedback")
