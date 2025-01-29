from enum import Enum

class Environment(str, Enum):
    PRODUCTION: str = "PROD"
    DEVELOPMENT: str = "DEV"
    STAGING: str = "STAGE"