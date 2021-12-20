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
from actions.models.nutrient_model import NutrientModel


class ActionClearData(Action):
    def name(self) -> Text:
        return "action_help"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        return []


# TODO handle help intent fuck you fuck you again
# Help intent
# - Summary
# - How to get ingredient
# - How to set nutrient
# - How to cook recipe
# - Recipe detail
# - ingredient detail
# - Ask for meal plan
# - Ask for food technique
# - Ask for recipe
