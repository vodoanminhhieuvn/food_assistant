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


class ActionGetFoodDetail(Action):
    def name(self) -> Text:
        return "action_get_food_detail"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        message_tracker = MessageTracker(**tracker.latest_message)

        food_model: RecipeModel = food_data.list_food_model[
            int(message_tracker.entities[0].value)
        ]

        message = "".join(
            f"{value.label}: {value.quantity / food_model.yield_} {value.unit} \n"
            for field, value in food_model.total_nutrients
        )

        dispatcher.utter_message(image=food_model.image)
        dispatcher.utter_message(text=message)

        return []


class ActionHowToCook(Action):
    def name(self) -> Text:
        return "action_how_to_cook"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        message_tracker = MessageTracker(**tracker.latest_message)

        print(message_tracker.entities)

        return []
