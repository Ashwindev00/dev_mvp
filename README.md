# Blockchain Knowledge Agent UI

This is an elegant web interface for the Blockchain Knowledge Agent that provides information about Bitcoin, Ethereum, and Solana based on their whitepapers and technical documentation.

## Setup Instructions

1. **Install Required Packages**

   ```bash
   pip install Flask langchain-text-splitters langchain-community langchain-core langchain-chroma chromadb langchain-huggingface sentence-transformers langchain-groq python-dotenv
   ```

2. **Set Environment Variables**

   Make sure you have your GROQ API key in `.env` file:
   ```
   GROQ_API_KEY = your_groq_api_key
   ```

3. **Run the Application**

   From the project directory, run:
   ```bash
   python run.py
   ```

   This will:
   - Check if the database exists
   - Run the ingestion process if needed
   - Start the Flask web server

4. **Access the UI**

   Open your browser and go to:
   ```
   http://localhost:5000
   ```

## Features

- **Elegant Chat Interface**: Clean, modern UI for a great user experience
- **Suggested Prompts**: Example questions to help you get started
- **Markdown Support**: The agent's responses support markdown formatting
- **Session Persistence**: Your conversation history is maintained during the session

## Available Knowledge

The agent has knowledge about:

1. **Bitcoin**: Based on the original Bitcoin whitepaper by Satoshi Nakamoto
2. **Ethereum**: Information about smart contracts and proof of stake mechanism
3. **Solana**: Technical details about Proof of History and Solana's architecture

## Example Questions

- What is the double-spending problem in Bitcoin?
- How does Proof of History work in Solana?
- What are smart contracts in Ethereum?
- Compare consensus mechanisms in Bitcoin, Ethereum, and Solana
- How does Bitcoin's Proof of Work differ from Ethereum's Proof of Stake? 