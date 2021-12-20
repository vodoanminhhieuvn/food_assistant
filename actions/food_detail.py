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
        return "action_get_food_detail"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        try:
            message_tracker = MessageTracker(**tracker.latest_message)
        except:
            dispatcher.utter_message(text="Error has occurred: No entity found")
            return []

        try:
            food_model = food_data.list_current_food[0]

        except:
            dispatcher.utter_message(text="Error has occurred: No food model found")
            return []

        message = "".join(
            f"{value.label}: {value.quantity / food_model.yield_} {value.unit} \n"
            for field, value in food_model.total_nutrients
        )

        button_message: List[ButtonMessageModel] = []

        for index, food_model_index in enumerate(food_data.list_current_food):
            food_name = food_model_index.label
            button_message.append(
                ButtonMessageModel(
                    title=food_name, payload=f"food option {index}"
                ).dict()
            )

        button_message.append(
            ButtonMessageModel(
                title=f"How to cook {food_name}",
                payload=f"How to cook {message_tracker.entities[0].value}",
            ).dict()
        )

        dispatcher.utter_message(text=f"{food_model.label}")

        dispatcher.utter_message(image=food_model.image)
        dispatcher.utter_message(text=message, buttons=button_message)

        return []
