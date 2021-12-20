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


list_ingredient: List[Ingredient] = []


class ActionHowToCook(Action):
    def name(self) -> Text:
        return "action_how_to_cook"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        try:
            message_tracker = MessageTracker(**tracker.latest_message)
        except:
            return []

        try:
            food_model: RecipeModel = food_data.list_food_model[
                int(message_tracker.entities[0].value)
            ]
        except:
            return []

        message = "".join(
            f"{ingredient} \n" for ingredient in food_model.ingredient_lines
        )

        button_message: List[ButtonMessageModel] = []

        for index, ingredient in enumerate(food_model.ingredients):
            ingredient_name = ingredient.text
            button_message.append(
                ButtonMessageModel(
                    title=ingredient_name, payload=f"ingredient option {index}"
                ).dict()
            )

        dispatcher.utter_message(image=food_model.image)
        dispatcher.utter_message(text=message, buttons=button_message)

        list_ingredient.append(food_model.ingredients)

        return []


class ActionIngredientDetail(Action):
    def name(self) -> Text:
        return "action_ingredient_detail"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        try:
            message_tracker = MessageTracker(**tracker.latest_message)
        except:
            dispatcher.utter_message(text="Error occurred: Can't load entity")
            return []

        try:
            ingredient_model: Ingredient = list_ingredient[
                int(message_tracker.entities[0].value)
            ]
        except:
            dispatcher.utter_message(text="Error occurred: Can't load ingredient model")
            return []

        # message = "".join(f"{field}: {value} \n" for field, value in ingredient_model)

        dispatcher.utter_message(text="Finish Ingredient")

        return []
