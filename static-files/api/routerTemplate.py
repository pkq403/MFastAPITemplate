from fastapi import APIRouter
from src.api.controllers.devController import dev_controller
from .prefixes import Prefix

router = APIRouter()

router.include_router(router=dev_controller,
                      prefix=Prefix.dev_prefix.value,
                      tags=["dev"])
