@echo off
echo Setting up Python environment...

set PYTHON_PATH=C:\Users\hrith\AppData\Local\Programs\Python\Python311
set PYTHON_SCRIPTS=%PYTHON_PATH%\Scripts

:: Add Python paths to system PATH
setx PATH "%PATH%;%PYTHON_PATH%;%PYTHON_SCRIPTS%"

:: Create virtual environment
%PYTHON_PATH%\python.exe -m venv venv

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Install required packages
python -m pip install --upgrade pip
pip install langchain-text-splitters langchain-community langchain-core langchain-chroma chromadb langchain-huggingface sentence-transformers langchain-groq python-dotenv

echo Environment setup complete!
echo Please run: venv\Scripts\activate.bat
pause 