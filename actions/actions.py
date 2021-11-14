from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
import rasa_sdk
from rasa_sdk.types import DomainDict
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import (
    SlotSet,
    UserUtteranceReverted,
    ConversationPaused,
    EventType,
)

import os

from actions.api.food_api import FoodAPI


class ActionFinishAsking(Action):
    def name(self) -> Text:
        return "action_get_nutrient"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        print("Finish")
        