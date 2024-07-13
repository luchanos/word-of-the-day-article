from envparse import env

API_PORT = env.int("API_PORT", default=8080)

OPENAI_API_KEY = env.str("OPENAI_API_KEY")

REDIS_TEST_HOST = env.str("REDIS_TEST_URL", default="0.0.0.0")
REDIS_TEST_PORT = env.int("REDIS_TEST_PORT", default=6379)
REDIS_HOST = env.str("REDIS_HOST")
REDIS_PORT = env.int("REDIS_PORT")
