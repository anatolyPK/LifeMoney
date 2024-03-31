from pydantic import BaseModel
from typing import NewType


PyModel = NewType("PyModel", BaseModel)