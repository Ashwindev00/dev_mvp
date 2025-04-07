# Blockchain Knowledge Agent UI - Startup Instructions

Follow these simple steps to launch the web-based UI for your Blockchain Knowledge Agent:

## Quick Start (Recommended)

1. **Open a command prompt or PowerShell window**

2. **Navigate to the project directory**
   ```
   cd C:\Users\hrith\Downloads\mvp_ashwin\mvp_ashwin
   ```

3. **Run the application**
   ```
   C:\Users\hrith\AppData\Local\Programs\Python\Python311\python.exe run.py
   ```

4. **Open the UI in your browser**
   Once the application is running, open your web browser and go to:
   ```
   http://localhost:5000
   ```

## Manual Setup (Alternative)

If you encounter any issues with the quick start, you can try these manual steps:

1. **Install Required Packages**
   ```
   C:\Users\hrith\AppData\Local\Programs\Python\Python311\python.exe -m pip install Flask langchain-text-splitters langchain-community langchain-core langchain-chroma chromadb langchain-huggingface sentence-transformers langchain-groq python-dotenv
   ```

2. **Run the Database Setup**
   ```
   C:\Users\hrith\AppData\Local\Programs\Python\Python311\python.exe my_langchain.py
   ```

3. **Start the Flask Application**
   ```
   C:\Users\hrith\AppData\Local\Programs\Python\Python311\python.exe app.py
   ```

4. **Access the UI**
   Open your browser and go to:
   ```
   http://localhost:5000
   ```

## Troubleshooting

- **Missing Modules**: If you see "module not found" errors, make sure all packages are installed using pip
- **Database Errors**: If you see database errors, try running `my_langchain.py` manually
- **Port Already in Use**: If port 5000 is busy, modify the port number in `app.py` to an available port

If you experience persistent issues, please stop any running Python processes and try again.

Enjoy using your Blockchain Knowledge Agent! 