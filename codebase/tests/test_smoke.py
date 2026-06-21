import bcrypt

from src.config.settings import settings
from src.core import auth
from src.utils.zalo_bot import ZaloBot, MAX_TEXT_LEN
from src.utils.document_loader import DocumentLoader


def test_settings_loaded():
    assert settings.PROJECT.name
    assert settings.GEMINI_MODEL_NAME
    assert settings.EMBEDDING_MODEL_NAME


def test_password_hash_roundtrip():
    pw = "s3cret-pass"
    hashed = auth.hash_password(pw)
    assert hashed != pw
    assert bcrypt.checkpw(pw.encode(), hashed.encode())
    assert not bcrypt.checkpw(b"wrong", hashed.encode())


def test_zalo_bot_secret_disabled_in_dev():
    bot = ZaloBot()
    bot.secret_token = ""
    assert bot.verify_secret("anything") is True


def test_zalo_bot_secret_verification():
    bot = ZaloBot()
    bot.secret_token = "s3cret"
    assert bot.verify_secret("s3cret") is True
    assert bot.verify_secret("nope") is False
    assert bot.verify_secret("") is False


def test_zalo_bot_chunking_respects_max_len():
    bot = ZaloBot()
    chunks = list(bot._chunks("x" * (MAX_TEXT_LEN * 2 + 137)))
    assert all(len(c) <= MAX_TEXT_LEN for c in chunks)
    assert "".join(chunks) == "x" * (MAX_TEXT_LEN * 2 + 137)


def test_document_loader_returns_list():
    files = DocumentLoader.get_available_files()
    assert isinstance(files, list)
