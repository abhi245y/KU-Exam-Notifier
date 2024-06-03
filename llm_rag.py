from phi.knowledge.pdf import PDFUrlKnowledgeBase
from phi.assistant import Assistant
from phi.llm.groq import Groq
from phi.embedder.ollama import OllamaEmbedder
from phi.vectordb.pgvector import PgVector2
from phi.storage.assistant.postgres import PgAssistantStorage
from rich.prompt import Prompt

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"
embeddings_model = "nomic-embed-text"
embeddings_table = "groq_rag_documents_ollama"

embedder = OllamaEmbedder(model=embeddings_model, dimensions=768)

knowledge = PDFUrlKnowledgeBase(
    urls=["https://exams.keralauniversity.ac.in/Images/Time%20Table/2024/05/83029.pdf"],
    vector_db=PgVector2(
        db_url=db_url,
        collection=embeddings_table,
        embedder=embedder,
    ),
)

rag_assistant = Assistant(
    name="groq_rag_assistant",
    llm=Groq(model="llama3-8b-8192"),
    storage=PgAssistantStorage(table_name="groq_rag_assistant", db_url=db_url),
    knowledge_base=knowledge,
    description="You are an AI called 'GroqRAG' and your task is to answer questions using the provided information",
    instructions=[
        "When a user asks a question, you will be provided with information about the question.",
        "Carefully read this information and provide a clear and concise answer to the user.",
        "Do not use phrases like 'based on my knowledge' or 'depending on the information'.",
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

rag_assistant.knowledge_base.load()


while True:
    message = Prompt.ask(f"[bold] :sunglasses: User [/bold]")
    if message in ("exit", "bye"):
        break
    rag_assistant.print_response(message, markdown=True)

# rag_assistant.print_response(
#     "Tell me about TENTH SEMESTER INTEGRATED (5 YEAR)BA.LLB timetable and about the collges where the exam is going to be conducted"
# )
