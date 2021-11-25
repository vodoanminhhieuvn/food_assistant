from typing import List, Optional
from actions.models.message_tracker_model import Entity
from pydantic import BaseModel

class RecipeSearchKeyword(BaseModel):
    keywords: list = []