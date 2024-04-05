import redis
import os

# script to reset redis cache for testing.
# put it inside backend image because redis is in the poetry env

host = os.environ.get("REDIS_HOST")
r = redis.Redis(host=host, port=6379, decode_responses=True)

# r.delete("Christopher Nolan")

# delete all keys
for key in r.scan_iter():
    r.delete(key)
