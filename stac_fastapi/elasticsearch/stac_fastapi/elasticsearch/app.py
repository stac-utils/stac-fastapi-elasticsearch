from robyn import Robyn
import json
from stac_fastapi.elasticsearch.core import (
    CoreClient,
    TransactionsClient,
)
from stac_fastapi.elasticsearch.indexes import IndexesClient
app = Robyn(__file__)

@app.get("/")
async def root(requests):
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

@app.delete("/collections/:collection_id")
async def delete_collection(request):   
    client = TransactionsClient()
    await client.delete_collection(collection_id=request["params"]["collection_id"])

@app.post("/collections/:collection_id/items")
async def create_item(request):
    client = TransactionsClient()
    item = json.loads(bytearray(request["body"]).decode("utf-8"))
    Request.base_url = "localhost:8080"

    item = await client.create_item(item=item, request=Request)
    return json.dumps(item)

@app.get("/collections/:collection_id/items/:item_id")
async def get_item(request):
    client = CoreClient()
    Request.base_url = "localhost:8080"
    item = await client.get_item(
        item_id=request["params"]["item_id"], 
        collection_id=request["params"]["collection_id"], 
        request=Request
    )
    return json.dumps(item)

@app.delete("/collections/:collection_id/items/:item_id")
async def delete_item(request):   
    client = TransactionsClient()
    await client.delete_item(
        collection_id=request["params"]["collection_id"],
        item_id=request["params"]["item_id"]
    )

app.start(port=8080, url="0.0.0.0")
