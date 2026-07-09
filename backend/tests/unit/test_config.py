from app.core.config import Settings


def test_settings_load_default_values() -> None:
    settings = Settings()

    assert settings.app_name == "Industrial Edge Monitoring Platform API"
    assert settings.app_env == "local"
    assert settings.api_v1_prefix == "/api/v1"
    assert settings.log_level == "INFO"
    assert settings.jwt_algorithm == "HS256"
    assert settings.access_token_expire_minutes == 30
    assert settings.device_api_key_header == "X-Device-Api-Key"
    assert settings.enable_metrics is True
    assert settings.enable_tracing is False


def test_settings_allow_environment_override(monkeypatch) -> None:
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("ENABLE_TRACING", "true")

    settings = Settings()

    assert settings.app_env == "test"
    assert settings.log_level == "DEBUG"
    assert settings.enable_tracing is True
