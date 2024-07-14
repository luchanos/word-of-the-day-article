from envparse import env

API_PORT = env.int("API_PORT", default=8080)

ARTICLE_CACHE_TTL = env.int("ARTICLE_CACHE_TTL", default=60 * 60 * 24)
ARTICLE_CACHE_MAXSIZE = env.int("ARTICLE_CACHE_MAXSIZE", default=128)
OPENAI_API_KEY = env.str("OPENAI_API_KEY", default="")
OPENAI_TEST_API_KEY = env.str("OPENAI_TEST_API_KEY", default="openai_test_api_key")
