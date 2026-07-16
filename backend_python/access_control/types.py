from typing import Union
from pydantic import BaseModel

# Type récursif pour allowedRolesRequester
AccessRule = Union[
    str,            # "anonymous" | "connected_user"
    list[str],      # ["administratif", "enseignant"]
    dict,           # {"roles": [...], "one": {...}, "all": {...}, "hierarchy": {...}}
]

class Responsibility(BaseModel):
    type_objet:  str
    dimensions:  dict[str, str] = {}  # {"resp": "stage", "filiere": "IDU", "niveau": "FI4", ...}