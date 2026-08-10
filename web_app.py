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
# CSS
# =========================================================

st.html(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at top right,
                rgba(99, 102, 241, 0.10),
                transparent 30%
            ),
            linear-gradient(
                135deg,
                #080c14 0%,
                #0d1422 55%,
                #090e18 100%
            );
    }

    .block-container {
        max-width: 1180px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    section[data-testid="stSidebar"] {
        background: #0c111b;
        border-right: 1px solid rgba(255, 255, 255, 0.07);
    }

    .hero {
        padding: 1.6rem 0 1.2rem 0;
    }

    .hero-title {
        font-size: 3rem;
        line-height: 1.1;
        font-weight: 800;

        background: linear-gradient(
            90deg,
            #60a5fa,
            #8b5cf6,
            #22d3ee
        );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;

        margin-bottom: 0.7rem;
    }

    .hero-subtitle {
        color: #a5b4c7;
        font-size: 1.08rem;
        max-width: 760px;
        line-height: 1.6;
    }

    .sidebar-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 1rem;
    }

    .sidebar-metric {
        padding: 1rem;
        border-radius: 14px;

        background: rgba(255, 255, 255, 0.035);
        border: 1px solid rgba(255, 255, 255, 0.07);

        margin-bottom: 1rem;
    }

    .sidebar-metric-label {
        color: #94a3b8;
        font-size: 0.72rem;
        letter-spacing: 0.08em;
        font-weight: 600;
    }

    .sidebar-metric-value {
        color: #f8fafc;
        font-size: 2rem;
        font-weight: 700;
        margin-top: 0.2rem;
    }

    .document-card {
        padding: 0.75rem 0.9rem;
        margin-bottom: 0.55rem;

        border-radius: 10px;

        background: rgba(255, 255, 255, 0.035);
        border: 1px solid rgba(255, 255, 255, 0.07);

        color: #dbe4f0;
        font-size: 0.84rem;

        overflow-wrap: anywhere;
    }

    .welcome-card {
        padding: 1.4rem 1.5rem;

        border-radius: 16px;

        background: rgba(255, 255, 255, 0.025);
        border: 1px solid rgba(255, 255, 255, 0.07);

        margin-top: 0.5rem;
        margin-bottom: 1rem;
    }

    .welcome-title {
        color: #f8fafc;
        font-size: 1.35rem;
        font-weight: 700;
        margin-bottom: 0.6rem;
    }

    .welcome-text {
        color: #9ca3af;
        line-height: 1.6;
    }

    .source-card {
        padding: 0.75rem 0.9rem;

        border-radius: 9px;

        background: rgba(96, 165, 250, 0.07);
        border-left: 3px solid #60a5fa;

        margin-bottom: 0.55rem;

        color: #dbeafe;
    }

    .source-meta {
        color: #94a3b8;
        font-size: 0.8rem;
        margin-top: 0.2rem;
    }

    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.025);
        border: 1px solid rgba(255, 255, 255, 0.065);
        border-radius: 14px;

        padding: 1rem 1.2rem;
    }

    [data-testid="stChatMessage"] {
        border-radius: 14px;
        padding: 0.55rem;
        margin-bottom: 0.7rem;
    }

    div.stButton > button {
        border-radius: 9px;
        min-height: 2.6rem;
        transition: 0.2s ease;
    }

    div.stButton > button:hover {
        transform: translateY(-1px);
    }

    .footer {
        color: #64748b;
        font-size: 0.78rem;
        text-align: center;

        padding-top: 3.5rem;
        padding-bottom: 1rem;
    }

    </style>
    """
)


# =========================================================
# FUNÇÕES
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

    destination = DOCUMENTS_DIR / uploaded_file.name

    with open(destination, "wb") as file:
        file.write(
            uploaded_file.getbuffer()
        )

    return destination


def index_documents() -> dict:
    documents = load_all_pdfs()

    chunks = split_documents(
        documents
    )

    processed = add_documents_to_vector_store(
        chunks
    )

    return {
        "pages": len(documents),
        "chunks": len(chunks),
        "processed": processed,
    }


def clear_chat():
    st.session_state.messages = []


def show_sources(sources: list):
    if not sources:
        return

    with st.expander("📄 Fontes utilizadas"):
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

            st.html(
                f"""
                <div class="source-card">
                    <strong>📄 {filename}</strong>
                    <div class="source-meta">
                        Página {page}
                        &nbsp;•&nbsp;
                        Relevância {score:.4f}
                    </div>
                </div>
                """
            )


def detect_quota_error(
    error: Exception,
) -> bool:
    error_text = str(error).lower()

    terms = [
        "resource_exhausted",
        "quota exceeded",
        "429",
    ]

    return any(
        term in error_text
        for term in terms
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

    st.html(
        """
        <div class="sidebar-title">
            📚 Base de conhecimento
        </div>
        """
    )

    pdf_files = get_pdf_files()

    st.html(
        f"""
        <div class="sidebar-metric">

            <div class="sidebar-metric-label">
                DOCUMENTOS INDEXADOS
            </div>

            <div class="sidebar-metric-value">
                {len(pdf_files)}
            </div>

        </div>
        """
    )

    if pdf_files:

        st.subheader(
            "Documentos"
        )

        for pdf_file in pdf_files:

            st.html(
                f"""
                <div class="document-card">
                    📄 {pdf_file.name}
                </div>
                """
            )

    else:

        st.info(
            "Nenhum PDF foi adicionado."
        )

    st.divider()

    # =====================================================
    # UPLOAD
    # =====================================================

    st.subheader(
        "➕ Adicionar documento"
    )

    uploaded_file = st.file_uploader(
        "Selecione um PDF",
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
                    "Documento indexado com sucesso!"
                )

                st.caption(
                    f"{result['pages']} páginas "
                    f"• {result['chunks']} chunks"
                )

                st.rerun()

            except Exception as error:

                st.error(
                    "Não foi possível processar "
                    "o documento."
                )

                st.caption(
                    str(error)
                )

    st.divider()

    # =====================================================
    # CONTROLES
    # =====================================================

    st.subheader(
        "⚙️ Controles"
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
# HERO
# =========================================================

st.html(
    """
    <div class="hero">

        <div class="hero-title">
            RAG Assistant
        </div>

        <div class="hero-subtitle">
            Converse com seus documentos usando Inteligência
            Artificial e busca semântica.
            Faça upload de PDFs, encontre informações relevantes
            e receba respostas baseadas no conteúdo da sua base.
        </div>

    </div>
    """
)


# =========================================================
# INDICADORES
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
        "🧠 Modelo",
        "Gemini",
    )


with col3:
    st.metric(
        "🔎 Recuperação",
        "Semântica",
    )


st.divider()


# =========================================================
# ESTADO INICIAL
# =========================================================

if not pdf_files:

    st.info(
        "👈 Adicione um documento PDF "
        "na barra lateral para começar."
    )


elif not st.session_state.messages:

    st.html(
        """
        <div class="welcome-card">

            <div class="welcome-title">
                👋 Como posso ajudar?
            </div>

            <div class="welcome-text">
                Faça perguntas sobre os documentos disponíveis
                na sua base de conhecimento.
            </div>

        </div>
        """
    )

    st.markdown(
        """
        **Experimente perguntar:**

        - Qual é o valor do plano Premium?
        - Como funciona a matrícula?
        - Quantos dias posso trabalhar remotamente?
        - Quais são os benefícios disponíveis?
        """
    )


# =========================================================
# HISTÓRICO
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
# CHAT
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

st.html(
    """
    <div class="footer">

        RAG Assistant
        &nbsp;•&nbsp;
        Python
        &nbsp;•&nbsp;
        LangChain
        &nbsp;•&nbsp;
        Gemini
        &nbsp;•&nbsp;
        ChromaDB
        &nbsp;•&nbsp;
        Streamlit

    </div>
    """
)
