from langchain_groq import ChatGroq
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.retrievers import BM25Retriever
from dotenv import load_dotenv
from langchain_chroma import Chroma
from my_langchain import embeddings

import os
import sys
from langchain.prompts import ChatPromptTemplate
# Load environment variables
load_dotenv()

# Check if GROQ API key is set
if not os.getenv("GROQ_API_KEY"):
    print("ERROR: GROQ_API_KEY not found in environment variables. Please check your .env file.")
    sys.exit(1)

# Initialize LLM with proper error handling
try:
    llm = ChatGroq(model="llama3-70b-8192")
    curr_dir = os.path.dirname(os.path.abspath(__file__))
except Exception as e:
    print(f"ERROR initializing ChatGroq: {e}")
    sys.exit(1)

def retreiver(db):
    try:
        retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 4})
        return retriever
    except Exception as e:
        print(f"Error creating retriever: {e}")
        raise

def create_chain(persist_dir):
    try:
        # Check if the persist_dir exists
        if not os.path.exists(persist_dir):
            print(f"Error: Database directory not found at {persist_dir}")
            # Try to find the latest database
            db_dir = os.path.join(curr_dir, "db")
            if os.path.exists(db_dir):
                subfolders = [f for f in os.listdir(db_dir) if os.path.isdir(os.path.join(db_dir, f)) and f.startswith("chroma")]
                if subfolders:
                    # Use the most recent chroma folder (assuming naming convention with timestamps)
                    latest_db = os.path.join(db_dir, sorted(subfolders)[-1])
                    print(f"Using alternative database at {latest_db}")
                    persist_dir = latest_db
                else:
                    raise FileNotFoundError(f"No chroma database folders found in {db_dir}")
            else:
                raise FileNotFoundError(f"Database directory {db_dir} not found")
        
        db = Chroma(embedding_function=embeddings, persist_directory=persist_dir)
        retrieved = retreiver(db)
        
        template = """
        You are an expert blockchain and cryptocurrency analyst with deep knowledge of Bitcoin, Ethereum, and Solana. 
        You excel at both technical analysis and engaging conversation. Your responses should be natural, insightful, and demonstrate deep understanding.

        Context: {context}

        Question: {question}

        Please provide a response that matches the user's communication style and question depth:
        1. For short, direct questions: Provide concise, focused answers
        2. For detailed questions: Offer comprehensive analysis
        3. For technical queries: Include relevant technical details while maintaining clarity
        4. For general questions: Keep responses accessible and engaging

        Key guidelines:
        - Match the length and depth of your response to the user's question
        - For brief questions, provide crisp, valuable insights
        - For in-depth questions, offer detailed analysis with examples
        - Use bullet points or numbered lists only when they add clarity
        - Keep technical explanations simple unless the question demands detail
        - Focus on the most relevant information from the context

        If the information is not present in the context, say "I don't have specific information about this in my knowledge base, but I'd be happy to discuss other aspects of blockchain technology or answer related questions."

        Remember to:
        - Be conversational and engaging
        - Adapt your response length to the question
        - Prioritize clarity and relevance
        - Provide practical examples when helpful
        - Maintain a balance between technical accuracy and accessibility
        
        Answer:"""

        prompt = ChatPromptTemplate.from_template(template)

        chain = (
        {
            "context": retrieved,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser())

        return chain
    except Exception as e:
        print(f"Error creating chain: {e}")
        raise

# Initialize the chain with proper error handling
try:
    # Try to read the latest db path first
    db_path = None
    latest_db_file = os.path.join(curr_dir, "db", "latest_db.txt")
    if os.path.exists(latest_db_file):
        with open(latest_db_file, "r") as f:
            db_path = f.read().strip()
    
    # If latest_db.txt doesn't exist or its path is invalid, use the default
    if not db_path or not os.path.exists(db_path):
        db_path = os.path.join(curr_dir, "db", "chroma")
    
    print(f"Initializing with database: {db_path}")
    chain = create_chain(db_path)
except Exception as e:
    print(f"Error initializing chain: {e}")
    chain = None

def generate(query):
    try:
        if chain is None:
            return "Error: The RAG system is not properly initialized. Please check your database and API key."
        
        # Improved error handling and user feedback
        if not query or len(query.strip()) < 2:
            return "Please provide a valid question about blockchain technologies."
            
        response = chain.invoke(query)
        return response
    except Exception as e:
        error_msg = str(e)
        if "api_key" in error_msg.lower() or "apikey" in error_msg.lower():
            return "Error: There seems to be an issue with the API key. Please check your GROQ_API_KEY in the .env file."
        elif "timeout" in error_msg.lower() or "connection" in error_msg.lower():
            return "Error: Could not connect to the GROQ API. Please check your internet connection."
        else:
            return f"Error generating response: {error_msg}"

def chat(query):
    while query.lower() != "exit":
        response = generate(query)
        print(f"AI: {response}")
        query = input("Human: ")
    print("--AI Stopped--")

def main():
    # Read the latest db path
    try:
        with open(os.path.join(curr_dir, "db", "latest_db.txt"), "r") as f:
            db_path = f.read().strip()
            
        if not os.path.exists(db_path):
            print(f"Warning: Database path {db_path} not found. Running my_langchain.py to create a new database.")
            os.system(f"{sys.executable} {os.path.join(curr_dir, 'my_langchain.py')}")
            
            # Re-read the latest db path
            with open(os.path.join(curr_dir, "db", "latest_db.txt"), "r") as f:
                db_path = f.read().strip()
    except Exception as e:
        print(f"Error: {e}. Running my_langchain.py to create the database.")
        os.system(f"{sys.executable} {os.path.join(curr_dir, 'my_langchain.py')}")
        
        # Re-read the latest db path
        try:
            with open(os.path.join(curr_dir, "db", "latest_db.txt"), "r") as f:
                db_path = f.read().strip()
        except:
            print("Critical error: Failed to create and read database.")
            return

    global chain
    chain = create_chain(db_path)
    print("Blockchain Knowledge Agent ready. Type 'exit' to quit.")
    query = input("Human: ")
    chat(query)

if __name__ == "__main__":
    main()