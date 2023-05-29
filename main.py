import streamlit as st
from streamlit_chat import message

from langchain import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings

from backend.core import create_docs, run_llm
from backend.text_processor import create_sources_string


st.header("LangChain🦜🔗 Document Helper Bot")
if (
    "chat_answers_history" not in st.session_state
    and "user_prompt_history" not in st.session_state
    and "chat_history" not in st.session_state
):
    st.session_state["chat_answers_history"] = []
    st.session_state["user_prompt_history"] = []
    st.session_state["chat_history"] = []

if "last_uploaded_files" not in st.session_state:
    st.session_state.last_uploaded_files = []

# Show the sidebar on first render
uploaded_files = st.sidebar.file_uploader(
    "**Upload Your Files**",
    type=[
        "pdf",
        "docx",
        "txt",
        "doc",
        "pptx",
        "ppt",
        "xlsx",
        "xls",
        "csv",
        "html",
        "htm",
        "xml",
        "json",
    ],
    accept_multiple_files=True,
)

if uploaded_files != st.session_state.last_uploaded_files:
    st.session_state["chat_answers_history"] = []
    st.session_state["user_prompt_history"] = []
    st.session_state["chat_history"] = []
    st.session_state.last_uploaded_files = uploaded_files

if uploaded_files:
    all_pages = create_docs(uploaded_files)
    api = st.sidebar.text_input(
        "**Enter OpenAI API Key**",
        type="password",
        placeholder="sk-",
        help="https://platform.openai.com/account/api-keys",
    )

    if api:
        embeddings = OpenAIEmbeddings(openai_api_key=api)
        index = None
        try:
            with st.spinner("It's indexing..."):
                index = FAISS.from_documents(documents=all_pages, embedding=embeddings)
            st.sidebar.success("Embeddings done.", icon="✅")
        except Exception as e:
            st.sidebar.error(f"Indexing failed. Please check if API key is valid.")
            st.error("Indexing failed. Please check if API key is valid.")

        if index:
            prompt = st.text_area(
                "Prompt", placeholder="Enter your message here..."
            ) or st.button("Submit")

            if prompt:
                with st.spinner("Generating response..."):
                    generated_response = run_llm(
                        key=api,
                        query=prompt,
                        index=index,
                        chat_history=st.session_state["chat_history"],
                    )

                    sources = set(
                        [
                            doc.metadata["source"]
                            for doc in generated_response["source_documents"]
                        ]
                    )
                    formatted_response = f"{generated_response['answer']} \n\n {create_sources_string(sources)}"

                    st.session_state.chat_history.append(
                        (prompt, generated_response["answer"])
                    )
                    st.session_state.user_prompt_history.append(prompt)
                    st.session_state.chat_answers_history.append(formatted_response)

            if st.session_state["chat_answers_history"]:
                for generated_response, user_query in reversed(
                    list(
                        zip(
                            st.session_state["chat_answers_history"],
                            st.session_state["user_prompt_history"],
                        )
                    )
                ):
                    message(generated_response)
                    message(
                        user_query,
                        is_user=True,
                        key=f"{user_query}-{generated_response}",
                    )
    else:
        st.warning("Input your API key to continue.")
else:
    st.warning("Upload your file to continue.")
