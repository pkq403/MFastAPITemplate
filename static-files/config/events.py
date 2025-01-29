from fastapi import FastAPI
import loguru
from src.config.db.db_events import initialize_db_connection, dispose_db_connection

def execute_backend_server_event_handler(backend_app: FastAPI) -> None:
    loguru.logger.info("Starting FastAPI Server ...")
    def launch_backend_server_events() -> None:
        initialize_db_connection(backend_app=backend_app)
    return launch_backend_server_events

def terminate_backend_server_event_handler(backend_app: FastAPI) -> None:
    loguru.logger.info("Terminating FastAPI Server ...")
    def stop_backend_server_events() -> None:
        dispose_db_connection(backend_app=backend_app)
    return stop_backend_server_events