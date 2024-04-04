import streamlit as st
from google.cloud import speech_v1p1beta1 as speech

@st.cache
def get_history():
  if "history" not in st.session_state:
    st.session_state["history"] = []
  return st.session_state["history"]

def add_to_history(user_input, assistant_response):
  history = get_history()
  history.append({"user": user_input, "assistant": assistant_response})
  st.session_state["history"] = history

def display_chat():
  history = get_history()
  for message in history:
    if message["user"]:
      st.chat_message("User", message["user"])
    else:
      st.chat_message("Assistant", message["assistant"])

def get_voice_input():
  client = speech.SpeechClient()
  config = {
      "encoding": speech.RecognitionConfig.AudioEncoding.LINEAR16,
      "sample_rate_hertz": 16000,
      "language_code": "en-US",
  }

  with st.spinner("Listening..."):
    audio = st.audio_recorder(format="wav", key="voice_input")
    audio_data = audio.getvalue()

  if audio_data:
    audio = speech.RecognitionAudio(content=audio_data)
    response = client.recognize(config=config, audio=audio)

    for result in response.results:
      return result.alternatives[0].transcript.lower()

  else:
    st.write("Sorry, I could not understand your audio.")
    return ""

def main():
  text_input = st.text_input("Type your message here...")
  voice_input = st.button("Speak your message")

  if voice_input:
    user_input = get_voice_input()
    if user_input:
      add_to_history(user_input, "Thanks for your message!")  # Replace with actual response logic
  elif text_input:
    add_to_history(text_input, "Thanks for your message!")  # Replace with actual response logic
  display_chat()

if __name__ == "__main__":
  main()