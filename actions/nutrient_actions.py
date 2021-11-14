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

import os

from actions.api.food_api import FoodAPI
from actions.utils.food_utils import Nutrients


""" [nutrient_slot] to set Slot after calling Get Nutrient """
nutrient_slots = {
    "calory_min": None,
    "calory_max": None,
    "fat_min": None,
    "fat_max": None,
}


class ActionGetNutrient(Action):
    def name(self) -> Text:
        return "action_get_nutrient"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        min_value = []
        max_value = []
        nutrient_type = []

        tracker_entities = tracker.latest_message["entities"]

        for entity in tracker_entities:
            if entity["entity"] == "min":
                min_value.append(entity["value"])
            elif entity["entity"] == "max":
                max_value.append(entity["value"])
            elif entity["entity"] == "nutrient":
                nutrient_type.append(entity["value"])

        self._check_valid_nutrient(dispatcher, nutrient_type)
        self._add_min_to_slot(dispatcher, min_value, nutrient_type[0])
        self._add_max_to_slot(dispatcher, max_value, nutrient_type[0])

        print(nutrient_slots)

        return [SlotSet(slot, value) for slot, value in nutrient_slots.items()]

    def _check_valid_nutrient(
        self, dispatcher: CollectingDispatcher, nutrient_type: list
    ):
        if len(nutrient_type) >= 2:
            return self._too_much_info(
                dispatcher, "You can't input 2 nutrient type values"
            )
        elif len(nutrient_type) != 0:
            valid = Nutrients.containNutrient(nutrient_type[0])
            if not valid:
                return []

    def _add_min_to_slot(
        self, dispatcher: CollectingDispatcher, min_values: list, nutrient_type: str
    ):
        if len(min_values) >= 2:
            return self._too_much_info(
                dispatcher, "You can't input 2 minium type values"
            )

        elif len(min_values) != 0:
            nutrient_slots[f"{nutrient_type}_min"] = min_values[0]

    def _add_max_to_slot(
        self, dispatcher: CollectingDispatcher, max_values: list, nutrient_type: str
    ):
        if len(max_values) >= 2:
            return self._too_much_info(
                dispatcher, "You can't input 2 maximum type values"
            )
        elif len(max_values) != 0:
            nutrient_slots[f"{nutrient_type}_max"] = max_values[0]

    def _too_much_info(self, dispatcher, text):
        dispatcher.utter_message(text=text)
        dispatcher.utter_message(text="Please input only 1 value of each type")

        return []