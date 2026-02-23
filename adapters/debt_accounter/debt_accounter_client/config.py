from pydantic_settings import BaseSettings, SettingsConfigDict


class DebtAccounterClientConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='DEBT_ACCOUNTER_CLIENT_')

    HOST: str
