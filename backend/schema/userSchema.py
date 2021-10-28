from datetime import datetime
from typing import Optional
from odmantic import Model


class User(Model):
    firstname: str
    lastname: str
    email: str
    password: str
    is_active: bool = True
    is_admin: bool = True
    create_at: Optional[datetime] = datetime.utcnow()
