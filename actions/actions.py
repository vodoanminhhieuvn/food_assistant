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


class ActionSearchFoodRecipe(Action):
    def name(self) -> Text:
        return "action_search_food_recipe"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        entities = [
            e["value"]
            for e in tracker.latest_message["entities"]
            if e["entity"] == "ingredients"
        ]

        if not entities:
            dispatcher.utter_message(
                text="Im not sure what kind recipe you want, can you repeat ?"
            )
        else:
            dispatcher.utter_message(text=f"Let me get {entities[0]} for you, ")
            dispatcher.utter_message(text="Wait for minutes, ")

            return [
                SlotSet("ingredients", entities[0]),
                rasa_sdk.events.FollowupAction("action_get_food_recipe"),
            ]


class ActionGetFoodRecipe(Action):
    def name(self) -> Text:
        return "action_get_food_recipe"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        ingredients = tracker.get_slot("ingredients")

        print(ingredients)

        dispatcher.utter_message(text=f"You want {ingredients} ?")

        # food_label = FoodAPI.get_food_recipe(ingredients=ingredients)
        # dispatcher.utter_message(text=f"{food_label}")

        return []
