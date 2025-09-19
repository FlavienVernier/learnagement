import os

from qdrant_client import QdrantClient
from sympy.multipledispatch.dispatcher import source

from langchain_qdrant import Qdrant
#from langchain.text_splitter import RecursiveCharacterTextSplitte
from langchain.text_splitter import CharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader
import uuid

import dotenv
dotenv.load_dotenv()

#https://medium.com/@himansrivastava/retrieval-augmented-generation-rag-using-qdrant-with-a-pdf-file-45a9c757bf68
# def pdf_path_to_document(pdf_path):
#     loader = PyPDFLoader(pdf_path)
#     documents = loader.load()
#     langchain_documents = []
#     for doc in documents:
#         langchain_documents.append(
#             Document(
#                 page_content=doc.page_content,
#                 metadata={
#                     "source": doc.metadata["source"],
#                     "page": doc.metadata["page"],
#                     "project": "project_1",
#                 },
#             )
#         )
#     return langchain_documents
#
# def split_pdf(pdf_path, chunk_size=800, chunk_overlap=400):
#     langchain_documents = pdf_path_to_document(pdf_path)
#     text_splitter = RecursiveCharacterTextSplitter(
#         chunk_size=chunk_size,
#         chunk_overlap=chunk_overlap,
#         length_function=len,
#         add_start_index=True,
#     )
#     texts = text_splitter.split_documents(langchain_documents)
#     return texts
#
def add_unique_id(chunks):
     for chunk in chunks:
         chunk.metadata["chunk_id"] = (
             f"{chunk.metadata['source']}_{chunk.metadata['start_index']}"
         )
     return chunks

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
    # embedings =
    # Qdrant.from_documents(  # Create a Qdrant vector store
    #     documents=documents,  # Pass the document chunks
    #     embedding=embeddings,  # Use OpenAI embeddings
    #     collection_name="lakers_collection"  # Name of the collection in Qdrant
    # )
    docs_dict = {k: [doc.dict()[k] for doc in documents] for k in documents[0].dict()}
    client = QdrantClient("http://learnagement_qdrant_llm:6333")  # Adjust the URL to your Qdrant instance
    client.add(
        collection_name="documents",
        documents=docs_dict["page_content"],
        metadata=docs_dict["metadata"],
        ids=[i for i in range(0, len(documents))]
    )


def load_documents():

    # def load_dir(dir_path, i):
    #     client = QdrantClient("http://learnagement_qdrant_llm:6333")
    #     for racine, sub_dir, documents in os.walk(dir_path):
    #         print("load_dir", racine, sub_dir, documents, flush=True)
    #         for document in documents:
    #             documentPath = os.path.join(racine, document)
    #             with open(documentPath, 'r') as file:
    #                 documentContent = file.read()
    #                 print("documentContent", documentContent, flush=True)
    #
    #                 client.add(
    #                     collection_name="documents",
    #                     documents=documentContent,
    #                     metadata=[{"source": documentPath}],
    #                     ids=[i]
    #                 )
    #                 i+=1
    #         for dir in sub_dir:
    #             i=load_dir(dir, i)
    #     return i
    # i=0
    documentsPath = os.environ["DOCUMENTS_PATH"]
    print("documentsPath", documentsPath, flush=True)
    #load_dir(documentsPath, i)
    documents=[]
    for path, subdirs, files in os.walk(documentsPath):
        for name in files:
            doc = load_txt_document(os.path.join(path, name))
            print("doc: ", doc, flush=True)
            documents = documents + doc
    print("documents: ", documents, flush=True)
    documents = add_unique_id(documents)
    add_txt_documents(documents)

