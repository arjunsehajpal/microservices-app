import redis
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import HashModel
from starlette.requests import Request

from .utils import io_helpers

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000"], allow_methods=["*"], allow_headers=["*"])


redis_conn_params = io_helpers.get_secret("inventory/secrets.json", "redis")
redis_conn = redis.Redis(**redis_conn_params)


class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str  # allowed values: [pending, completed, refunded]

    class Meta:
        database = redis


@app.post("/orders")
async def create(order_request: Request):
    """creates an order

    Args:
        order_request (Request): should contain following keys:
            - id
            - quantity
    """
    body = await order_request.json()
    req_to_product = requests.get("http://localhost:8000/products/{}".format(body["id"]))
    return req_to_product.json()
