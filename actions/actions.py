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

from actions.api.food_api import FoodAPi


class ActionGetFoodRecipe(Action):
    def name(self) -> Text:
        return "action_get_food_recipe"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        entities = [
            e["value"]
            for e in tracker.latest_message["entities"]
            if e["entity"] == "food_recipe"
        ]

        if len(entities) == 0:
            dispatcher.utter_message(
                text="Im not sure what kind recipe you want, can you repeat ?"
            )
            return []
        else:
            dispatcher.utter_message(text=f"Let me get {entities} for you, ")
            dispatcher.utter_message(text="Wait for minutes, ")
            print(entities)
            return []
