from robyn import Robyn, jsonify
import json
import stac_pydantic.api
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
    method = None
    url = None

@app.post("/collections")
async def create_collection(request):
    await IndexesClient().create_indexes()
    client = TransactionsClient()
    collection = json.loads(bytearray(request["body"]).decode("utf-8"))
    Request.base_url = "localhost:8080"

    await client.create_collection(collection=collection, request=Request)
    return jsonify(collection)

@app.get("/collections/:collection_id")
async def get_collection(request):
    client = CoreClient()
    Request.base_url = "localhost:8080"
    collection = await client.get_collection(collection_id=request["params"]["collection_id"], request=Request)
    return jsonify(collection)

@app.get("/collections")
async def get_all_collections(requests):
    client = CoreClient()
    Request.base_url = "localhost:8080"
    collections = await client.all_collections(request=Request)
    return jsonify({
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
    return jsonify(item)

@app.get("/collections/:collection_id/items/:item_id")
async def get_item(request):
    client = CoreClient()
    Request.base_url = "localhost:8080"
    item = await client.get_item(
        item_id=request["params"]["item_id"], 
        collection_id=request["params"]["collection_id"], 
        request=Request
    )
    return jsonify(item)

@app.delete("/collections/:collection_id/items/:item_id")
async def delete_item(request):   
    client = TransactionsClient()
    await client.delete_item(
        collection_id=request["params"]["collection_id"],
        item_id=request["params"]["item_id"]
    )

@app.get("/collections/:collection_id/items")
async def get_item_collection(request):
    client = CoreClient()
    Request.base_url = "localhost:8080"
    Request.method = None
    Request.url = "localhost:8080"
    items = await client.item_collection(
        collection_id=request["params"]["collection_id"], 
        request=Request
    )
    return jsonify(items)

@app.post("/search")
async def post_search(request):
    client = CoreClient()
    search_body = json.loads(bytearray(request["body"]).decode("utf-8"))
    search = stac_pydantic.api.Search(
        collections=search_body["collections"] if "collections" in search_body else [],
        ids=search_body["ids"] if "ids" in search_body else [],
        intersects=search_body["intersects"] if "intersects" in search_body else None
    )
    Request.base_url = "localhost:8080"
    items = await client.post_search(
        search_request=search,
        request=Request
    )
    return jsonify(items)

app.start(port=8080, url="0.0.0.0")
