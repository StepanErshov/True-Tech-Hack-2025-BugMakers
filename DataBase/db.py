import weaviate
from weaviate.classes.init import Auth
from weaviate.classes.config import Configure
import os, sys, json, numpy as np
from dotenv import load_dotenv
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from initialData.parser import read_xlsx
# from api.main import post_embeddings

# in .env vars weaviate_url and weaviate_api_key
load_dotenv() 

weaviate_url = os.environ["WEAVIATE_URL"]
weaviate_api_key = os.environ["WEAVIATE_API_KEY"]

client = weaviate.connect_to_weaviate_cloud(
    cluster_url=weaviate_url,
    auth_credentials=Auth.api_key(weaviate_api_key),
)

dataa = read_xlsx(path='../initialData/Q&A set.xlsx')
with open('articles.json', 'r', encoding='utf-8') as file:
    data_b2c = json.load(file)

with open('articles_b2c.json', 'r', encoding='utf-8') as file:
    data_b2c_2 = json.load(file)


def init_collection(name_of_coll):
    collection_name = client.collections.create(
        name=f"{name_of_coll}",
        vectorizer_config=Configure.Vectorizer.text2vec_weaviate(), 
        generative_config=Configure.Generative.cohere()             
    )
    return collection_name


def fill_coll_objects(collection_name, dataa):
    collection_name = client.collections.get(f"{collection_name}")

    with collection_name.batch.dynamic() as batch:
        for d in dataa:
            batch.add_object({
                "Answer": d["correct_answer"],
                "Query": d["query"],
            })
            if batch.number_errors > 10:
                print("Batch import stopped due to excessive errors.")
                break

def fill_coll_objects_b2c(collection_name, dataa):
    collection_name = client.collections.get(f"{collection_name}")

    with collection_name.batch.dynamic() as batch:
        for d in dataa:
            batch.add_object({
                "Content": d["content"],
                "Name": d["name"],
                "ID": d["id"],
            })
            if batch.number_errors > 10:
                print("Batch import stopped due to excessive errors.")
                break


def get_all_vectors_and_text(collection_name):
    output = []
    collection_name = client.collections.get(f"{collection_name}")
    for item in collection_name.iterator(include_vector=True):
        output.append((item.properties, item.vector))
    return output
        # vec1 = np.asarray(post_embeddings(item.properties['query'])['data'][0]['embedding'])
        # vec2 = np.asarray(item.vector['default'])
        # print(np.linalg.norm(vec1) - np.linalg.norm(vec2))
        # break

def add_object(collection_name, data_answ, data_query) -> None:
    collection_name = client.collections.get(f"{collection_name}")

    uuid = collection_name.data.insert({
        "Answer": f"{data_answ}",
        "Query": f'{data_query}', 
    })

def add_object_b2c(collection_name, content, name, id) -> None:
    collection_name = client.collections.get(f"{collection_name}")

    uuid = collection_name.data.insert({
        "Content": f'{content}',
        "Name": f'{name}',
        "ID": f'{id}',
    })


#add b2c cases
init_collection(name_of_coll='b2c')
fill_coll_objects_b2c(collection_name='b2c', dataa=data_b2c)
fill_coll_objects_b2c(collection_name='b2c', dataa=data_b2c_2)
client.close()