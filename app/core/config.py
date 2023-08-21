from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Помощь котикам'
    app_description: str = 'Приложение для сбора пожертвований.'
    database_url: str = 'sqlite+aiosqlite:///./qrkot.db'
    secret: str = 'BIGSECRET'

    class Config:
        env_file = '.env'


settings = Settings()
