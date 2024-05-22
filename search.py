#!/usr/bin/env python
# coding: utf-8

# In[ ]:
import pip

#pip install langchain[all]


# In[ ]:


#pip install sentence-transformers




# In[ ]:

from sentence_transformers import SentenceTransformer
from langchain.embeddings import SentenceTransformerEmbeddings
embedding_function3 = SentenceTransformerEmbeddings(model_name='intfloat/multilingual-e5-large')


# In[ ]:


#pip install qdrant-client


from langchain_community.vectorstores import Qdrant


from qdrant_client import QdrantClient

qdrant_client = QdrantClient(
    url="https://88c128b7-6432-4bcf-aa91-27bb78990c30.us-east4-0.gcp.cloud.qdrant.io:6333",
    api_key="B4jBqmIUhizGuWaHWX8JkIy2wt_Wsg2UMt3nU-DFp1kUMKJD-tw4hw",
)


doc_store = Qdrant(
    client=qdrant_client, collection_name="vkr3",
    embeddings=embedding_function3,
)

#query = "Цифровая иллюстрация: Создание цифровых иллюстраций с помощью Procreate или Adobe Photoshop"
def search(query):
    ans1 = doc_store.similarity_search(query, 2)
    #print(ans1)
    answer = "Вам могут подойти следующие курсы:"

    for doc in ans1:
        title = str(doc.metadata['title'].split('–')[0])
        if title not in answer:
            answer += '\n'
            answer += '\n'
            answer += title
            answer += '\n'
            answer += str(doc.metadata['source'])
    return answer

#print(search(query))