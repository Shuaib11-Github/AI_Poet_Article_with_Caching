from ai_poet import generator
from pytest import MonkeyPatch

def test_generate_poem_uses_stub(monkeypatch: MonkeyPatch):
    dummy = "Unit-test poem."
    # patch the copy that generate_poem really calls
    monkeypatch.setattr("ai_poet.generator.chat_completion",
                        lambda *_a, **_kw: dummy)

    assert generator.generate_poem("pytest topic", use_cache=False) == dummy