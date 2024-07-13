from envparse import env

API_PORT = env.int("API_PORT", default=8080)

OPENAI_API_KEY = env.str("OPENAI_API_KEY")

REDIS_TEST_URL = env.str("REDIS_TEST_URL", default="")
REDIS_URL = env.str("REDIS_URL", default="")
