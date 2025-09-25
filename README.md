# BeluTales 📚

A magical children's story platform built with Streamlit, featuring interactive stories, audio narration, translations, and quizzes.

## Features

- 📖 Interactive story reading with beautiful styling
- 🎵 Audio narration support
- 🌍 Multi-language translation
- 🧩 Interactive quizzes
- 🔐 User authentication and story gating
- ✨ Magical UI with gradient backgrounds and animations

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Beluchi90/belutales.git
cd belutales
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the App

To run the BeluTales app locally:

```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

The app will be available at:
- Local URL: http://localhost:8501
- Network URL: http://0.0.0.0:8501

## Deployment

This app is configured for Streamlit Cloud deployment with:
- Python 3.9.7 (specified in runtime.txt)
- Compatible package versions (specified in requirements.txt)

## Project Structure

- `app.py` - Main Streamlit application
- `stories.json` - Story data with content, images, and metadata
- `assets/images/` - Story cover images and illustrations
- `requirements.txt` - Python dependencies
- `runtime.txt` - Python version specification

## Usage

1. **Browse Stories**: View available stories on the main page
2. **Sign Up/Login**: Create an account or login to access premium content
3. **Read Stories**: Click "Read" to open stories with enhanced features
4. **Audio Narration**: Listen to stories with built-in audio player
5. **Translations**: Switch between different languages
6. **Take Quizzes**: Test your understanding with interactive quizzes

## Technologies Used

- **Streamlit** - Web application framework
- **SQLite** - User authentication database
- **Pillow** - Image processing
- **gTTS** - Text-to-speech for audio narration
- **Google Translate** - Multi-language support

## License

This project is open source and available under the MIT License.
