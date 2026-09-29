"""Domain-specific exceptions, mapped to HTTP responses in app/main.py."""


class ResearchAssistantError(Exception):
    """Base exception for all app-specific errors."""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class SessionNotFoundError(ResearchAssistantError):
    def __init__(self, session_id: str):
        super().__init__(f"Research session '{session_id}' not found.", status_code=404)


class NoLiteratureFoundError(ResearchAssistantError):
    def __init__(self, query: str):
        super().__init__(
            f"No papers were found for query '{query}' across configured search providers.",
            status_code=422,
        )


class LLMProviderError(ResearchAssistantError):
    def __init__(self, provider: str, detail: str):
        super().__init__(f"LLM provider '{provider}' failed: {detail}", status_code=502)


class SearchProviderError(ResearchAssistantError):
    def __init__(self, provider: str, detail: str):
        super().__init__(f"Search provider '{provider}' failed: {detail}", status_code=502)


class InvalidPipelineStateError(ResearchAssistantError):
    def __init__(self, detail: str):
        super().__init__(detail, status_code=409)
