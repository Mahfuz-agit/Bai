from .base import ModelProvider


class MockProvider(ModelProvider):
    """Deterministic placeholder so the architecture can be tested before wiring a model API."""

    def generate(self, *, system: str, user: str, temperature: float = 0.2, **kwargs) -> str:
        return f"[MOCK]\nSYSTEM: {system[:120]}\nUSER: {user[:500]}"
