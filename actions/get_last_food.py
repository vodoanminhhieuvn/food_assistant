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


class ActionGetFoodDetail(Action):
    def name(self) -> Text:
        return "action_get_last_food"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        button_message: List[ButtonMessageModel] = []

        try:
            list_current_food = food_data.list_current_food
            for index, food_model_index in enumerate(list_current_food):
                food_name = food_model_index.label
                button_message.append(
                    ButtonMessageModel(
                        title=food_name, payload=f"food option {index}"
                    ).dict()
                )

            dispatcher.utter_message(
                text="Here your previous foods", buttons=button_message
            )

        except:
            dispatcher.utter_message(
                text="Can't get previous recipe, did you get recipe?"
            )
            return []
