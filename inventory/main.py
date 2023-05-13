from fastapi import FastAPI
from redis_om import HashModel
from .utils import io_helpers
import redis


app = FastAPI()

redis_conn = redis.Redis(io_helpers.get_secret("inventory/secrets.json", "redis"))


class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis_conn


@app.get("/products")
def all():
    return Product.all_pks()
