from envparse import env

API_PORT = env.int("API_PORT", default=8080)

REDIS_TEST_URL = env.str("REDIS_TEST_URL", default="")
REDIS_URL = env.str("REDIS_URL", default="")
