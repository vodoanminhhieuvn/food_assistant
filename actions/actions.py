from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
import rasa_sdk
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

from actions.api.food_api import FoodAPI
from actions.food_utils import Nutrients


class ActionSearchFoodRecipe(Action):
    def name(self) -> Text:
        return "action_search_food_recipe"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        print("------------------")
        recipe_parts = tracker.get_slot("recipe_parts")
        print(recipe_parts)
        entities = tracker.latest_message["entities"]
        has_ingredient_in_old = any(
            item["entity"] == "ingredient" for item in recipe_parts
        )
        has_technique_in_old = any(
            item["entity"] == "preparation_technique" for item in recipe_parts
        )
        has_ingredient_in_new = any(item["entity"] == "ingredient" for item in entities)
        has_technique_in_new = any(
            item["entity"] == "preparation_technique" for item in entities
        )

        # Check should clear list entity
        if (
            has_ingredient_in_new
            and has_ingredient_in_old
            or has_technique_in_new
            and has_technique_in_old
        ):
            recipe_parts = []

        # Update recipe parts
        recipe_parts += entities
        text_length = len(tracker.latest_message["text"])
        for item in recipe_parts:
            item["start"] -= text_length
            item["end"] -= text_length

        results = []
        results.append(SlotSet("recipe_parts", recipe_parts))
        # Check for missing components => utter request
        if not any(item["entity"] == "ingredient" for item in recipe_parts):
            dispatcher.utter_message(text="Give me main ingredient")
            return results
        elif not any(
            item["entity"] == "preparation_technique" for item in recipe_parts
        ):
            dispatcher.utter_message(text="You can provide me a technique")
            return results

        # Else
        # Sort list
        def compareTo(e):
            return e["start"]

        recipe_parts.sort(key=compareTo)

        # Remove redundant operator
        for index, val in enumerate(recipe_parts):
            if val["entity"] == "or" and (
                index == 0
                or index == len(recipe_parts) - 1
                or recipe_parts[index + 1]["entity"] == "or"
            ):
                del recipe_parts[index]

        print(list(map(lambda x: x["value"], recipe_parts)))

        # Run handle creating search keywords by rule
        # ? type or and
        # ? same x2  +
        # ? diff X   +
        search_list = []

        branch_list = []
        index = 0
        while index < len(recipe_parts):
            bl_len = len(branch_list)
            if recipe_parts[index]["entity"] == "or":
                if (
                    recipe_parts[index - 1]["entity"]
                    == recipe_parts[index + 1]["entity"]
                ):
                    for i in range(bl_len):
                        raw_item = branch_list[0]
                        del raw_item[-1]
                        branch_list.append(raw_item + [recipe_parts[index - 1]])
                        branch_list.append(raw_item + [recipe_parts[index + 1]])
                        del branch_list[0]
                    index += 1
            else:
                if bl_len == 0:
                    branch_list.append([recipe_parts[index]])
                else:
                    for item in branch_list:
                        item.append(recipe_parts[index])
            index += 1

        for item in branch_list:
            search_list.append(item[0]["value"])
            for i in range(1, len(item)):
                search_list[-1] += " " + item[i]["value"]

        # result utter
        results.append(SlotSet("search_list", search_list))
        print(search_list)

        dispatcher.utter_message("Your mind is:")
        for item in search_list:
            dispatcher.utter_message(item)

        # results.append(rasa_sdk.events.FollowupAction(
        #     "action_get_food_recipe"))
        return results

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

""" [nutrient_slot] to set Slot after calling Get Nutrient """
nutrient_slots = {
    "calory_min": None,
    "calory_max": None,
    "fat_min": None,
    "fat_max": None,
}

class ActionGetNutrient(Action):
    def name(self) -> Text:
        return "action_get_nutrient"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        min_value = []
        max_value = []
        nutrient_type = []

        tracker_entities = tracker.latest_message["entities"]

        for entity in tracker_entities:
            if entity["entity"] == "min":
                min_value.append(entity["value"])
            elif entity["entity"] == "max":
                max_value.append(entity["value"])
            elif entity["entity"] == "nutrient":
                nutrient_type.append(entity["value"])
                
        self._check_valid_nutrient(dispatcher, nutrient_type)
        self._add_min_to_slot(dispatcher, min_value, nutrient_type[0])
        self._add_max_to_slot(dispatcher, max_value, nutrient_type[0])
        
        print(nutrient_slots)

        return []
    
    def _check_valid_nutrient(self, dispatcher, nutrient_type):
        if len(nutrient_type) >= 2:
            return self._too_much_info(
                dispatcher, "You can't input 2 nutrient type values"
            )
        elif len(nutrient_type) != 0:  
            valid = Nutrients.containNutrient(nutrient_type[0])
            if not valid:
                return []
    
    def _add_min_to_slot(self, dispatcher, min_values, nutrient_type):
        if len(min_values) >= 2:
            return self._too_much_info(
                dispatcher, "You can't input 2 minium type values"
            )
        
        elif len(min_values) != 0:
            nutrient_slots[f"{nutrient_type}_min"] = min_values[0]
            
    def _add_max_to_slot(self, dispatcher, max_values, nutrient_type):
        if len(max_values) >= 2:
            return self._too_much_info(
                dispatcher, "You can't input 2 maximum type values"
            )
        elif len(max_values) != 0:
            nutrient_slots[f"{nutrient_type}_max"] = max_values[0]
        
    def _too_much_info(self, dispatcher, text):
        dispatcher.utter_message(text=text)
        dispatcher.utter_message(text="Please input only 1 value of each type")
        
        return []
