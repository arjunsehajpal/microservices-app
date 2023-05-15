from main import Product, redis_conn

key = "order_completed"
group = "inventory-group"


try:
    redis_conn.xgroup_create(key, groupname=group)
except KeyError as K:
    print(f"group {group} already exists!")
    print(f"Details:\n{K}")


while True:
    try:
        results = redis_conn.xreadgroup(group, key, {key: ">"}, None)
    except Exception as E:
        print(f"encountered following exception while reading groups:\n{E}")