def initQdrant():
    # Initialize Qdrant client
    client = QdrantClient("http://learnagement_qdrant_llm:6333")  # Adjust the URL to your Qdrant instance

    # Define wine descriptions
    wines_with_descriptions = [
        "Chateau Margaux a prestigious Bordeaux wine with rich aromas of blackcurrant, tobacco, and licorice.",
        "Penfolds Grange an iconic Australian Shiraz known for its full-bodied structure and deep, complex flavors.",
        "Opus On a Napa Valley classic blending Cabernet Sauvignon and Merlot for a balanced, elegant taste.",
        "Sassicaia a renowned Italian wine from Tuscany, offering flavors of dark berries, spice, and a touch of oak.",
        "Domaine de la Romanée-Conti La Tâche an exceptional Burgundy wine with notes of red fruit, earth, and subtle floral hints.",
        "Chateau Latour a powerful and structured Bordeaux wine with flavors of cassis, cedar, and earthy undertones.",
        "Mouton Rothschild a celebrated Bordeaux wine known for its rich, velvety texture and complex layers of flavor.",
        "Harlan Estate a luxurious Napa Valley wine with deep, concentrated flavors of blackberry, chocolate, and espresso.",
        "Chateau Haut-Brion an elegant Bordeaux wine with notes of plum, tobacco, and a hint of minerality.",
        "Joseph Phelps Insignia a robust Napa Valley blend with flavors of dark fruit, cocoa, and a touch of vanilla.",
        "Louis Roederer Cristal Brut a prestigious Champagne with crisp acidity, fine bubbles, and notes of citrus and brioche.",
        "Chateau Cheval Blanc a refined Bordeaux wine with flavors of red fruit, spice, and a long, elegant finish.",
        "Chateau d'Yquem a legendary sweet wine from Sauternes, known for its2 honeyed flavors and luscious texture.",
        "Chateau Lafite Rothschild a premier Bordeaux wine with complex aromas of blackcurrant, graphite, and a hint of violets.",
        "Caymus Special Selection Cabernet Sauvignon a rich and opulent Napa Valley Cabernet with flavors of ripe berries and cocoa.",
        "Screaming Eagle Cabernet Sauvignon a rare and highly sought-after Napa Valley wine with intense flavors of dark fruit and spice.",
        "Tenuta San Guido Sassicaia a distinguished Italian wine from Bolgheri, offering notes of blackcurrant, herbs, and a touch of oak.",
        "Ornellaia Bolgheri Superiore a luxurious Italian wine with rich flavors of dark berries, tobacco, and chocolate.",
        "E. Guigal Cote Rotie La Landonne a powerful and complex Rhone wine with flavors of blackberry, smoked meat, and pepper.",
        "Vega Sicilia Unico a legendary Spanish wine with notes of dark fruit, spice, and a long, sophisticated finish.",
        "Chateau Palmer a refined Bordeaux wine with elegant aromas of plum, tobacco, and a hint of cedar.",
        "Petrus an exquisite Bordeaux wine from Pomerol, known for its rich, velvety texture and complex flavors.",
        "Chateau Mouton Rothschild a celebrated Bordeaux wine known for its rich, velvety texture and complex layers of flavor.",
        "Chateau Margaux a prestigious Bordeaux wine with rich aromas of blackcurrant, tobacco, and licorice.",
        "Chateau Haut-Brion an elegant Bordeaux wine with notes of plum, tobacco, and a hint of minerality.",
        "Chateau Lafite Rothschild a premier Bordeaux wine with complex aromas of blackcurrant, graphite, and a hint of violets.",
        "Chateau Latour a powerful and structured Bordeaux wine with flavors of cassis, cedar, and earthy undertones.",
        "Chateau Cheval Blanc a refined Bordeaux wine with flavors of red fruit, spice, and a long, elegant finish.",
        "Chateau d'Yquem a legendary sweet wine from Sauternes, known for its honeyed flavors and luscious texture.",
        "Caymus Special Selection Cabernet Sauvignon a rich and opulent Napa Valley Cabernet with flavors of ripe berries and cocoa."
    ]


    # Use the new add method
    client.add(
        collection_name="wines6",
        documents=wines_with_descriptions,
        metadata=
        #[{"source": "raw_data"}],
        [{"source": "raw_data_"+str(i)} for i in range(0, len(wines_with_descriptions))],
        #[
        #    {"source": "Langchain-docs"},
        #    {"source": "Linkedin-docs"},
        #],
        ids=[i for i in range(0, len(wines_with_descriptions))]
    )

    load_documents()

    # search_result = client.query(
    #     collection_name="wines6",
    #     query_text="Chateau Cheval Blanc"
    # )
    # print("search_result: ", search_result, flush=True)

def get_doc(request):
    # Initialize Qdrant client
    client = QdrantClient("http://learnagement_qdrant_llm:6333")
    # Test the db
    search_result = client.query(
        collection_name="documents",
        query_text=request
    )
    return search_result