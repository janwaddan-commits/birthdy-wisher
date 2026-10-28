import os

import streamlit as st
from groq import Groq

st.set_page_config(page_title="Birthday Wishes Replier", page_icon="🎂", layout="centered")

MODEL = "llama-3.3-70b-versatile"


def get_api_key():
    """Read the Groq key from Streamlit secrets or an environment variable."""
    try:
        return st.secrets["GROQ_API_KEY"]
    except Exception:
        return os.getenv("GROQ_API_KEY")


def generate_replies(wishes, tone, language, count, name):
    client = Groq(api_key=get_api_key())
    system_prompt = (
        "You help people reply to birthday wishes they received. "
        "Write warm, genuine, natural-sounding thank-you replies. "
        "Never invent facts about the sender that are not in the wishes."
    )
    user_prompt = (
        f"Here are the birthday wishes I received:\n\n{wishes}\n\n"
        f"Write {count} different thank-you reply options.\n"
        f"Tone: {tone}\nLanguage: {language}\n"
        + (f"My name is {name}; sign off with it if suitable.\n" if name else "")
        + "Number each option and keep each one short."
    )
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.8,
        max_tokens=1024,
    )
    return response.choices[0].message.content


st.title("🎂 Birthday Wishes Replier")
st.caption("Paste the birthday wishes you received and get ready-to-send thank-you replies.")

if not get_api_key():
    st.error("GROQ_API_KEY is missing. Add it to .streamlit/secrets.toml or as an environment variable.")
    st.stop()

wishes = st.text_area("Paste birthday wishes here", height=200,
                      placeholder="Happy birthday! Wishing you a great year ahead...")

col1, col2 = st.columns(2)
with col1:
    tone = st.selectbox("Tone", ["Warm & heartfelt", "Funny", "Formal", "Short & casual", "Emotional"])
    name = st.text_input("Your name (optional)")
with col2:
    language = st.selectbox("Language", ["English", "Urdu", "Roman Urdu", "Pashto", "Hindi", "Arabic", "Spanish", "French"])
    count = st.slider("Number of reply options", 1, 5, 3)

if st.button("Generate replies", type="primary"):
    if not wishes.strip():
        st.warning("Please paste some birthday wishes first.")
    else:
        with st.spinner("Writing your replies..."):
            try:
                result = generate_replies(wishes, tone, language, count, name)
                st.subheader("Your replies")
                st.markdown(result)
            except Exception as e:
                st.error(f"Something went wrong: {e}")
