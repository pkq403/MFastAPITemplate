from functools import lru_cache
import decouple
from src.config.settings.base import BackendBaseSettings
from src.config.settings.development import BackendDevSettings
from src.config.settings.production import BackendProdSettings
from src.config.settings.environment import Environment

class BackendSettingsFactory:
    def __init__(self, environment: str):
        self.enviroment = environment

    def __call__(self) -> BackendBaseSettings:
        if self.enviroment == Environment.DEVELOPMENT.value:
            return BackendDevSettings()
        return BackendProdSettings()
    
@lru_cache()
def get_settings() -> BackendBaseSettings:
    return BackendSettingsFactory(environment=decouple.config("ENVIRONMENT", default="DEV", cast=str))()  # type: ignore


settings: BackendBaseSettings = get_settings()