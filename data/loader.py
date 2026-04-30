import os, re
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import *

def split_by_dieu(text, source):
    parts = re.split(r"(Điều\s+\d+\.)", text)
    docs = []

    for i in range(1, len(parts), 2):
        title = parts[i]
        content = parts[i+1]

        match = re.search(r"Điều\s+(\d+)", title)
        dieu = int(match.group(1)) if match else None

        docs.append(Document(
            page_content=(title + content).strip(),
            metadata={"source": source, "dieu": dieu}
        ))
    return docs


def load_docs():
    docs = []

    for file in os.listdir(DATA_PATH):
        if file.endswith(".txt"):
            loader = TextLoader(os.path.join(DATA_PATH, file), encoding="utf-8")
            raw = loader.load()

            source = os.path.splitext(file)[0]

            for d in raw:
                docs.extend(split_by_dieu(d.page_content, source))

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    return splitter.split_documents(docs)
