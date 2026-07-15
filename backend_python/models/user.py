from pydantic import BaseModel


class User(BaseModel):
    id: int
    prenom: str
    nom: str
    mail: str | None = None
    ExplicitSecondaryK: str
    main_role: str
    roles: list = []
    responsibilities: list = []
    password2update: bool = False


class UserInDB(User):
    password: str
