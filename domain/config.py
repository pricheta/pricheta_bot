from pydantic_settings import BaseSettings, SettingsConfigDict


class BotConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='BOT_')

    TOKEN: str
    USER_ANSWER_TIMEOUT: int
    GET_TRANSFER_HISTORY_DEFAULT_LOOKBACK: int
    COMMON_CHANNEL: bool


config = BotConfig()
