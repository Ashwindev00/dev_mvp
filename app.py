from flask import Flask, render_template, request, jsonify
import os
import sys
import importlib.util
import traceback

app = Flask(__name__)

# Mock generate function to use when the real one can't be imported
def mock_generate(query):
    responses = {
        "bitcoin": "Bitcoin is a decentralized digital currency, without a central bank or single administrator, that can be sent from user to user on the peer-to-peer bitcoin network without the need for intermediaries. Transactions are verified by network nodes through cryptography and recorded in a public distributed ledger called a blockchain.",
        "ethereum": "Ethereum is a decentralized, open-source blockchain with smart contract functionality. Ether is the native cryptocurrency of the platform. After Bitcoin, it is the second-largest cryptocurrency by market capitalization. The Ethereum Virtual Machine (EVM) enables execution of smart contracts.",
        "solana": "Solana is a highly functional open source project that implements a new, high-performance, permissionless blockchain. The Solana protocol is designed to facilitate decentralized app (DApp) creation. It aims to improve scalability by introducing a proof-of-history (PoH) consensus.",
        "blockchain": "Blockchain is a system of recording information in a way that makes it difficult or impossible to change, hack, or cheat the system. A blockchain is essentially a digital ledger of transactions that is duplicated and distributed across the entire network of computer systems on the blockchain.",
        "crypto": "Cryptocurrency is a digital or virtual currency that is secured by cryptography, which makes it nearly impossible to counterfeit or double-spend. Many cryptocurrencies are decentralized networks based on blockchain technology.",
        "smart contract": "A smart contract is a self-executing contract with the terms of the agreement between buyer and seller being directly written into lines of code. The code and the agreements contained therein exist across a distributed, decentralized blockchain network."
    }
    
    # Default response for queries not in our knowledge base
    default_response = "I don't have specific information about this in my knowledge base, but I'd be happy to answer other questions about blockchain technologies."
    
    # Check if any of our keywords are in the query
    for key, response in responses.items():
        if key.lower() in query.lower():
            return response
    
    return default_response

# Dynamically import the generate function from rag.py
def import_generate_function():
    try:
        # Check if rag.py exists
        rag_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rag.py")
        if not os.path.exists(rag_path):
            print(f"Error: rag.py not found at {rag_path}")
            return None
            
        spec = importlib.util.spec_from_file_location("rag", rag_path)
        rag_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(rag_module)
        
        if not hasattr(rag_module, "generate"):
            print("Error: generate function not found in rag.py")
            return None
            
        return rag_module.generate
    except Exception as e:
        print(f"Error importing generate function: {str(e)}")
        traceback.print_exc()
        return None

# Try to import the generate function, fall back to mock if it fails
try:
    generate = import_generate_function()
    if generate is None:
        generate = mock_generate
        print(f"RAG system initialization failed. Using mock implementation.")
    else:
        print(f"RAG system initialized successfully.")
except Exception as e:
    print(f"Error initializing RAG system: {str(e)}")
    generate = mock_generate
    print(f"Using mock implementation.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():    
    try:
        # Get query from request
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
            
        user_query = data.get('query', '').strip()
        if not user_query:
            return jsonify({'error': 'No query provided'}), 400
        
        # Generate response
        response = generate(user_query)
        
        # Check if the response is an error message
        if response and response.startswith("Error:"):
            return jsonify({'error': response[7:]}), 500
            
        return jsonify({'response': response})
    except Exception as e:
        print(f"Error processing query: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': 'An unexpected error occurred processing your request'}), 500

if __name__ == '__main__':
    # Check if templates directory exists
    templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
    if not os.path.exists(templates_dir):
        print(f"Warning: Templates directory not found at {templates_dir}. Creating it...")
        os.makedirs(templates_dir)
        
        # Check if index.html exists in the templates directory
        index_path = os.path.join(templates_dir, "index.html")
        if not os.path.exists(index_path):
            print(f"Warning: index.html not found. The application may not work correctly.")
    
    app.run(debug=True, port=5000) 