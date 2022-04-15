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

class Request():
    base_url = str

@app.post("/collections")
async def create_collection(request):
    await IndexesClient().create_indexes()
    client = TransactionsClient()
    collection = json.loads(bytearray(request["body"]).decode("utf-8"))
    Request.base_url = "localhost:8080"

    await client.create_collection(collection=collection, request=Request)
    return json.dumps(collection)

@app.get("/collections/:collection_id")
async def get_collection(request):
    client = CoreClient()
    Request.base_url = "localhost:8080"
    collection = await client.get_collection(collection_id=request["params"]["collection_id"], request=Request)
    return json.dumps(collection)

@app.get("/collections")
async def get_all_collections(requests):
    client = CoreClient()
    Request.base_url = "localhost:8080"
    collections = await client.all_collections(request=Request)
    return json.dumps({
        "collections": collections
    })

app.start(port=8080, url="0.0.0.0")
