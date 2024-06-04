from phi.knowledge.pdf import PDFUrlKnowledgeBase
from phi.assistant import Assistant
from phi.llm.groq import Groq
from phi.embedder.ollama import OllamaEmbedder
from phi.vectordb.pgvector import PgVector2
from phi.storage.assistant.postgres import PgAssistantStorage
from rich.prompt import Prompt
from webscraper import scrape

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"
embeddings_model = "nomic-embed-text"
embeddings_table = "groq_rag_documents_ollama"
embedder = OllamaEmbedder(model=embeddings_model, dimensions=768)

vector_db = PgVector2(
    db_url=db_url,
    collection=embeddings_table,
    embedder=embedder,
)

# url = [result["link"] for result in scrape.fetch_from_site()[:20]]
knowledge_base = PDFUrlKnowledgeBase(
    urls=[],
    vector_db=vector_db,
)
rag_assistant = Assistant(
    name="groq_rag_assistant",
    llm=Groq(
        model="llama3-8b-8192",
    ),
    storage=PgAssistantStorage(table_name="groq_rag_assistant", db_url=db_url),
    knowledge_base=knowledge_base,
    description="You are an AI called 'GroqRAG' and your task is to answer questions using the provided information",
    instructions=[
        "You are an AI assistant that processes university examination time tables to provide information about examination schedules.",
        "When given a time table PDF, extract relevant details such as the degree program, semester, exam types (written, practical, viva voce), subject lists, and dates.",
        "Use this extracted information to accurately answer queries about the start and end dates of written examinations, as well as specific details like exam names, schedules, and dates for individual exams or semesters.",
        "Provide clear and concise responses without using phrases like 'based on my knowledge' or 'depending on the information'.",
    ],
    # This setting adds references from the knowledge_base to the user prompt
    add_references_to_prompt=True,
    # This setting tells the LLM to format messages in markdown
    markdown=True,
    # This setting adds chat history to the messages
    add_chat_history_to_messages=True,
    # This setting adds 4 previous messages from chat history to the messages
    num_history_messages=4,
    add_datetime_to_instructions=True,
    debug_mode=True,
)
rag_assistant.knowledge_base.load(recreate=True)


def update_data():
    urls = [result["link"] for result in scrape.fetch_from_site()[:20]]
    knowledge_base = PDFUrlKnowledgeBase(
        urls=urls,
        vector_db=vector_db,
    )
    knowledge_base.load(upsert=True)
    # rag_assistant.knowledge_base.load(upsert=True)


# while True:
#     message = Prompt.ask("[bold] :sunglasses: User [/bold]")
#     if message in ("exit", "bye"):
#         break
#     elif message == "update":
#         urls = [result["link"] for result in scrape.fetch_from_site()[:20]]
#         knowledge_base = PDFUrlKnowledgeBase(
#             urls=urls,
#             vector_db=vector_db,
#         )
#         rag_assistant.knowledge_base.load(upsert=True)
#         message = "Any new time tables published after May 31 2025"
#     rag_assistant.print_response(message, markdown=True)
