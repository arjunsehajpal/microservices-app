from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from redis_om import HashModel
from .utils import io_helpers

import redis


app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000"], allow_methods=["*"], allow_headers=["*"])


redis_conn_params = io_helpers.get_secret("inventory/secrets.json", "redis")
redis_conn = redis.Redis(**redis_conn_params)


class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis_conn


def format(pk: str):
    product = Product.get(pk)
    return {"id": product.pk, "name": product.name, "price": product.price, "quantity": product.quantity}


@app.get("/products")
async def all():
    return [format(pk) for pk in Product.all_pks()]


@app.get("/products/{pk}")
def get_product(pk: str):
    return Product.get(pk)


@app.delete("/products/{pk}")
def delete_product(pk: str):
    return Product.delete(pk)


@app.post("/products")
def create(product: Product):
    return product.save()
