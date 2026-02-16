import time
from collections import defaultdict

requests_store = defaultdict(list)

def check_rate_limit(api_key, limit):
    now = time.time()
    window = 60

    requests_store[api_key] = [
        t for t in requests_store[api_key]
        if now - t < window
    ]

    if len(requests_store[api_key]) >= limit:
        return False

    requests_store[api_key].append(now)
    return True
