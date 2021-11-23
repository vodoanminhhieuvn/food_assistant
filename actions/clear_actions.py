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

from actions.api.get_api import SpoonAPI, get_edamam_config


class ActionClearData(Action):
    def name(self) -> Text:
        return "action_clear_data"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        SpoonAPI.getRecipes()
        # tracker_intent = tracker.latest_message["intent"]
        # tracker_entities = tracker.latest_message["entities"]
        # print(tracker_intent)
        # print(tracker_entities)

    def clear_calory():
        print("Clear calory")

    def clear_fat():
        print("Clear fat")
