import os
import shutil
from langchain_text_splitters import  RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document

embeddings= HuggingFaceEmbeddings(model_name= "sentence-transformers/all-MiniLM-L6-v2")
def ingest(dir, files: list[str]) -> list:
    docs = []
    for i in files:
        path = os.path.join(dir, "books", i)
        try:
            # Try with default encoding first
            loader = TextLoader(path)
            doc = loader.load()
            docs.extend(doc)
        except Exception as e:
            try:
                # Try with UTF-8 encoding
                loader = TextLoader(path, encoding='utf-8')
                doc = loader.load()
                docs.extend(doc)
            except Exception as e:
                try:
                    # Try with latin-1 encoding (should handle most characters)
                    loader = TextLoader(path, encoding='latin-1')
                    doc = loader.load()
                    docs.extend(doc)
                except Exception as e:
                    print(f"Error loading {path}: {e}")
                    continue
    print(docs)
    return docs


def splitting(doc):
    print("---Creating chunks---")
    text_splitter= RecursiveCharacterTextSplitter(
        chunk_size= 1000,
        chunk_overlap= 200,
        separators= ["\n\n","\n"," ",""],
    )
    chunks= text_splitter.split_documents(doc)
    print("sample\n")
    return chunks

def vectordb(persis_dir,chunks):
    if(os.path.exists(persis_dir)):
        print("Removing existing db...")
        shutil.rmtree(persis_dir)
    
    print("Creating new db...")
    db = Chroma.from_documents(documents=chunks,
                              embedding=embeddings,
                              persist_directory=persis_dir)
    print("---created db---")
    return db
       

def main():
    curr_dir= os.path.dirname(os.path.abspath(__file__))
    import time
    timestamp = str(int(time.time()))
    perist_dir= os.path.join(curr_dir,"db", f"chroma_{timestamp}")
    files= ["bitcoin.txt", "sol.txt", "eth.txt"]
    print (files)
    loaded_files= ingest(curr_dir, files)
    chunks= splitting(loaded_files)
    db= vectordb(perist_dir, chunks)
    
    # Write the latest db path to a file
    with open(os.path.join(curr_dir, "db", "latest_db.txt"), "w") as f:
        f.write(perist_dir)

main()