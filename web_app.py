from pathlib import Path

import streamlit as st

from config.settings import DOCUMENTS_DIR
from src.exceptions import RAGException
from src.loader import load_all_pdfs
from src.rag import ask_rag
from src.splitter import split_documents
from src.vector_store import add_documents_to_vector_store


# =========================================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================================

st.set_page_config(
    page_title="RAG Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# ESTILO VISUAL
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        background: linear-gradient(
            135deg,
            #0b0f19 0%,
            #111827 55%,
            #0d1321 100%
        );
    }

    .block-container {
        max-width: 1150px;
        padding-top: 2.5rem;
        padding-bottom: 4rem;
    }

    .rag-header {
        padding: 1.2rem 0 1.6rem 0;
    }

    .rag-title {
        font-size: 2.6rem;
        font-weight: 800;
        margin-bottom: 0.3rem;
        background: linear-gradient(
            90deg,
            #60a5fa,
            #8b5cf6,
            #22d3ee
        );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .rag-subtitle {
        color: #9ca3af;
        font-size: 1.05rem;
    }

    .metric-card {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.7rem;
    }

    .metric-label {
        font-size: 0.8rem;
        color: #9ca3af;
    }

    .metric-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #f3f4f6;
    }

    .document-card {
        background: rgba(255,255,255,0.035);
        border: 1px solid rgba(255,255,255,0.07);
        padding: 0.75rem;
        border-radius: 10px;
        margin-bottom: 0.5rem;
        font-size: 0.86rem;
    }

    .source-card {
        background: rgba(96, 165, 250, 0.08);
        border-left: 3px solid #60a5fa;
        border-radius: 8px;
        padding: 0.65rem 0.9rem;
        margin-bottom: 0.5rem;
    }

    section[data-testid="stSidebar"] {
        background: #0d111a;
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    [data-testid="stChatMessage"] {
        border-radius: 14px;
        padding: 0.4rem;
        margin-bottom: 0.7rem;
    }

    div.stButton > button {
        border-radius: 9px;
        transition: all 0.2s ease;
    }

    div.stButton > button:hover {
        transform: translateY(-1px);
    }

    .footer {
        margin-top: 4rem;
        text-align: center;
        color: #6b7280;
        font-size: 0.78rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# FUNÇÕES AUXILIARES
# =========================================================

def get_pdf_files() -> list[Path]:

    if not DOCUMENTS_DIR.exists():
        return []

    return sorted(
        DOCUMENTS_DIR.glob("*.pdf")
    )


def save_uploaded_file(uploaded_file) -> Path:

    DOCUMENTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    destination = (
        DOCUMENTS_DIR
        / uploaded_file.name
    )

    with open(
        destination,
        "wb",
    ) as file:

        file.write(
            uploaded_file.getbuffer()
        )

    return destination


def index_documents() -> dict:

    documents = load_all_pdfs()

    chunks = split_documents(
        documents
    )

    processed = (
        add_documents_to_vector_store(
            chunks
        )
    )

    return {
        "pages": len(documents),
        "chunks": len(chunks),
        "processed": processed,
    }


def clear_chat():

    st.session_state.messages = []


def show_sources(
    sources: list,
):

    if not sources:
        return

    with st.expander(
        "📄 Fontes utilizadas"
    ):

        for source in sources:

            filename = source.get(
                "filename",
                "Fonte desconhecida",
            )

            page = source.get(
                "page",
                "?",
            )

            score = source.get(
                "score",
                0,
            )

            st.markdown(
                f"""
                <div class="source-card">

                <strong>📄 {filename}</strong><br>

                Página {page}
                &nbsp;•&nbsp;
                Relevância {score:.4f}

                </div>
                """,
                unsafe_allow_html=True,
            )


def detect_quota_error(
    error: Exception,
) -> bool:

    error_text = str(error).lower()

    quota_terms = [
        "resource_exhausted",
        "quota exceeded",
        "429",
    ]

    return any(
        term in error_text
        for term in quota_terms
    )


# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        "## 📚 Base de conhecimento"
    )

    pdf_files = get_pdf_files()

    st.markdown(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                DOCUMENTOS INDEXADOS
            </div>

            <div class="metric-value">
                {len(pdf_files)}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    if pdf_files:

        st.markdown(
            "### Documentos"
        )

        for pdf_file in pdf_files:

            st.markdown(
                f"""
                <div class="document-card">

                📄 {pdf_file.name}

                </div>
                """,
                unsafe_allow_html=True,
            )

    else:

        st.info(
            "Nenhum PDF foi adicionado."
        )

    st.divider()

    st.markdown(
        "### ➕ Adicionar documento"
    )

    uploaded_file = st.file_uploader(
        "Selecione um arquivo PDF",
        type=["pdf"],
        label_visibility="collapsed",
    )

    if uploaded_file is not None:

        if st.button(
            "📥 Adicionar à base",
            use_container_width=True,
        ):

            try:

                with st.spinner(
                    "Processando documento..."
                ):

                    save_uploaded_file(
                        uploaded_file
                    )

                    result = (
                        index_documents()
                    )

                st.success(
                    "Documento indexado!"
                )

                st.caption(
                    f"{result['pages']} páginas • "
                    f"{result['chunks']} chunks"
                )

                st.rerun()

            except Exception as error:

                st.error(
                    "Não foi possível "
                    "processar o documento."
                )

                st.caption(
                    str(error)
                )

    st.divider()

    st.markdown(
        "### ⚙️ Controles"
    )

    if st.button(
        "🗑️ Limpar conversa",
        use_container_width=True,
    ):

        clear_chat()

        st.rerun()

    st.divider()

    st.caption(
        "Gemini • LangChain • ChromaDB"
    )


# =========================================================
# CABEÇALHO
# =========================================================

st.markdown(
    """
    <div class="rag-header">

        <div class="rag-title">
            RAG Assistant
        </div>

        <div class="rag-subtitle">
            Converse com seus documentos utilizando
            busca semântica e Inteligência Artificial.
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# STATUS DA BASE
# =========================================================

pdf_files = get_pdf_files()

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "📄 Documentos",
        len(pdf_files),
    )


with col2:

    st.metric(
        "🧠 IA",
        "Gemini",
    )


with col3:

    st.metric(
        "🔎 Busca",
        "Semântica",
    )


st.divider()


# =========================================================
# ESTADO VAZIO
# =========================================================

if not pdf_files:

    st.info(
        "👈 Adicione um PDF na barra lateral "
        "para começar."
    )


elif not st.session_state.messages:

    st.markdown(
        """
        ### 👋 Como posso ajudar?

        Faça perguntas sobre os documentos
        disponíveis na base.

        **Exemplos:**

        - Qual é o valor do plano Premium?
        - Como funciona a matrícula?
        - Quantos dias posso trabalhar remotamente?
        - Quais são os benefícios disponíveis?
        """
    )


# =========================================================
# HISTÓRICO DO CHAT
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

        show_sources(
            message.get(
                "sources",
                [],
            )
        )


# =========================================================
# INPUT
# =========================================================

question = st.chat_input(
    "Faça uma pergunta sobre seus documentos..."
)


if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message(
        "user"
    ):

        st.markdown(
            question
        )

    with st.chat_message(
        "assistant"
    ):

        with st.spinner(
            "🔎 Consultando a base..."
        ):

            try:

                result = ask_rag(
                    question
                )

                answer = result[
                    "answer"
                ]

                sources = result[
                    "sources"
                ]

                st.markdown(
                    answer
                )

                show_sources(
                    sources
                )

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "sources": sources,
                    }
                )

            except RAGException as error:

                if detect_quota_error(
                    error
                ):

                    message = (
                        "⚠️ O limite gratuito da IA "
                        "foi atingido. "
                        "Tente novamente mais tarde."
                    )

                    st.warning(
                        message
                    )

                else:

                    message = (
                        "Não foi possível processar "
                        "sua pergunta."
                    )

                    st.error(
                        message
                    )

                    st.caption(
                        str(error)
                    )

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": message,
                    }
                )

            except Exception as error:

                if detect_quota_error(
                    error
                ):

                    message = (
                        "⚠️ O limite gratuito da IA "
                        "foi atingido. "
                        "Tente novamente mais tarde."
                    )

                    st.warning(
                        message
                    )

                else:

                    message = (
                        "Ocorreu um erro inesperado."
                    )

                    st.error(
                        message
                    )

                    st.caption(
                        str(error)
                    )

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": message,
                    }
                )


# =========================================================
# RODAPÉ
# =========================================================

st.markdown(
    """
    <div class="footer">

        RAG Assistant
        • Python
        • LangChain
        • Gemini
        • ChromaDB
        • Streamlit

    </div>
    """,
    unsafe_allow_html=True,
)
