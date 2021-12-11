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
from actions.api.get_api import SpoonAPI

from actions.models.slots import Slot
from actions.models.data import food_data
from actions.models.food_model import FoodModel
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

        SpoonAPI.getRecipes()

        # button_message: List[ButtonMessageModel] = []

        # for index, food_model in enumerate(food_data.list_food_model):
        #     food_name = food_model.title
        #     button_message.append(
        #         ButtonMessageModel(
        #             title=food_name, payload=f"get me food at {index}"
        #         ).dict()
        #     )
        #     dispatcher.utter_message(text=food_name)

        # dispatcher.utter_message(text="Here your foods", buttons=button_message)

        return []
