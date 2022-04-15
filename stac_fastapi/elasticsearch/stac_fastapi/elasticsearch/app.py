from robyn import Robyn
import json
from stac_fastapi.elasticsearch.core import (
    CoreClient,
    TransactionsClient,
)
from stac_fastapi.elasticsearch.indexes import IndexesClient
app = Robyn(__file__)

@app.get("/")
async def h(requests):
    return "Hello, world!"

@app.post("/collections")
async def create_collection(request):

    await IndexesClient().create_indexes()
    client = TransactionsClient()
    collection = json.loads(bytearray(request["body"]).decode("utf-8"))
    Request.base_url = "localhost:8080"

    await client.create_collection(collection=collection, request=Request)
    return json.dumps(collection)

class Request():
    base_url = str

@app.get("/collections")
async def get_all_collections(requests):
    client = CoreClient()
    Request.base_url = "localhost:8080"
    
    # request["base_url"] = "localhost:8080"
    collections = await client.all_collections(request=Request)
    return json.dumps({
        "collections": collections
    })
    return json.dumps(requests)

app.start(port=8080, url="0.0.0.0")
