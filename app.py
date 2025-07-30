import streamlit as st

from ai_poet.generator import generate_poem, generate_article

st.set_page_config(page_title="AI Poet & Article Generator", page_icon=":pencil:", layout="centered")

st.title("🪶 AI Poet & Article Generator")

mode = st.radio("Choose mode:", ["Poem", "Article"])
topic = st.text_input("Enter a topic", placeholder="e.g. Artificial Intelligence or Deep Learning")

if st.button(f"Generate {mode}"):
    if not topic.strip():
        st.warning("Please enter a topic!")
    else:
        with st.spinner("Generating..."):
            try:
                if mode == "Poem":
                    output = generate_poem(topic)
                else:
                    output = generate_article(topic)
                st.markdown(output)
            except Exception as e:
                st.error(f"Error: {e}")