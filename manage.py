import logging.config

import uvicorn
import uvloop

import settings

uvloop.install()
logging.config.dictConfig(settings.LOGGING_CONFIG)


if __name__ == "__main__":
    uvicorn.run("app.application:create_app", host="0.0.0.0", port=settings.API_PORT)
