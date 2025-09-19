import os

from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient
from langchain.text_splitter import CharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader

import dotenv
dotenv.load_dotenv()

#https://medium.com/@himansrivastava/retrieval-augmented-generation-rag-using-qdrant-with-a-pdf-file-45a9c757bf68

def add_unique_id(chunks):
     for chunk in chunks:
         chunk.metadata["chunk_id"] = (
             f"{chunk.metadata['source']}_{chunk.metadata['start_index']}"
         )
     return chunks

def load_pdf_document(pdf_path):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    langchain_documents = []
    for doc in documents:
        langchain_documents.append(
            Document(
                page_content=doc.page_content,
                metadata={
                    "source": doc.metadata["source"],
                    "page": doc.metadata["page"],
                    "project": "project_1",
                },
            )
        )
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    docs = text_splitter.split_documents(langchain_documents)
    return docs


#https://medium.com/@anixlynch/build-rag-with-qdrant-w-dynamic-prompt-via-langchain-hub-c5ab43758b93
def load_txt_document(doc_path):
    loader = TextLoader(doc_path)  # Load the text file
    document = loader.load()  # Load the document content

    langchain_documents = []
    for doc in document:
         langchain_documents.append(
             Document(
                 page_content=doc.page_content,
                 metadata={
                     "source": doc_path,
#                    "page": doc.metadata["page"],
                     "project": "project_1",
                 },
             )
         )

    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100, add_start_index=True)  # Split text into chunks
    docs = text_splitter.split_documents(langchain_documents)  # Process and create document chunks

    return docs


def add_txt_documents(documents):
    docs_dict = {k: [doc.dict()[k] for doc in documents] for k in documents[0].dict()}
    client = QdrantClient("http://learnagement_qdrant_llm:6333")  # Adjust the URL to your Qdrant instance
    client.add(
        collection_name="lnm_dev",
        documents=docs_dict["page_content"],
        metadata=docs_dict["metadata"],
        ids=[i for i in range(0, len(documents))]
    )


def load_documents(documentsPath):

    documents=[]
    for path, subdirs, files in os.walk(documentsPath):
        for name in files:
            doc = load_txt_document(os.path.join(path, name))
            documents = documents + doc
    documents = add_unique_id(documents)
    add_txt_documents(documents)

def initQdrant():

    documentsPath = os.environ["RAG_DOCUMENTS_PATH"]
    load_documents(documentsPath)


def get_doc(request):
    # Initialize Qdrant client
    client = QdrantClient("http://learnagement_qdrant_llm:6333")
    # Test the db
    search_result = client.query(
        collection_name="lnm_dev",
        query_text=request
    )
    return search_result