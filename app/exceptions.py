class OpenAIClientError(Exception):
    pass


class OpenAIClientHTTPError(OpenAIClientError):
    def __init__(self, status_code, response_text):
        self.status_code = status_code
        self.response_text = response_text
        super().__init__(f"HTTP error occurred: {status_code} {response_text}")


class OpenAIClientRequestError(OpenAIClientError):
    def __init__(self, message):
        self.message = message
        super().__init__(f"Request error occurred: {message}")


class WordsmithClientError(Exception):
    pass


class WordsmithClientHTTPError(WordsmithClientError):
    def __init__(self, status_code, response_text):
        self.status_code = status_code
        self.response_text = response_text
        super().__init__(f"HTTP error occurred: {status_code} {response_text}")


class WordsmithClientRequestError(WordsmithClientError):
    def __init__(self, message):
        self.message = message
        super().__init__(f"Request error occurred: {message}")


class WordsmithClientParseError(WordsmithClientError):
    def __init__(self, message):
        self.message = message
        super().__init__(f"Parse error: {message}")
