from typing import Any, Text, Dict, List


from rasa_sdk import Action, Tracker
from rasa_sdk.types import DomainDict
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import (
    FollowupAction,
    SessionStarted,
    SlotSet,
    UserUtteranceReverted,
    ConversationPaused,
    EventType,
)
from actions.api.get_api import SpoonAPI

from actions.models.slots import slot
from actions.models.data import food_data
from actions.models.food_model import RecipeModel
from actions.models.button_message_model import ButtonMessageModel


class ActionFinishAsking(Action):
    def name(self) -> Text:
        return "action_get_data"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        if not slot.recipe_search_keyword_slots.keywords:

            has_ingredient = any(
                item.type == "ingredient" for item in slot.recipe_parts_slots.parts
            )

            if not has_ingredient:
                dispatcher.utter_message(text="Please provide me more ingredient")

                return []

            dispatcher.utter_message(
                text="It's seem you don't have any search key word yet"
            )
            dispatcher.utter_message(
                text="you can type: I want to cook chicken : to set search keyword"
            )

            return []

        SpoonAPI.getRecipes()

        button_message: List[ButtonMessageModel] = []

        for index, food_model_index in enumerate(food_data.list_current_food):
            food_name = food_model_index.label
            button_message.append(
                ButtonMessageModel(
                    title=food_name, payload=f"food option {index}"
                ).dict()
            )

        dispatcher.utter_message(text="Here your foods", buttons=button_message)

        return []
