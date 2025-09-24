# BeluTales Audio Assets

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
