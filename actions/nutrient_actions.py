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
from actions.models.nutrient_model import NutrientModel


class ActionGetNutrient(Action):
    def name(self) -> Text:
        return "action_get_nutrient"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        min_values = []
        max_values = []
        nutrient_type = []

        message_tracker = MessageTracker(**tracker.latest_message)

        for entity in message_tracker.entities:
            if entity.type == "min":

                min_values.append(entity.value)

            elif entity.type == "max":

                max_values.append(entity.value)

            elif entity.type == "nutrient":
                nutrient_type.append(entity.value)

        if not (self._check_valid_nutrient(dispatcher, nutrient_type)):
            return []

        if not (
            self._add_nutrient_to_slot(
                dispatcher, min_values, max_values, nutrient_type[0]
            )
        ):
            return []

        minDisplayValue = slot.nutrient_slots.dict()[f"min{nutrient_type[0]}"]
        maxDisplayValue = slot.nutrient_slots.dict()[f"max{nutrient_type[0]}"]

        dispatcher.utter_message(
            text=f"{nutrient_type[0]}\nMin: {minDisplayValue} - Max: {maxDisplayValue}"
        )

        return []

    def _check_valid_nutrient(
        self, dispatcher: CollectingDispatcher, nutrient_type: list
    ):
        if len(nutrient_type) >= 2:
            return self._too_much_info(
                dispatcher, "You can't input 2 nutrient type values"
            )
        return True

    def _add_nutrient_to_slot(
        self,
        dispatcher: CollectingDispatcher,
        min_values: list,
        max_values: list,
        nutrient_type: str,
    ):
        if len(min_values) >= 2 or len(max_values) >= 2:
            return self._too_much_info(
                dispatcher, "You can't input 2 minium or maximum type values"
            )

        slot.nutrient_slots = NutrientModel(
            **slot.nutrient_slots.copy(
                update={
                    f"min{nutrient_type}": min_values[0]
                    if 0 < len(min_values)
                    else slot.nutrient_slots.dict()[f"min{nutrient_type}"],
                    f"max{nutrient_type}": max_values[0]
                    if 0 < len(max_values)
                    else slot.nutrient_slots.dict()[f"max{nutrient_type}"],
                }
            ).dict()
        )

        return True

    def _too_much_info(self, dispatcher, text):
        dispatcher.utter_message(text=text)
        dispatcher.utter_message(text="Please input only 1 value of each type")

        return False
