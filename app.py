import streamlit as st
from googletrans import Translator, LANGUAGES
from gtts import gTTS
import os

# Initialize the translator
translator = Translator()

# Create a mapping from language names to codes
language_names = list(LANGUAGES.values())
language_codes = list(LANGUAGES.keys())
name_to_code = {name.lower(): code for code, name in LANGUAGES.items()}

# Get supported languages for gTTS
from gtts.lang import tts_langs
gtts_supported = tts_langs()

# Streamlit app title with emojis
st.title("Translator 360 🌍")

# Description with an emoji
st.write("Translate text in real-time and hear the pronunciation instantly. Just choose your languages and enter text! 🗣️")

# Add a nice separator line
st.markdown("---")

# Text input with optional language detection
st.header("Enter Text to Translate 📜")
input_text = st.text_area("Type your text here:")

# Language selection with default values
st.header("Choose Languages 🌐")
source_lang_name = st.selectbox(
    "Select source language (leave as 'auto' for detection):",
    ['auto'] + language_names,
    index=0
)
target_lang_name = st.selectbox(
    "Select target language:",
    language_names,
    index=language_names.index('hindi') if 'hindi' in language_names else 0
)

# Function to get language code from name
def get_lang_code(lang_name):
    return name_to_code.get(lang_name.lower(), 'en')  # Default to 'en' if not found

# Translation and pronunciation
st.markdown("---")
st.header("Translation & Pronunciation 🔄")

if st.button("Translate 🔄"):
    if not input_text.strip():
        st.warning("⚠️ Please enter text to translate.")
    else:
        # Determine source language
        if source_lang_name.lower() == 'auto':
            src_lang = 'auto'
        else:
            src_lang = get_lang_code(source_lang_name)
        
        # Get target language code
        dest_lang = get_lang_code(target_lang_name)

        try:
            # Translate the text
            translation = translator.translate(input_text, src=src_lang, dest=dest_lang)
            translated_text = translation.text
            detected_src = LANGUAGES.get(translation.src, 'Unknown').title()

            st.write(f"**Detected Source Language:** `{detected_src}` 🌍")
            st.success(f"**Translated Text:** {translated_text} 🎉")

            # Check if target language is supported by gTTS
            if dest_lang not in gtts_supported:
                st.warning(f"⚠️ Pronunciation for '{target_lang_name}' is not supported.")
            else:
                # Text-to-Speech (TTS) for pronunciation
                try:
                    tts = gTTS(translated_text, lang=dest_lang)
                    audio_file = "translated_audio.mp3"
                    tts.save(audio_file)

                    # Display audio player
                    st.audio(audio_file, format="audio/mp3")

                    # Option to download the audio
                    with open(audio_file, "rb") as f:
                        st.download_button(
                            label="Download Pronunciation 📥",
                            data=f,
                            file_name="translated_audio.mp3",
                            mime="audio/mp3"
                        )

                    # Clean up the audio file after playing
                    os.remove(audio_file)
                except ValueError as ve:
                    st.error(f"TTS Error: {ve}")
        except Exception as e:
            st.error(f"Translation Error: {e}")

# Footer with some style
st.markdown("---")
st.write("💡 **Tip:** You can translate any language you want and hear the pronunciation!")
st.write("Made with ❤️ using Streamlit.")
