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

from actions.models.message_tracker_model import MessageTracker

from actions.api.get_api import SpoonAPI, get_edamam_config
from actions.models.slots import slot


class ActionClearData(Action):
    def name(self) -> Text:
        return "action_clear_data"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        message_tracker = MessageTracker(**tracker.latest_message)

        if message_tracker.intent.name == "clear_all":
            self._clear_all()

        elif message_tracker.intent.name == "clear_nutrient":
            for entity in message_tracker.entities:
                if entity.type == "nutrient_type":
                    self._clear_nutrient(
                        message_tracker.entities[0].value, entity.value
                    )

    def _clear_all():
        print("Clear all")

    def _clear_nutrient(reset_option: str, target: str):
        if reset_option == "reset_all":
            slot.set_nutrient_attr(f"min{target}", None)
            slot.set_nutrient_attr(f"max{target}", None)
        elif reset_option == "reset_min":
            slot.set_nutrient_attr(f"min{target}", None)
        elif reset_option == "reset_max":
            slot.set_nutrient_attr(f"max{target}", None)
