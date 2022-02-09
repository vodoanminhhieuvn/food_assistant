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
from actions.models.recipe_parts_model import RecipePartsModel
from actions.models.recipe_search_keyword import RecipeSearchKeyword


class ActionGetNutrient(Action):
    def name(self) -> Text:
        return "action_ingredient_setting"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        try:
            list_keywords_model = slot.recipe_search_keyword_slots.keywords

            if list_keywords_model:
                dispatcher.utter_message("Here's your search keywords")
                message = "".join(f"{keyword}\n" for keyword in list_keywords_model)
                dispatcher.utter_message(message)

            else:
                dispatcher.utter_message(
                    "Seem like you haven't had any search keyword yet"
                )

            return []
        except:
            dispatcher.utter_message("Seem like you haven;t had any search keyword yet")
            return []


class ActionResetIngredient(Action):
    def name(self) -> Text:
        return "action_reset_ingredient"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        slot.recipe_parts_slots = RecipePartsModel()
        slot.recipe_search_keyword_slots = RecipeSearchKeyword()

        dispatcher.utter_message("Ingredient has been reset")

        return []
