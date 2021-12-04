from pydantic import BaseModel, Field
from typing import List, Literal, Optional


class ButtonMessageModel(BaseModel):
    title: str
    payload: str
