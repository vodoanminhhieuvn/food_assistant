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
from actions.models.data import food_data
from actions.models.food_model import RecipeModel
from actions.models.button_message_model import ButtonMessageModel
from actions.models.slots import slot


class ActionSetDiet(Action):
    def name(self) -> Text:
        return "action_set_diet"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        diet_entity = ""

        try:
            message_tracker = MessageTracker(**tracker.latest_message)

            for entity in message_tracker.entities:
                if entity.type == "diet":
                    diet_entity = entity.value
        except:
            dispatcher.utter_message("There something wrong with setting diet")
            return []

        slot.diet = diet_entity

        dispatcher.utter_message(text=f"Diet: {slot.diet}")

        return []


class ActionShowDiet(Action):
    def name(self) -> Text:
        return "action_show_diet"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        if slot.diet:
            dispatcher.utter_message(f"Here your diet setting: {slot.diet}")
        else:
            dispatcher.utter_message("You haven't set any diet setting yet")
            dispatcher.utter_message(
                "You can type: set diet setting to vegan : to set diet setting"
            )

        return []


class ActionResetDiet(Action):
    def name(self) -> Text:
        return "action_reset_diet"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        slot.diet = ""

        dispatcher.utter_message("Diet has been reset")

        print(slot.diet)

        return []
