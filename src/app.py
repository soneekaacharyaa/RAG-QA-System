import streamlit as st
from generate_answers import generate_answer, load_system

def main():
    st.set_page_config(page_title="Movie Trivia QA", page_icon="🎬")
    index, processed_data, embedding_model, openai_client = load_system()

    st.title("Movie Trivia Question Answering")
    st.markdown("Ask questions about movies from our database of 40+ popular films.")

    if "question" not in st.session_state:
        st.session_state.question = ""

    question = st.text_input(
        "Ask a question about a movie:",
        placeholder="E.g., 'Who directed The Shawshank Redemption?'",
        value=st.session_state.question,
        key="input_box"
    )
    if question:
        with st.spinner("Searching for answer..."):
            answer, context_type, message = generate_answer(
                question, index, processed_data, embedding_model, openai_client
            )
        st.subheader("Answer")
        if answer:
            st.write(f"{message}")
            st.success(answer)
        else:
            st.warning(f"{message}")
        st.session_state.question = ""

    st.subheader("Try these sample questions:")
    sample_questions = [
        "Who directed The Shawshank Redemption?",
        "When was The Godfather released?",
        "Who are the main actors in The Dark Knight?",
        "What is the plot of Inception?",
        "Who directed Titanic?",
        "What year was Jurassic Park released?"
    ]

    cols = st.columns(3)
    for i, q in enumerate(sample_questions):
        if cols[i % 3].button(q):
            st.session_state.question = q
            st.rerun() 

if __name__ == "__main__":
    main()
