import os
import subprocess
import sys
import time
import importlib
import importlib.util
import platform
import traceback

# Set the working directory to the script's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def get_python_path():
    """Get the correct Python executable path"""
    return sys.executable

def print_diagnostics():
    """Print diagnostic information"""
    print("\n===== SYSTEM DIAGNOSTICS =====")
    print(f"Python version: {sys.version}")
    print(f"Platform: {platform.platform()}")
    print(f"Script directory: {os.path.dirname(os.path.abspath(__file__))}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python executable: {sys.executable}")
    
    # Check key files
    files_to_check = ["app.py", "rag.py", "my_langchain.py", ".env"]
    print("\nChecking critical files:")
    for file in files_to_check:
        status = "✓ Found" if os.path.exists(file) else "✗ Missing"
        print(f"  {file}: {status}")
        
    # Check directories
    dirs_to_check = ["templates", "db", "books"]
    print("\nChecking directories:")
    for dir_name in dirs_to_check:
        if os.path.exists(dir_name):
            print(f"  {dir_name}/: ✓ Found ({len(os.listdir(dir_name))} items)")
        else:
            print(f"  {dir_name}/: ✗ Missing")
    
    # Check .env file content
    if os.path.exists(".env"):
        try:
            with open(".env", "r") as f:
                env_content = f.read().strip()
                if "GROQ_API_KEY" in env_content:
                    print("\n.env file contains GROQ_API_KEY")
                else:
                    print("\n⚠️ .env file doesn't contain GROQ_API_KEY")
        except:
            print("\n⚠️ Error reading .env file")
    
    print("=============================\n")

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = ["flask", "langchain_chroma", "langchain_groq", "langchain_core", 
                         "langchain_text_splitters", "langchain_community", "langchain_huggingface",
                         "python-dotenv", "chromadb"]
    missing_packages = []
    
    print("Checking required packages...")
    for package in required_packages:
        try:
            # Handle packages with dashes that use underscores in import
            import_name = package.replace("-", "_")
            importlib.import_module(import_name)
            print(f"  ✓ {package} installed")
        except ImportError:
            missing_packages.append(package)
            print(f"  ✗ {package} missing")
    
    if missing_packages:
        print(f"\nMissing required packages: {', '.join(missing_packages)}")
        install = input("Would you like to install them now? (y/n): ")
        if install.lower() == 'y':
            try:
                print(f"Installing packages with: {get_python_path()} -m pip install {' '.join(missing_packages)}")
                result = subprocess.run([get_python_path(), "-m", "pip", "install"] + missing_packages, 
                                      check=True, capture_output=True, text=True)
                print("Packages installed successfully.")
                return True
            except subprocess.CalledProcessError as e:
                print(f"Error installing packages: {e}")
                print("Error output:")
                print(e.stderr)
                return False
            except Exception as e:
                print(f"Unexpected error installing packages: {e}")
                traceback.print_exc()
                return False
        else:
            print("Cannot continue without required packages.")
            return False
    
    print("All required packages are installed.")
    return True

def check_database():
    """Check if the database has been initialized properly"""
    try:
        db_path = os.path.join(os.getcwd(), "db")
        if not os.path.exists(db_path):
            print("Database directory doesn't exist. Creating it...")
            os.makedirs(db_path)
        
        latest_db_file = os.path.join(db_path, "latest_db.txt")
        db_exists = False
        
        if os.path.exists(latest_db_file):
            try:
                with open(latest_db_file, 'r') as f:
                    chroma_path = f.read().strip()
                if os.path.exists(chroma_path):
                    print(f"Database found at: {chroma_path}")
                    db_exists = True
                else:
                    print(f"Database path exists in file but directory not found: {chroma_path}")
            except Exception as e:
                print(f"Error reading database path: {e}")
        
        if not db_exists:
            print("Database not initialized. Running ingestion script...")
            python_path = get_python_path()
            try:
                # Check if the ingestion script exists
                if not os.path.exists("my_langchain.py"):
                    print("Error: my_langchain.py not found!")
                    return False
                
                # Check if books directory exists
                books_dir = os.path.join(os.getcwd(), "books")
                if not os.path.exists(books_dir):
                    print("Books directory not found. Creating it...")
                    os.makedirs(books_dir)
                    
                # Check if there are any txt files in the books directory
                txt_files = [f for f in os.listdir(books_dir) if f.endswith('.txt')]
                if not txt_files:
                    print("No text files found in books directory. Creating sample files...")
                    create_sample_files(books_dir)
                
                print(f"Running: {python_path} my_langchain.py")
                result = subprocess.run([python_path, "my_langchain.py"], 
                                      check=True, capture_output=True, text=True)
                print("Ingestion completed successfully.")
                time.sleep(2)  # Wait for file creation
                
                # Check again if database was created
                if os.path.exists(latest_db_file):
                    with open(latest_db_file, 'r') as f:
                        db_path = f.read().strip()
                        if os.path.exists(db_path):
                            print(f"Database created at: {db_path}")
                            return True
                        else:
                            print(f"Database path written to file but directory not found: {db_path}")
                            return False
                else:
                    print("Database initialization failed: latest_db.txt not created")
                    return False
            except subprocess.CalledProcessError as e:
                print(f"Error running ingestion script: {e}")
                print("Error output:")
                print(e.stderr)
                return False
            except Exception as e:
                print(f"Unexpected error during database initialization: {e}")
                traceback.print_exc()
                return False
        
        return db_exists
    except Exception as e:
        print(f"Error checking database: {e}")
        traceback.print_exc()
        return False

