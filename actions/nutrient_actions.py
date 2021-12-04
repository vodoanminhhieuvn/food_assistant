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
from actions.models.message_tracker_model import MessageTracker
from actions.models.slots import Slot, slot
from actions.utils.food_utils import Nutrients


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

        message_tracker = MessageTracker(**tracker.latest_message)

        slot.nutrient_slots.minCalories = 500
        slot.nutrient_slots.maxCalories = 50
        print(slot.nutrient_slots)

        # for entity in message_tracker.entities:
        #     if entity.type == "min":
        #         min_value.append(entity.value)
        #     elif entity.type == "max":
        #         max_value.append(entity.value)
        #     elif entity.type == "nutrient":
        #         nutrient_type.append(entity.value)

        # self._check_valid_nutrient(dispatcher, nutrient_type)
        # self._add_min_to_slot(dispatcher, min_value, nutrient_type[0])
        # self._add_max_to_slot(dispatcher, max_value, nutrient_type[0])

        # return []

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
            Slot.set_nutrient_attr(f"min{nutrient_type}", min_values[0])

    def _add_max_to_slot(
        self, dispatcher: CollectingDispatcher, max_values: list, nutrient_type: str
    ):
        if len(max_values) >= 2:
            return self._too_much_info(
                dispatcher, "You can't input 2 maximum type values"
            )

        elif len(max_values) != 0:
            Slot.set_nutrient_attr(f"min{nutrient_type}", max_values[0])

    def _too_much_info(self, dispatcher, text):
        dispatcher.utter_message(text=text)
        dispatcher.utter_message(text="Please input only 1 value of each type")

        return []
