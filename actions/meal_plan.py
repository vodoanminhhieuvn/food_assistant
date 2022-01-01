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
from actions.models.food_model import Ingredient
from actions.api.get_api import SpoonAPI

import json

global list_ingredient


class ActionHowToCook(Action):
    def name(self) -> Text:
        return "action_meal_plan"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        SpoonAPI.getMealPlan()

        message = "".join(
            f"{field}: {value} \n" for field, value in food_data.meal_plan.nutrients
        )

        button_message: List[ButtonMessageModel] = []

        for meal in food_data.meal_plan.meals:
            food_name: str = meal.title

            button_message.append(
                ButtonMessageModel(
                    title=food_name,
                    payload="/spoon_food_recipe"
                    + json.dumps({"recipe_search_name": food_name}),
                ).dict()
            )

        dispatcher.utter_message(text=message, buttons=button_message)

        return []
