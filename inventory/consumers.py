from main import redis_conn, Product
import time

key = "orders_completed"
group = "inventory-group"

try:
    redis_conn.xgroup_create(key, group)
except:
    print("Group already exists!")

while True:
    try:
        results = redis_conn.xreadgroup(group, key, {key: ">"}, None)
        print(results)

        if results != []:
            for result in results:
                obj = result[1][0][1]
                try:
                    product = Product.get(obj["product_id"])
                    print(product)
                    product.quantity = product.quantity - int(obj["quantity"])
                    product.save()
                except:
                    redis_conn.xadd("refund_order", obj, "*")

    except Exception as e:
        print(str(e))
    time.sleep(1)
