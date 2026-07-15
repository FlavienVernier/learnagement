from pydantic import BaseModel
from typing import Union, Callable

AccessRule = Union[
    str,        # "anonymous" | "connected_user"
    list[str],  # ["administratif", "enseignant"]
    dict,       # {"roles": [...], "any": {...}, "all": [...], "hierarchy": [...]},
    Callable,   # lambda rule
]


class SQLRequest(BaseModel):
    request: str
    params: dict | None = None
    allowedRolesRequester: AccessRule

    model_config = {"arbitrary_types_allowed": True}
