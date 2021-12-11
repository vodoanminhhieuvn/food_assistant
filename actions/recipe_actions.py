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

class ActionSearchFoodRecipe(Action):
    def name(self) -> Text:
        return "action_search_food_recipe"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        message_tracker = MessageTracker(**tracker.latest_message)
     
        # Check should clear list entity
        slot.recipe_parts_slots.checkShouldClear(message_tracker.entities)

        # Update recipe parts
        slot.recipe_parts_slots.append_list(message_tracker.entities)

        # Check for missing components => utter request
        if(self._request_more_part(dispatcher, slot.recipe_parts_slots.parts)):
            return []
        # Else
        # Sort list
        slot.recipe_parts_slots.refactor()

        # Run handle creating search keywords by rule
        slot.recipe_search_keyword_slots.keywords = slot.recipe_parts_slots.createSearchKeywords()
        
        # result utter
        dispatcher.utter_message("Your mind is:")
        for item in slot.recipe_search_keyword_slots.keywords:
            dispatcher.utter_message(item)

        # results.append(rasa_sdk.events.FollowupAction(
        #     "action_get_food_recipe"))
        return []

        # if not entities:
        #     dispatcher.utter_message(
        #         text="Im not sure what kind recipe you want, can you repeat ?"
        #     )
        # else:
        #     dispatcher.utter_message(
        #         text=f"Let me get {entities[0]} for you, ")
        #     dispatcher.utter_message(text="Wait for minutes, ")

        #     return [
        #         SlotSet("ingredient", entities[0]),
        #         rasa_sdk.events.FollowupAction("action_get_food_recipe"),
        #     ]
        
    def _request_more_part(self, dispatcher: CollectingDispatcher, recipe_parts: list) -> bool:
        if all(item.type != "ingredient" for item in recipe_parts):
            dispatcher.utter_message(text="Give me main ingredient")
            return True
        elif all(
            item.type != "cook_technique" for item in recipe_parts
        ):
            dispatcher.utter_message(text="You can provide me a technique")
            return True
        else: return False


class ActionGetFoodRecipe(Action):
    def name(self) -> Text:
        return "action_get_food_recipe"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        print("Hello World")
        ingredients = tracker.get_slot("ingredient")

        print(ingredients)

        dispatcher.utter_message(text=f"You want {ingredients} ?")

        # food_label = FoodAPI.get_food_recipe(ingredients=ingredients)
        # dispatcher.utter_message(text=f"{food_label}")

        return []