def create_sample_files(books_dir):
    """Create sample text files if none exist"""
    try:
        # Create sample Bitcoin file
        with open(os.path.join(books_dir, "bitcoin.txt"), "w") as f:
            f.write("""Bitcoin: A Peer-to-Peer Electronic Cash System
Satoshi Nakamoto
satoshin@gmx.com
www.bitcoin.org

Abstract. A purely peer-to-peer version of electronic cash would allow online
payments to be sent directly from one party to another without going through a
financial institution. Digital signatures provide part of the solution, but the main
benefits are lost if a trusted third party is still required to prevent double-spending.
We propose a solution to the double-spending problem using a peer-to-peer network.
The network timestamps transactions by hashing them into an ongoing chain of
hash-based proof-of-work, forming a record that cannot be changed without redoing
the proof-of-work. The longest chain not only serves as proof of the sequence of
events witnessed, but proof that it came from the largest pool of CPU power.""")
        
        # Create sample Ethereum file
        with open(os.path.join(books_dir, "eth.txt"), "w") as f:
            f.write("""Ethereum: A Next-Generation Smart Contract and Decentralized Application Platform
Vitalik Buterin
https://ethereum.org/

Ethereum is a decentralized platform that runs smart contracts: applications that run exactly as programmed without any possibility of downtime, censorship, fraud or third-party interference.

Ethereum is a blockchain-based platform with smart contract functionality. It provides a decentralized virtual machine, the Ethereum Virtual Machine (EVM), which can execute scripts using an international network of public nodes.

Ethereum uses a proof-of-stake consensus mechanism where validators stake ETH to secure the network.""")
        
        # Create sample Solana file
        with open(os.path.join(books_dir, "sol.txt"), "w") as f:
            f.write("""Solana: A new architecture for a high performance blockchain
Anatoly Yakovenko
https://solana.com/

Solana is a high-performance blockchain supporting builders around the world creating crypto apps that scale today.

Solana is a decentralized blockchain built to enable scalable, user-friendly apps for the world. It uses a unique method called Proof of History to order transactions, combined with a Proof of Stake consensus mechanism for high throughput.

Solana features ultra-low transaction costs and sub-second settlement times.""")
        
        print("Sample blockchain text files created successfully.")
    except Exception as e:
        print(f"Error creating sample files: {e}")
        traceback.print_exc()

def run_app():
    """Run the Flask application"""
    try:
        # Check if we have a RAG module that works
        if not os.path.exists("rag.py"):
            print("Error: rag.py not found!")
            return False
        
        if not os.path.exists("app.py"):
            print("Error: app.py not found!")
            return False
            
        # Check template directory exists
        templates_dir = os.path.join(os.getcwd(), "templates")
        if not os.path.exists(templates_dir):
            print("Templates directory not found. Creating it...")
            os.makedirs(templates_dir)
        
        # Check if index.html exists
        index_path = os.path.join(templates_dir, "index.html")
        if not os.path.exists(index_path):
            print("Error: index.html not found in templates directory!")
            print("Please make sure the UI template exists before continuing.")
            return False
        
        # Try to import the app
        try:
            from app import app
            print("Starting the Blockchain Knowledge Agent UI...")
            print("Access the UI in your browser at: http://localhost:5000")
            app.run(debug=True, port=5000)
            return True
        except ImportError as e:
            print(f"Error importing Flask app: {e}")
            print("Trying to run app.py directly...")
            
            # If import fails, try to run the app directly
            python_path = get_python_path()
            try:
                subprocess.run([python_path, "app.py"], check=True)
                return True
            except subprocess.CalledProcessError as e:
                print(f"Error running app.py: {e}")
                return False
    except Exception as e:
        print(f"Error starting Flask app: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\n=== Blockchain Knowledge Agent ===")
    print("Initializing system...")
    
    # Print diagnostics to help troubleshoot issues
    print_diagnostics()
    
    if not check_dependencies():
        print("Failed to verify dependencies.")
        sys.exit(1)
        
    if not check_database():
        print("Failed to initialize database.")
        sys.exit(1)
        
    if not run_app():
        print("Failed to start the web application.")
        sys.exit(1) 