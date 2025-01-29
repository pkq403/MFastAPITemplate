from fastapi import FastAPI
import loguru
from sqlalchemy import event
from src.config.db.database_setup import engine, Base
from ...models import *

@event.listens_for(engine, "connect")
def log_connection(db_api_connection, connection_record):
    loguru.logger.info(f"New PgSQL connection ---\n {db_api_connection}")
    loguru.logger.info(f"Connection Record ---\n {connection_record}")


@event.listens_for(engine, "close")
def log_connection_close(db_api_connection, connection_record):
    loguru.logger.info(f"Closing PgSQL connection ---\n {db_api_connection}")
    loguru.logger.info(f"Closed Connection Record ---\n {connection_record}")


def initialize_db_tables() -> None:
    loguru.logger.info("Database Table Creation --- Initializing . . .")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    loguru.logger.info("Database Table Creation --- Succesfully Initialized!")


def initialize_db_connection(backend_app: FastAPI) -> None:
    loguru.logger.info("Database Connection --- Establishing . . .")
    backend_app.state.db = engine
    initialize_db_tables() # if u want to reset db each time fastapi reloads)
    loguru.logger.info("Database Connection --- Succesfully Establised!")


def dispose_db_connection(backend_app: FastAPI) -> None:
    loguru.logger.info("Database Connection --- Disposing . . .")
    engine.dispose()
    loguru.logger.info("Database Connection --- Succesfully Disposed!")
