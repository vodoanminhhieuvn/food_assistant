from typing import Any, Text, Dict, List


from rasa_sdk import Action, Tracker
from rasa_sdk.types import DomainDict
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import (
    SlotSet,
    UserUtteranceReverted,
    ConversationPaused,
    EventType,
)
from actions.api.get_api import SpoonAPI

from actions.models.slots import Slot


class ActionFinishAsking(Action):
    def name(self) -> Text:
        return "action_get_data"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        print(tracker.latest_message)
        SpoonAPI.getRecipes()
        print(Slot.nutrient_slots)

        return []
