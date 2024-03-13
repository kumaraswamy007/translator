import streamlit as st
import speech_recognition as sr
import pyttsx3
from googletrans import Translator
import gtts

# Define supported languages and their codes (at least 15)
languages = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Russian": "ru",
    "Chinese": "zh-cn",
    "Japanese": "ja",
    "Korean": "ko",
    "Hindi": "hi",
    "Arabic": "ar",
    "Turkish": "tr",
    "Dutch": "nl",
    "Greek": "el",
    "Telugu":"te"
}

def speak(text):
    """Speaks the given text using pyttsx3."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def translate_and_speak(text, source_lang, target_lang):
    """Translates text and speaks the translated version."""
    translator = Translator()
    translation = translator.translate(text, src=source_lang, dest=target_lang)
    translated_text = translation.text
    st.subheader(f"**Translated Text:** {translated_text}")
    speak(translated_text)

def main():
    """Builds the Streamlit app for text and voice translation."""

    st.title("Translator App")

    # Text translation section
    st.header("Text Translation")
    source_text = st.text_area("Enter the text to translate")
    source_lang = st.selectbox("Source Language", list(languages.keys()),key="lang3")
    target_lang = st.selectbox("Target Language", list(languages.keys()),key="lang2")

    if st.button("Translate"):
        source_lang_code = languages[source_lang]
        target_lang_code = languages[target_lang]
        translate_and_speak(source_text, source_lang_code, target_lang_code)

    # Voice translation section
    st.header("Voice Translation")
    spoken_source_lang = st.selectbox("Source Language", list(languages.keys()),key="lang1")
    if st.button("Speak to Translate"):
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()

        with microphone as source:
            st.info("Say something...")
            audio = recognizer.listen(source)

        try:
            source_text = recognizer.recognize_google(audio)
            source_lang = spoken_source_lang  # Assuming default source language is English
            target_lang = st.selectbox("Translate to", list(languages.keys()))
            source_lang_code = languages[source_lang]
            target_lang_code = languages[target_lang]
            translate_and_speak(source_text, source_lang_code, target_lang_code)

        except sr.UnknownValueError:
            st.error("Could not understand audio")
        except sr.RequestError as e:
            st.error(f"Request error: {e}")

if __name__ == "__main__":
    main()
