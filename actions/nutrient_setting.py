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
        return "action_nutrient_setting"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        try:
            message_tracker = MessageTracker(**tracker.latest_message)
            nutrient_model = slot.nutrient_slots
            target = message_tracker.entities[0].value
            if target == "Nutrient":
                message = "".join(
                    f"{field}: {value}\n" for field, value in nutrient_model
                )

            else:
                minProperty = f"min{target}"
                maxProperty = f"max{target}"
                minValue = nutrient_model.dict()[minProperty]
                maxValue = nutrient_model.dict()[maxProperty]

                message = "".join(f"{target} \n min: {minValue} \n max: {maxValue}")

            dispatcher.utter_message(message)

            return []

        except:
            dispatcher.utter_message("We can't load your setting, please try again")
            return []
