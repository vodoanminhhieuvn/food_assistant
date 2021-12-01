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


tech_descriptions = {
    "baking": "The technique of prolonged cooking of food by dry heat acting by convection, normally in an oven, but can also be done in hot ashes or on hot stones. Appliances like Rotimatic also allow automatic baking.",
    "blind-baking": "Baking pastry before adding a filling.",
    "boiling": "The rapid vaporization of a liquid, which occurs when a liquid is heated to its boiling point, the temperature at which the vapor pressure of the liquid is equal to the pressure exerted on the liquid by the surrounding environmental pressure.",
    "blanching": "Cooking technique which food substance, usually a vegetable or fruit, is plunged into boiling water, removed after a brief, timed interval, and finally plunged into iced water or placed under cold running water (shocked) to halt the cooking process.",
    "braising": "Combination cooking method using both moist and dry heat; typically the food is first seared at a high temperature and then finished in a covered pot with a variable amount of liquid, resulting in a particular flavour.",
    "coddling": "Food is heated in water kept just below the boiling point.",
    "infusion": "The process of soaking plant matter, such as fruits or tea leaves, in a liquid, such as water or alcohol, so as to impart flavor into the liquid.",
    "pressure cooking": "Cooking in a sealed vessel that does not permit air or liquids to escape below a preset pressure, which allows the liquid in the pot to rise to a higher temperature before boiling.",
    "simmering": "Foods are cooked in hot liquids kept at or just below the boiling point of water, but higher than poaching temperature.",
    "poaching": "Process of gently simmering food in liquid, generally milk, stock or wine.",
    "steaming": "Boiling water continuously so it vaporizes into steam and carries heat to the food being steamed, thus cooking the food.",
    "double steaming": "Chinese cooking technique in which food is covered with water and put in a covered ceramic jar and the jar is then steamed for several hours.",
    "steeping": "Saturation of a food (such as an herb) in a liquid solvent to extract a soluble ingredient into the solvent. E.g., a cup of tea is made by steeping tea leaves in a cup of hot water.",
    "stewing": "Food is cooked in liquid and served in the resultant gravy.",
    "vacuum flask cooking": "A thermal cooker, or a vacuum flask cooker, is a cooking device that uses thermal insulation to retain heat and cook food without the continuous use of fuel or other heat source. It is a modern implementation of a haybox, which uses hay or straw to insulate a cooking pot.",
    "grilling": "Grilling is a form of cooking that involves dry heat applied to the surface of food, commonly from above, below or from the side. Grilling usually involves a significant amount of direct, radiant heat, and tends to be used for cooking meat and vegetables quickly. Food to be grilled is cooked on a grill (an open wire grid such as a gridiron with a heat source above or below), using a cast iron/frying pan, or a grill pan (similar to a frying pan, but with raised ridges to mimic the wires of an open grill).",
    "barbecuing": "Method of cooking meat, poultry and occasionally fish with the heat and hot smoke of a fire, smoking wood, or hot coals of charcoal.",
    "frying": "Cooking food in oil or another fat, a technique that originated in ancient Egypt around 2500 BC.",
    "deep frying": "Food is submerged in hot oil or fat. This is normally performed with a deep fryer or chip pan.",
    "gentle frying": "Gentle frying or low-temperature frying is an oil- or fat-based cooking method used for relatively fragile or starchy foods. While gentle frying is most notably used to cook fried eggs, it is also used for delicate fish, tender cuts of meat, sausages, and as a first step in fried potatoes.",
    "hot salt frying": "Hot salt frying and hot sand frying are cooking techniques used by street-side food vendors in Bangladesh, Pakistan, China and India. Hot salt frying is an old cooking technique, and is used in villages throughout Asia and other parts of the world. Many foods are fried with hot salt or sand, even in common households.",
    "pan frying": "Cooking food in a pan using a small amount of cooking oil or fat as a heat transfer agent and to keep the food from sticking.",
    "pressure frying": "In cooking, pressure frying is a variation on pressure cooking where meat and cooking oil are brought to high temperatures while pressure is held high enough to cook the food more quickly. This leaves the meat very hot and juicy. A receptacle used in pressure frying is known as a pressure fryer. The process is most notable for its use in the preparation of fried chicken in many commercial fried chicken restaurants.",
    "sauteing": "Sautéing or sauteing from French in reference to tossing while cooking is a method of cooking that uses a relatively small amount of oil or fat in a shallow pan over relatively high heat. Various sauté methods exist.",
    "shallow frying": "Shallow frying is a hot oil-based cooking technique. It is typically used to prepare portion-sized cuts of meat, fish, potatoes and patties such as fritters. Shallow frying can also be used to cook vegetables.",
    "stir frying": "Stir frying is a Chinese cooking technique in which ingredients are fried in a small amount of very hot oil while being stirred or tossed in a wok. The technique originated in China and in recent centuries has spread into other parts of Asia and the West. It is similar to sautéing in Western cooking technique.",
    "microwave oven": "Type of oven that heats foods quickly and efficiently using microwaves. However, unlike conventional ovens, a microwave oven does not brown bread or bake food. This makes microwave ovens unsuitable for cooking certain foods and unable to achieve certain culinary effects. Additional kinds of heat sources can be added into microwave ovens or microwave packaging so as to add these additional effects.",
    "roasting": "Cooking method that uses dry heat, whether an open flame, oven, or other heat source. Roasting usually causes caramelization or Maillard browning of the surface of the food, which is considered by some as a flavor enhancement.",
    "rotisserie": "Meat is skewered on a spit - a long solid rod used to hold food while it is being cooked over a fire in a fireplace or over a campfire, or while being roasted in an oven.",
    "searing": "Technique used in grilling, baking, braising, roasting, sautéing, etc., in which the surface of the food (usually meat, poultry or fish) is cooked at high temperature so a caramelized crust forms.",
    "smoking": "The process of flavoring, cooking, or preserving food by exposing it to the smoke from burning or smoldering plant materials, most often wood. Hot smoking will cook and flavor the food, while cold smoking only flavors the food.",
    "brining": "Brining is a process similar to marination in which meat or poultry is soaked in brine before cooking",
    "ceviche": "Ceviche, also cebiche, seviche, or sebiche is a South American seafood dish that originated in Peru, typically made from fresh raw fish cured in fresh citrus juices, most commonly lemon or lime, but historically made with the juice of bitter orange. It is also spiced with ají, chili peppers or other seasonings and chopped onions, salt, and coriander are also added. The name originates from the Quechuan word siwichi, which means fresh or tender fish.",
    "drying": "Food drying is a method of food preservation in which food is dried (dehydrated or desiccated). Drying inhibits the growth of bacteria, yeasts, and mold through the removal of water. Dehydration has been used widely for this purpose since ancient times; the earliest known practice is 12,000 B.C. by inhabitants of the modern Middle East and Asia regions. Water is traditionally removed through evaporation by using methods such as air drying, sun drying, smoking or wind drying, although today electric food dehydrators or freeze-drying can be used to speed the drying process and ensure more consistent results.",
    "fermentation": "In food processing, fermentation is the conversion of carbohydrates to alcohol or organic acids using microorganisms—yeasts or bacteria—under anaerobic (oxygen-free) conditions. Fermentation usually implies that the action of microorganisms is desired. The science of fermentation is known as zymology or zymurgy.",
    "marinating": "Marinating is the process of soaking foods in a seasoned, often acidic, liquid before cooking. The origin of the word alludes to the use of brine (aqua marina or sea water) in the pickling process, which led to the technique of adding flavor by immersion in liquid. The liquid in question, the marinade, can be either acidic (made with ingredients such as vinegar, lemon juice, or wine) or enzymatic (made with ingredients such as pineapple, papaya, yogurt, or ginger), or have a neutral pH. In addition to these ingredients, a marinade often contains oils, herbs, and spices to further flavor the food items.",
    "saikyoyaki": "Saikyoyaki is a method of preparing fish in traditional Japanese cuisine by first marinating fish slices overnight in a white miso paste from Kyoto called saikyo shiro miso (西京白味噌). This dish is a speciality of Kyoto and the local white miso used for the marinade is sweeter than other varieties. Secondary ingredients of the marinade include sake and mirin.",
    "pickling": "Pickling is the process of preserving or extending the shelf life of food by either anaerobic fermentation in brine or immersion in vinegar. The pickling procedure typically affects the food's texture and flavor. The resulting food is called a pickle, or, to prevent ambiguity, prefaced with pickled. Foods that are pickled include vegetables, fruits, meats, fish, dairy and eggs.",
    "salting": "Salting is the preservation of food with dry edible salt. It is related to pickling in general and more specifically to brining also known as fermenting (preparing food with brine, that is, salty water) and is one form of curing. It is one of the oldest methods of preserving food, and two historically significant salt-cured foods are salted fish (usually dried and salted cod or salted herring) and salt-cured meat (such as bacon). Vegetables such as runner beans and cabbage are also often preserved in this manner.",
    "seasoning": "Seasoning is the process of adding herbs, salts or spices to food to enhance the flavour.",
    "souring": "Souring is a cooking technique that uses exposure to an acid to cause a physical and chemical change in food. This acid can be added explicitly (for example, in the form of vinegar, lemon juice, lime juice, etc.), or can be produced within the food itself by a microbe such as Lactobacillus. Souring is similar to pickling or fermentation, but souring typically occurs in minutes or hours, while pickling and fermentation can take a much longer time.",
    "sprouting": "Sprouting is the natural process by which seeds or spores germinate and put out shoots, and already established plants produce new leaves or buds or other newly developing parts experience further growth.In the field of nutrition, the term signifies the practice of germinating seeds (for example, mung beans or sunflower seeds) to be eaten raw or cooked, which is considered highly nutritious.",
    "sugaring": "Sugaring is a food preservation method similar to pickling. Sugaring is the process of desiccating a food by first dehydrating it, then packing it with pure sugar. This sugar can be crystalline in the form of table or raw sugar, or it can be a high sugar density liquid such as honey, syrup or molasses.",
    "basting": "Basting is a cooking technique that involves cooking meat with either its own juices or some type of preparation such as a sauce or marinade. The meat is left to cook, then periodically coated with the juice. Prominently used in grilling, rotisserie, roasting, and other meat preparations where the meat is over heat for extended periods of time, basting is used to keep meat moist during the cooking process and also to apply or enhance flavor. Improperly administered basting, however, may actually lead to the very problem it is designed to prevent: the undesired loss of moisture (drying out) of the meat.",
    "cutting": "Cutting is the separation or opening of a physical object, into two or more portions, through the application of an acutely directed force.",
    "dicing": "Cutting into cubes",
    "grating ": " The use of a grater to mash vegetables.",
    "julienning ": "Cutting into very thin pieces such as the thin carrots in store bought salad mix",
    "mincing ": "Cutting into very small pieces",
    "peeling ": "To take the outer skin/covering off of a fruit or vegetable",
    "shaving ": "scrape the outer skin of a vegetable or fruit",
    "chiffonade": "Cutting in a ribbon like way",
    "milling": "tear food into small pieces",
    "kneading": "In cooking (and more specifically baking), kneading is a process in the making of bread or dough, used to mix the ingredients and add strength to the final product. Its importance lies in the mixing of flour with water; when these two ingredients are combined and kneaded, the gliadin and glutenin proteins in the flour expand and form strands of gluten, which gives bread its texture. (To aid gluten production, many recipes use bread flour, which is higher in protein than all-purpose flour.) The kneading process warms and stretches these gluten strands, eventually creating a springy and elastic dough. If bread dough is not kneaded enough, it will not be able to hold the tiny pockets of gas (carbon dioxide) created by the leavening agent (such as yeast or baking powder), and will collapse, leaving a heavy and dense loaf.",
    "mixing": "Incorporating different ingredients to make something new; such as how mixing water, sugar, and lemon juice makes lemonade",
    "blending": "Using a machine called blender to grind ingredients"
}


class ActionSearchFoodRecipe(Action):
    def name(self) -> Text:
        return "action_answer_prepare_technique"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        message_tracker = MessageTracker(**tracker.latest_message)
        correct_technique = False
        for entity in message_tracker.entities:
            if entity.type == 'preparation_technique':
                dispatcher.utter_message(
                    text=tech_descriptions[entity.value.lower()])
                correct_technique = True
        if not correct_technique:
            dispatcher.utter_message(
                text="Could you repeat what you're trying to know ?")
        return []
