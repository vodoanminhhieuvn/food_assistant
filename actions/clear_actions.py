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
        return "action_clear_data"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        message_tracker = MessageTracker(**tracker.latest_message)

        nutrient_reset_option: List[str] = []
        nutrient_type: List[str] = []

        if message_tracker.intent.name == "clear_all":
            self._clear_all()

        elif message_tracker.intent.name == "clear_nutrient":
            for entity in message_tracker.entities:
                if entity.type == "nutrient_type":
                    nutrient_type.append(entity.value)
                elif entity.type == "nutrient_reset_option":
                    nutrient_reset_option.append(entity.value)

            self._clear_nutrient(nutrient_reset_option[-1], nutrient_type)

    def _clear_all(self):
        print("Clear all")

    def _clear_nutrient(self, reset_option: str, targets: List[str]):
        print(reset_option)
        print(targets)
        for target in targets:
            if reset_option == "reset_all":
                slot.nutrient_slots = NutrientModel(
                    **slot.nutrient_slots.copy(
                        update={f"min{target}": None, f"max{target}": None}
                    ).dict()
                )

            elif reset_option == "reset_min":
                slot.nutrient_slots = NutrientModel(
                    **slot.nutrient_slots.copy(update={f"min{target}": None}).dict()
                )
            elif reset_option == "reset_max":
                slot.nutrient_slots = NutrientModel(
                    **slot.nutrient_slots.copy(update={"max{target}": None}).dict()
                )
