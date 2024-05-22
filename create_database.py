import requests
#pip install selenium
import selenium
import soupsieve
from bs4 import BeautifulSoup

page1 = requests.get('https://www.hse.ru/edu/dpo/?onlyActual=0')
soup2=BeautifulSoup(page1.text,'html.parser')
urls2 = []
alltags=soup2.select("a[href*='hse.ru/edu/dpo']")
for item in alltags:
    if len(item['href']) < 40:
        urls2.append((item['href']))

for i in range(2, 40):
    link = 'https://www.hse.ru/edu/dpo/?page=' + str(i) + '&onlyActual=0'
    page = requests.get(link)
    soup2=BeautifulSoup(page.text,'html.parser')
    alltags=soup2.select("a[href*='hse.ru/edu/dpo']")
    for item in alltags:
        if len(item['href']) < 42 and item['href'] not in urls2:
            urls2.append((item['href']))

from langchain_community.document_loaders import WebBaseLoader

loader = WebBaseLoader(urls2)
docs = loader.load()

from langchain.text_splitter import RecursiveCharacterTextSplitter
r_splitter = RecursiveCharacterTextSplitter(separators = ["Программа обучения", "Формат обучения", "График обучения", "Стоимость и условия", "nn", "n", " "])

splits = r_splitter.split_documents(docs)

from langchain.embeddings import SentenceTransformerEmbeddings
embedding_function3 = SentenceTransformerEmbeddings(model_name='intfloat/multilingual-e5-large')

#pip install yake
import yake

extractor = yake.KeywordExtractor (
    lan = "ru",
    n = 3,
    dedupLim = 0.3,
    top = 10
)


def kw_extract(text):
    keywords = extractor.extract_keywords(text)
    top_keywords = [kw[0] for kw in keywords]
    return (' ,'.join(top_keywords))


for chunk in splits:
    chunk.metadata['keywords'] = kw_extract(chunk.page_content)

#pip install qdrant-client

from langchain_community.vectorstores import Qdrant

url = "https://88c128b7-6432-4bcf-aa91-27bb78990c30.us-east4-0.gcp.cloud.qdrant.io"
api_key = "B4jBqmIUhizGuWaHWX8JkIy2wt_Wsg2UMt3nU-DFp1kUMKJD-tw4hw"
qdrant = Qdrant.from_documents(
    splits,
    embedding_function3,
    url=url,
    prefer_grpc=False,
    api_key=api_key,
    collection_name="vkr3",
    force_recreate=True
)


