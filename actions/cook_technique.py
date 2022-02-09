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
    "acidulate": "To use an acid (such as that found in citrus juice, vinegar, or wine) to prevent browning, alter flavour, or make an item safe for canning.",
    "al dente": "To cook food (typically pasta) to the point where it is tender but not mushy.",
    "amandine": "A culinary term indicating a garnish of almonds. A dish served amandine is usually cooked with butter and seasonings, then sprinkled with whole or flaked, toasted almonds.",
    "amylolytic process": "Used in the brewing of alcohol from grains.",
    "anti-griddle": "A kitchen appliance that flash freezes or semi-freezes foods placed on its chilled metal top.",
    "aspic": "A savoury gelatin made from meat stock or consommé, and often shaped in a mold. Foods served in aspic are suspended in or on top of the gelatin.",
    "au gratin": "Prepared in the gratin style. Foods served au gratin are topped with breadcrumbs or cheese then browned under a broiler.",
    "au jus": "Foods served au jus, typically meat or sandwiches, are served with an unthickened sauce made from roast meat drippings, commonly in a separate side dish.",
    "au poivre": "Foods served au poivre, typically steak, are crusted with ground black pepper prior to cooking.",
    "backwoods cooking": "A method of cooking without the use of utensils that commonly takes place in remote areas, often in combination with wild or conventional camping.",
    "baghaar": "A cooking technique used in Pakistani cuisine and Indian cuisine in which cooking oil is heated and spices are added to fry. The oil is then added to a dish for flavoring.",
    "bain-marie": "A method of cooking where a container of food is placed in or above boiling water in order to heat gradually or to keep warm.",
    "baking": "The technique of prolonged cooking of food by dry heat acting by convection, normally in an oven, but can also be done in hot ashes or on hot stones. Appliances like Rotimatic also allow automatic baking.",
    "barbecuing": "Method of cooking meat, poultry and occasionally fish with the heat and hot smoke of a fire, smoking wood, or hot coals of charcoal.",
    "barding": "Wrapping meat in fat prior to roasting.",
    "basting": "Basting is a cooking technique that involves cooking meat with either its own juices or some type of preparation such as a sauce or marinade. The meat is left to cook, then periodically coated with the juice. Prominently used in grilling, rotisserie, roasting, and other meat preparations where the meat is over heat for extended periods of time, basting is used to keep meat moist during the cooking process and also to apply or enhance flavor. Improperly administered basting, however, may actually lead to the very problem it is designed to prevent: the undesired loss of moisture (drying out) of the meat.",
    "blanching": "A technique by which a fresh food such as a vegetable or fruit is briefly immersed in boiling water, removed after a timed interval, and then plunged into iced water or rinsed with cold running water (shocking or refreshing) to halt the cooking process.",
    "blending": "Using a machine called blender to grind ingredients.",
    "blind-baking": "Baking pastry before adding a filling.",
    "boiling": "The rapid vaporization of a liquid, which occurs when a liquid is heated to its boiling point, the temperature at which the vapor pressure of the liquid is equal to the pressure exerted on the liquid by the surrounding environmental pressure.",
    "braising": "Combination cooking method using both moist and dry heat; typically the food is first seared at a high temperature and then finished in a covered pot with a variable amount of liquid, resulting in a particular flavour.",
    "bricolage": "The preparation of a meal from whatever ingredients happen to be on hand.",
    "brine": "To soak a food item in salted water.",
    "brining": "Brining is a process similar to marination in which meat or poultry is soaked in brine before cooking",
    "broasting": "A method of cooking chicken and other foods using a pressure fryer and condiments.",
    "browning": "The process of partially cooking the surface of meat to help remove excessive fat and to give the meat a brown color crust and flavor through various browning reactions.",
    "candy making": "The preparation of candies and sugar confections by dissolving sugar in water or milk to form a syrup, which is boiled until it reaches the desired concentration or starts to caramelize.",
    "canning": "Involves the cooking of foods in sealed cans, among other processes.",
    "caramelization": "The browning of sugar, a process used extensively in cooking for the resulting nutty flavor and brown color.",
    "carryover cooking": "The phenomenon by which food retains heat and continues to cook even after being removed from the source of heat.",
    "casserole": "Food cooked and served in a casserole dish.",
    "ceviche": "Ceviche, also cebiche, seviche, or sebiche is a South American seafood dish that originated in Peru, typically made from fresh raw fish cured in fresh citrus juices, most commonly lemon or lime, but historically made with the juice of bitter orange. It is also spiced with ají, chili peppers or other seasonings and chopped onions, salt, and coriander are also added. The name originates from the Quechuan word siwichi, which means fresh or tender fish.",
    "charbroiler": "A cooking device consisting of a series of grates or ribs that can be heated using a variety of means, and is used in both residential and commercial applications for a variety of cooking operations.",
    "cheesemaking": "The craft of making cheese.",
    "chicken frying": "Battering and pan-frying a piece of beefsteak.",
    "chiffonade": "To cut leaves into long thin strips.",
    "chinese cooking techniques": "A set of methods and techniques traditionally used in Chinese cuisine. The cooking techniques can either be grouped into ones that use a single cooking method or a combination of wet and dry cooking methods.",
    "clay pot cooking": "A process of cooking food in a pot made from unglazed and natural clay.",
    "coddling": "Heating food in water kept just below the boiling point. Coddled egg may be prepared using this method.",
    "concasse": "To rough chop any ingredient, especially vegetables. The term is particularly applied to tomatoes, where tomato concasse is a tomato that has been peeled, seeded (seeds and skins removed), and chopped to specified dimensions.",
    "conche": 'A surface-scraping mixer and agitator that evenly distributes cocoa butter within chocolate, and may act as a "polisher" of the particles.',
    "confit": "A generic term for various kinds of food that have been cooked in grease, oil, or sugar water (syrup).",
    "consomme": "A type of clear soup made from richly flavored stock or bouillon that has been clarified.",
    "cooking with alcohol": "Many dishes incorporate alcoholic beverages into the food itself.",
    "cream": "The butterfat-heavy portion of whole milk that, due to its fat content, separates from the milk and rises to the top.",
    "creaming": "1.  Combining ingredients (typically butter and sugar) into a smooth paste.\n2.  Cooking meat or vegetables in a thick dairy-based sauce.\n3.  Mixing puréed corn kernels with whole corn kernels in the preparation of creamed corn.",
    "croquette": "A small roll made of finely chopped meat and/or vegetables that is breaded and fried.",
    "culinary triangle": "A concept described by anthropologist Claude Lévi-Strauss involving three types of cooking: boiling, roasting, and smoking, usually done to meat.",
    "curdling": "The breaking of an emulsion or colloid into large parts of different composition through the physico-chemical processes of flocculation, creaming, and coalescence. Curdling is intentional and desirable in making cheese and tofu, but may be unintentional and undesirable in making other foods such as sauces and custards.",
    "cured fish": "Fish preserved by fermentation, pickling, smoking, or some combination of these techniques.",
    "curing": "Any of a wide variety of food preservation and flavoring processes used for foods such as meat, fish, and vegetables, by the addition of a combination of salt, nitrates, nitrite, or sugar. Many curing processes also involve smoking, the process of flavoring, or cooking. The use of food dehydration was the earliest form of food curing.",
    "cutting": "Cutting is the separation or opening of a physical object, into two or more portions, through the application of an acutely directed force.",
    "deep frying": "A technique by which a food is completely submerged in hot fat or oil (as opposed to ordinary frying, which involves placing the food in a shallow pool of oil).",
    "deglazing": "Deglazing is a cooking technique for removing and dissolving browned food residue from a pan to flavor sauces, soups, and gravies.",
    "degreasing": "Degreasing, often called defatting or fat trimming, is the removal of fatty acids from an object. In culinary science, degreasing is done with the intention of reducing the fat content of a meal.",
    "dicing": "Cutting into cubes.",
    "double steaming": "Chinese cooking technique in which food is covered with water and put in a covered ceramic jar and the jar is then steamed for several hours.",
    "dough sheeting": "A technique used in industrial bakeries that involves rolling out dough into a (consistent) dough sheet with a desired even thickness prior to baking.",
    "dredging": "Coating the exterior of a food with a dry material (such as breadcrumbs) prior to cooking.",
    "dry roasting": "Dry roasting is a process by which heat is applied to dry foodstuffs without the use of oil or water as a carrier. Unlike other dry heat methods, dry roasting is used with foods such as nuts and seeds, in addition to some eaten insects such as house crickets.",
    "drying": "Any of a variety of processes by which a food is preserved by removing moisture, often by the use of a modern food dehydrator or by the traditional method of allowing sunlight and fresh air to evaporate moisture.",
    "dum pukht": "Also called slow oven cooking. A cooking technique associated with the Awadh region of India, in which meat and vegetables are cooked over a very low flame, generally in sealed containers.",
    "dutch oven cooking": "A Dutch oven is well suited for long, slow cooking, such as in making roasts, stews, and casseroles. Virtually any recipe that can be cooked in a conventional oven can be cooked in a Dutch oven. They are often used in outdoor cooking, such as when camping.",
    "earth oven": "A shallow pit in the ground used to trap heat and bake, smoke, or steam food.",
    "egg wash": "A preparation of beaten eggs, sometimes mixed with another liquid such as water or milk, which is brushed onto the surface of a pastry before baking.",
    "emulsify": "To combine two liquids that have a natural tendency to separate (such as oil and vinegar) into one homogeneous mass.",
    "en papillote": "A technique by which a food is put into a folded pouch or parcel and then baked.",
    "en vessie": "A cooking method by which a meat or other dish is cooked inside an animal bladder, often a pig bladder.",
    "engastration": "A cooking method by which the cook stuffs the remains of one animal into another animal.",
    "engine cooking": "Cooking food from the excess heat of an internal combustion engine, typically the engine of a car or a truck.",
    "escagraph": "Writing made out of food.",
    "fermentation": "In food processing, fermentation is the conversion of carbohydrates to alcohol or organic acids using microorganisms—yeasts or bacteria—under anaerobic (oxygen-free) conditions. Fermentation usually implies that the action of microorganisms is desired. ",
    "fillet": "To remove bones from meat or fish.",
    "flambe": "To pour alcohol over food and then ignite.",
    "flattop grill": "A flattop grill is a cooking appliance that resembles a griddle but performs differently because the heating element is circular rather than straight. This heating technology creates an extremely hot and even cooking surface, as heat spreads in a radial fashion over the surface.",
    "foam": 'A gelling or stabilizing agent in which air is suspended, creating a light, "fluffy" edible substance, e.g. whipped cream, meringue, and mousse.',
    "fondue": "Fondue is a Swiss melted cheese dish served in a communal pot over a portable stove heated with a candle or spirit lamp, and eaten by dipping bread into the cheese using long-stemmed forks.",
    "food preservation": "Food preservation includes food processing practices which prevent the growth of microorganisms, such as yeasts (although some methods work by introducing benign bacteria or fungi to the food), and slow the oxidation of fats that cause rancidity. Food preservation may also include processes that inhibit visual deterioration, such as the enzymatic browning reaction in apples after they are cut during food preparation.",
    "food steamer": "A food steamer or steam cooker is a small kitchen appliance used to cook or prepare various foods with steam heat by means of holding the food in a closed vessel reducing steam escape. This manner of cooking is called steaming.",
    "fricassee": "Fricassee or fricassée is a stew made with pieces of meat that have been browned in butter that are served in a sauce flavored with the cooking stock. Fricassee is usually made with chicken, veal or rabbit, with variations limited only by what ingredients the cook has at hand.",
    "fruit preserves": "Fruit preserves are preparations of fruits whose main preserving agent is sugar and sometimes acid, often stored in glass jars and used as a condiment or spread.",
    "frying": "Cooking food in oil or another fat, a technique that originated in ancient Egypt around 2500 BC.",
    "gentle frying": "Gentle frying or low-temperature frying is an oil- or fat-based cooking method used for relatively fragile or starchy foods. While gentle frying is most notably used to cook fried eggs, it is also used for delicate fish, tender cuts of meat, sausages, and as a first step in fried potatoes.",
    "glazing": "In cooking, a glaze is a glossy, translucent coating applied to the outer surface of a dish by dipping, dripping, or using a brush. A glaze may be either sweet or savory ; typical glazes include brushed egg whites, some types of icing, and jam, and may or may not include butter, sugar, milk, oil, and fruit or fruit juice.",
    "gratin": "Gratin is a culinary technique in which an ingredient is topped with a browned crust, often using breadcrumbs, grated cheese, egg or butter. Gratin is usually prepared in a shallow dish of some kind. A gratin is baked or cooked under an overhead grill or broiler to form a golden crust on top and is often served in its baking dish.",
    "grating ": " The use of a grater to mash vegetables.",
    "grilling": "Grilling is a form of cooking that involves dry heat applied to the surface of food, commonly from above, below or from the side. Grilling usually involves a significant amount of direct, radiant heat, and tends to be used for cooking meat and vegetables quickly. Food to be grilled is cooked on a grill (an open wire grid such as a gridiron with a heat source above or below), using a cast iron/frying pan, or a grill pan (similar to a frying pan, but with raised ridges to mimic the wires of an open grill).",
    "high-altitude cooking": "The process of cooking a food or beverage at altitudes well above sea level, where lower atmospheric pressure causes most foods to cook more slowly and may necessitate the use of special cooking techniques.",
    "hot salt frying": "Hot salt frying and hot sand frying are cooking techniques used by street-side food vendors in Bangladesh, Pakistan, China and India. Hot salt frying is an old cooking technique, and is used in villages throughout Asia and other parts of the world.",
    "huff paste": "Huff paste was a cooking technique involved making a stiff pie shell or coffyn using a mixture of flour, suet, and boiling water. The pastry when cooked created a tough protective layer around the food inside. When cooked, the pastry would be discarded as it was virtually inedible.",
    "indirect grilling": "Indirect grilling is a barbecue cooking technique in which the food is placed to the side of or above the heat source instead of directly over the flame as is more common. This can be achieved by igniting only some burners on a gas barbecue or by piling coals to one side of a charcoal pit. A drip tray is placed below the food to prevent fat from the food igniting and generating a direct flame. Indirect grilling is designed to cook larger or tougher foods that would burn if cooked using a direct flame. This method of cooking generates a more moderate temperature and allows for an easier introduction of wood smoke for flavoring.",
    "infusion": "The process of extracting chemical compounds or flavors from plant material in a solvent such as water, oil, or alcohol, by allowing the material to remain suspended in the solvent over time (a process often called steeping). A common example of an infusion is tea, and many herbal teas are prepared in the same way.",
    "jugging": "The process of stewing whole animals, mainly game or fish, for an extended period in a tightly covered container such as a casserole dish or an earthenware jug.",
    "juicing": "Juicing is the process of extracting juice from plant tissues such as fruit or vegetables.",
    "julienne": "A culinary knife cut which involves cutting food (typically vegetables) into long thin strips.",
    "julienning ": "Cutting into very thin pieces such as the thin carrots in store bought salad mix.",
    "kalua": "A traditional Hawaiian cooking method that utilizes an imu, a type of underground oven.",
    "karaage": "A Japanese cooking technique in which various foods — most often chicken, but also other meat and fish — are deep fried in oil, similar to the preparation of tempura.",
    "kho": "A cooking technique in Vietnamese cuisine in which a protein source such as fish, shrimp, poultry, pork, beef, or fried tofu is braised on low heat in a mixture of fish sauce, sugar, and water or a water substitute such as young coconut juice. It is similar to stew.",
    "kinpira": 'A Japanese cooking style that can be summarized as a technique of "sauté and simmer". It is commonly used to cook root vegetables and other foods.',
    "kneading": "In cooking (and more specifically baking), kneading is a process in the making of bread or dough, used to mix the ingredients and add strength to the final product. Its importance lies in the mixing of flour with water; when these two ingredients are combined and kneaded, the gliadin and glutenin proteins in the flour expand and form strands of gluten, which gives bread its texture. (To aid gluten production, many recipes use bread flour, which is higher in protein than all-purpose flour.) The kneading process warms and stretches these gluten strands, eventually creating a springy and elastic dough. If bread dough is not kneaded enough, it will not be able to hold the tiny pockets of gas (carbon dioxide) created by the leavening agent (such as yeast or baking powder), and will collapse, leaving a heavy and dense loaf.",
    "larding": "The act of threading strips of chilled pork fat through a roast.",
    "leaching": "Partially or incompletely boiling a food, especially as the first step in a longer cooking process. Parboiling involves cooking a food in boiling water only until it begins to soften, removing the food before it is fully cooked. The cooking is then often finished by a different method, such as braising or grilling.",
    "low-temperature cooking": "Low-temperature cooking is a cooking technique using temperatures in the range of about 45 to 82 °C for a prolonged time to cook food. Low-temperature cooking methods include sous vide cooking, slow cooking using a slow cooker, cooking in a normal oven which has a minimal setting of about 70 °C (158 °F)",
    "maceration": "Maceration is the process of preparing foods through the softening or breaking into pieces using a liquid.",
    "marinating": "Marinating is the process of soaking foods in a seasoned, often acidic, liquid before cooking. The origin of the word alludes to the use of brine (aqua marina or sea water) in the pickling process, which led to the technique of adding flavor by immersion in liquid. The liquid in question, the marinade, can be either acidic (made with ingredients such as vinegar, lemon juice, or wine) or enzymatic (made with ingredients such as pineapple, papaya, yogurt, or ginger), or have a neutral pH. In addition to these ingredients, a marinade often contains oils, herbs, and spices to further flavor the food items.",
    "marination": "The technique of soaking a food in a seasoned, often acidic, liquid (known as a marinade) prior to cooking. Marination is generally used as a means of adding or enhancing flavor or tenderizing tough cuts of meat, and the process can vary greatly in duration. It is similar to but distinct from brining and pickling.",
    "microwave oven": "Type of oven that heats foods quickly and efficiently using microwaves. However, unlike conventional ovens, a microwave oven does not brown bread or bake food. This makes microwave ovens unsuitable for cooking certain foods and unable to achieve certain culinary effects. Additional kinds of heat sources can be added into microwave ovens or microwave packaging so as to add these additional effects.",
    "milling": "tear food into small pieces.",
    "mincing ": "Cutting into very small pieces.",
    "mincing": "Mincing is a food preparation technique in which food ingredients are finely divided into uniform pieces. Minced food is in smaller pieces than diced or chopped foods, and is often prepared with a chef's knife or food processor, or in the case of meat by a specialised meat grinder.",
    "mixing": "Incorporating different ingredients to make something new; such as how mixing water, sugar, and lemon juice makes lemonade.",
    "mongolian barbecue": "Mongolian barbecue is a stir fried dish that was developed by Wu Zhaonan in Taiwan in 1951. Meat and vegetables are cooked on large, round, solid iron griddles at temperatures of up to 300 °C (572 °F).",
    "mother sauces": 'In French cuisine, the five "fundamental" sauces: béchamel, espagnole, velouté, hollandaise, and tomate, as defined by Auguste Escoffier.',
    "nappage": "Nappage or apricot glaze is a glazing technique used in pastry making. Jam made from apricots is diluted with water to form a transparent, slightly apricot-colored glaze.",
    "nixtamalization": "A process for the preparation of maize (corn) or other grain in which the grain is soaked and cooked in an alkaline solution, usually limewater, and then hulled.",
    "once-a-month cooking": "Preparing and cooking all the meals you need for an entire month in a single day.",
    "outdoor cooking": "Cooking in outdoor environments, which often demand specialized techniques and equipment for preparing food. Equipment used includes mess kits and portable stoves, among others.",
    "pan frying": "Characterized by the use of minimal cooking oil or fat (as opposed to shallow frying or deep frying), typically using just enough oil to lubricate the pan.",
    "parbaking": "Parbaking is a cooking technique in which a bread or dough product is partially baked and then rapidly frozen for storage. The raw dough is baked normally, but halted at about 80% of the normal cooking time, when it is rapidly cooled and frozen.",
    "parboiling": "Also called leaching. Partially or incompletely boiling a food, especially as the first step in a longer cooking process. Parboiling involves cooking a food in boiling water only until it begins to soften, removing the food before it is fully cooked. The cooking is then often finished by a different method, such as braising or grilling.",
    "paste": "A food paste is a semi-liquid colloidal suspension, emulsion, or aggregation used in food preparation or eaten directly as a spread. Pastes are often highly spicy or aromatic, are often prepared well in advance of actual usage, and are often made into a preserve for future use.",
    "peeling ": "To take the outer skin/covering off of a fruit or vegetable.",
    "pellicle": "A skin or coating of proteins on the surface of meat, fish, or poultry, which allows smoke to better adhere to the surface of the meat during the smoking process.",
    "pickling": "Pickling is the process of preserving or extending the shelf life of food by either anaerobic fermentation in brine or immersion in vinegar. The pickling procedure typically affects the food's texture and flavor. The resulting food is called a pickle, or, to prevent ambiguity, prefaced with pickled.",
    "pig roast": "A pig roast or hog roast is an event or gathering which involves the barbecuing of a whole pig.",
    "poaching": 'Poaching is a cooking technique that involves cooking by submerging food in a liquid, such as water, milk, stock or wine. Poaching is differentiated from the other "moist heat" cooking methods, such as simmering and boiling, in that it uses a relatively lower temperature. This temperature range makes it particularly suitable for delicate food, such as eggs, poultry, fish and fruit, which might easily fall apart or dry out using other cooking methods. Poaching is often considered a healthy method of cooking because it does not use fat to cook or flavor the food.',
    "pre-ferment": "A ferment is a fermentation starter used in indirect‍ methods of bread making. It may also be called mother dough.",
    "pressure cooking": "The process of cooking food, using water or other cooking liquid, in a sealed vessel known as a pressure cooker, which does not permit air or liquids to escape below a pre-set pressure.",
    "pressure frying": "In cooking, pressure frying is a variation on pressure cooking where meat and cooking oil are brought to high temperatures while pressure is held high enough to cook the food more quickly. This leaves the meat very hot and juicy. A receptacle used in pressure frying is known as a pressure fryer. The process is most notable for its use in the preparation of fried chicken in many commercial fried chicken restaurants.",
    "proofing": "In cooking, proofing is a step in the preparation of yeast bread and other baked goods where the dough is allowed to rest and rise a final time before baking. During this rest period, yeast ferments the dough and produces gases, thereby leavening the dough.",
    "purée": "A purée is cooked food, usually vegetables, fruits or legumes, that has been ground, pressed, blended or sieved to the consistency of a creamy paste or liquid. Purées of specific foods are often known by specific names, e.g., applesauce or hummus. The term is of French origin, where it meant in Old French purified or refined.",
    "reconstitution": "The process of assembling a palatable food product from processed sources (for example, adding water to concentrated juice or forming meat slurry into chicken nuggets).",
    "red cooking": "Also called Chinese stewing, red stewing, red braising, and flavour potting. A slow braising technique that imparts a red color to the prepared food, frequently used in Chinese cuisine.",
    "reduction": "In cooking, reduction is the process of thickening and intensifying the flavor of a liquid mixture such as a soup, sauce, wine, or juice by simmering or boiling.",
    "rendering": "Rendering is a process that converts waste animal tissue into stable, usable materials. Rendering can refer to any processing of animal products into more useful materials, or, more narrowly, to the rendering of whole animal fatty tissue into purified fats like lard or tallow. Rendering can be carried out on an industrial, farm, or kitchen scale. It can also be applied to non-animal products that are rendered down to pulp.",
    "ricing": 'Ricing is a cooking term meaning to pass food through a food mill or "ricer", which comes in several forms. In the most basic, food is pushed or pressured through a metal or plastic plate with many small holes, producing a smoother result than mashing, but coarser than pureeing or passing through a sieve or tamis. The size of the product produced by ricing is about the same as grains of rice.',
    "rillettes": "Rillettes is a preservation method similar to confit where meat is seasoned then slow cooked submerged in fat and cooked at an extremely slow rate for several hours. The meat is shredded and packed into sterile containers covered in fat. Rillettes are most commonly made with pork, but also made with other meats such as goose, duck, chicken, game birds, rabbit and sometimes with fish such as anchovies, tuna or salmon. Rillettes are best served at room temperature spread thickly on toasted bread.",
    "roasting": 'Roasting is a cooking method that uses dry heat where hot air covers the food, cooking it evenly on all sides with temperatures of at least 150 °C (300 °F) from an open flame, oven, or other heat source. Roasting can enhance the flavor through caramelization and Maillard browning on the surface of the food. Roasting uses indirect, diffused heat, and is suitable for slower cooking of meat in a larger, whole piece. Meats and most root and bulb vegetables can be roasted. Any piece of meat, especially red meat, that has been cooked in this fashion is called a roast. Meats and vegetables prepared in this way are described as "roasted", e.g., roasted chicken or roasted squash.',
    "robatayaki": "In Japanese cuisine, robatayaki , often shortened to robata, refers to a method of cooking, similar to barbecue in which items of food are cooked at varying speeds over hot charcoal. Many Japanese restaurants, both in Japan and abroad, specialize in this style of food preparation. Traditionally, the food consists of a combination of morsels of seafood and vegetables, but other kinds of food that are suitable for grilling may also be offered. The robata cooking style is different from other Japanese charcoal cooking in that it uses a wide, flat open fireplace in the style of an irori, rather than a shichirin or other type of charcoal cooking implement.",
    "rotisserie": "Rotisserie, also known as spit-roasting, is a style of roasting where meat is skewered on a spit – a long solid rod used to hold food while it is being cooked over a fire in a fireplace or over a campfire, or roasted in an oven. This method is generally used for cooking large joints of meat or entire animals, such as pigs or turkeys. The rotation cooks the meat evenly in its own juices and allows easy access for continuous basting.",
    "roux": "A paste-like thickening agent made of equal quantities of flour and fat cooked together to a sandy texture.",
    "saikyoyaki": "Saikyoyaki is a method of preparing fish in traditional Japanese cuisine by first marinating fish slices overnight in a white miso paste from Kyoto called saikyo shiro miso (西京白味噌). This dish is a speciality of Kyoto and the local white miso used for the marinade is sweeter than other varieties. Secondary ingredients of the marinade include sake and mirin.",
    "salting": "Salting is the preservation of food with dry edible salt. It is related to pickling in general and more specifically to brining also known as fermenting (preparing food with brine, that is, salty water) and is one form of curing. It is one of the oldest methods of preserving food, and two historically significant salt-cured foods are salted fish (usually dried and salted cod or salted herring) and salt-cured meat (such as bacon). Vegetables such as runner beans and cabbage are also often preserved in this manner.",
    "sautéing": "Sautéing or sauteing from French in reference to tossing while cooking is a method of cooking that uses a relatively small amount of oil or fat in a shallow pan over relatively high heat. Various sauté methods exist.",
    "searing": "A technique used in grilling, baking, braising, roasting, sautéing, etc., in which the surface of the food (usually meat, poultry, or fish) is cooked at high temperature until a crust forms from browning.",
    "seasoning": "Seasoning is the process of adding herbs, salts or spices to food to enhance the flavour.",
    "separating eggs": "Separating eggs is a process, generally used in cooking, in which the egg yolk is removed from the egg white. This allows one part of the egg to be used without the other part, or each part to be treated in different ways. Recipes for custard call for egg yolks, for example.",
    "shallow frying": "Shallow frying is a hot oil-based cooking technique. It is typically used to prepare portion-sized cuts of meat, fish, potatoes and patties such as fritters. Shallow frying can also be used to cook vegetables.",
    "shaving ": "scrape the outer skin of a vegetable or fruit",
    "shrivelling": "Shrivelling is a natural phenomenon where an object, with an attached sub-elastic covering, has its interior volume reduced in some way. The covering, which cannot contract any further, is then obliged to wrinkle and buckle, in order to preserve surface area while containing the lesser volume.",
    "shuck": "To remove the outer casing of a food item, such as an ear of corn or the shell of an oyster.",
    "simmering": "Simmering is a food preparation technique by which foods are cooked in hot liquids kept just below the boiling point of water and above poaching temperature. To create a steady simmer, a liquid is brought to a boil, then its heat source is reduced to a lower, constant temperature.",
    "slow cooker": "A slow cooker, also known as a crock-pot, is a countertop electrical cooking appliance used to simmer at a lower temperature than other cooking methods, such as baking, boiling, and frying. This facilitates unattended cooking for many hours of dishes that would otherwise be boiled: pot roast, soups, stews and other dishes.",
    "slow oven cooking": "A cooking technique associated with the Awadh region of India, in which meat and vegetables are cooked over a very low flame, generally in sealed containers.",
    "smoking": "Smoking is the process of flavoring, browning, cooking, or preserving food by exposing it to smoke from burning or smoldering material, most often wood. Meat, fish, and lapsang souchong tea are often smoked.",
    "smothering": "Smothering meat, seafood or vegetables is a cooking technique used in both Cajun and Creole cuisines of Louisiana. The technique involves cooking in a covered pan over low heat with a moderate amount of liquid, and can be regarded as a form of stove-top braising. The meat dishes cooked in this fashion are typically served over boiled or steamed white rice as a rice and gravy, while the vegetables are typically served as side dishes.",
    "souring": "Souring is a cooking technique that uses exposure to an acid to cause a physical and chemical change in food. This acid can be added explicitly, or can be produced within the food itself by a microbe such as Lactobacillus.",
    "sous vide": "Sous vide, also known as low temperature long time (LTLT) cooking, is a method of cooking in which food is placed in a plastic pouch or a glass jar and cooked in a water bath for longer than usual cooking times at a precisely regulated temperature.",
    "spatchcock": "Poultry or game that has been prepared for roasting or grilling by removing the backbone (and sometimes the sternum) and flattening it out before cooking.",
    "spherification": "Spherification is a culinary process that employs sodium alginate and either calcium chloride or calcium glucate lactate to shape a liquid into squishy spheres, which visually and texturally resemble roe. The technique was documented by Unilever in the 1950s and brought to the modernist cuisine by the creative team at El Bulli under the direction of chefs Ferran Adrià and Albert Adrià.",
    "sprouting": "Sprouting is the natural process by which seeds or spores germinate and put out shoots, and already established plants produce new leaves or buds or other newly developing parts experience further growth.In the field of nutrition, the term signifies the practice of germinating seeds (for example, mung beans or sunflower seeds) to be eaten raw or cooked, which is considered highly nutritious.",
    "steaming": "Steaming is a method of cooking using steam. This is often done with a food steamer, a kitchen appliance made specifically to cook food with steam, but food can also be steamed in a wok. In the American southwest, steam pits used for cooking have been found dating back about 5,000 years. Steaming is considered a healthy cooking technique that can be used for many kinds of foods.",
    "steeping": "Steeping is the soaking in liquid of a solid, usually so as to extract flavours or to soften it. The specific process of teas being prepared for drinking by leaving the leaves in heated water to release the flavour and nutrients is known as steeping. Herbal teas may be prepared by decoction, infusion, or maceration. Some solids are soaked to remove an ingredient, such as salt, where the solute is not the desired product.",
    "stewing": "A stew is a combination of solid food ingredients that have been cooked in liquid and served in the resultant gravy. Ingredients in a stew can include any combination of vegetables and may include meat, especially tougher meats suitable for slow-cooking, such as beef, pork, lamb, poultry, sausages, and seafood. While water can be used as the stew-cooking liquid, stock is also common. A small amount of red wine is sometimes added for flavour. Seasoning and flavourings may also be added. Stews are typically cooked at a relatively low temperature, allowing flavours to mingle.",
    "stir frying": "Stir frying is a Chinese cooking technique in which ingredients are fried in a small amount of very hot oil while being stirred or tossed in a wok. The technique originated in China and in recent centuries has spread into other parts of Asia and the West. It is similar to sautéing in Western cooking technique.",
    "straight dough": "Straight dough is a single-mix process of making bread. The dough is made from all fresh ingredients, and they are all placed together and combined in one kneading or mixing session. After mixing, a bulk fermentation rest of about 1 hour or longer occurs before division. It is also called the direct dough method.",
    "stuffing": "An edible food mixture, often a starch, used to fill a cavity in another food item.",
    "sugar panning": 'Sugar panning, or simply panning, is a method for adding a candy "shell" to candy or nuts. Popular candies that employ this process in their manufacture include dragées, M&M\'s, gobstoppers, konpeitō and jelly beans. Jelly beans use soft panning while the other three are examples of hard panning. The process was initially invented in 17th century France to make jordan almonds.',
    "sugaring": "Sugaring is a food preservation method similar to pickling. Sugaring is the process of desiccating a food by first dehydrating it, then packing it with pure sugar. This sugar can be crystalline in the form of table or raw sugar, or it can be a high sugar density liquid such as honey, syrup or molasses.",
    "supreme": "The term supreme used in cooking and culinary arts refers to the best part of the food. For poultry, game and fish dishes, supreme denotes a fillet.",
    "sweating": "The gentle heating of vegetables in a little oil or butter, which usually results in tender, sometimes translucent, pieces.",
    "swissing": "Swiss steak is a dish of meat, usually beef, that is swissed by rolling or pounding before being braised in a cooking pot of stewed vegetables and seasonings. It is often served with gravy. It is made either on a stove or in an oven, and does not get its name from Switzerland, as the name",
    "syringe": "For injecting fillings in foods.",
    "tandoor": "A cylindrical clay or metal oven used in cooking and baking in Southern, Central, and Western Asia, as well as in the Caucasus.",
    "tataki": 'Two methods of preparing fish or meat in Japanese cuisine are called tataki or tosa-mi. In Japanese, tataki (たたき) means "pounded" or "hit into pieces".',
    "tempering": "1.  Tempering (chocolate), a method of increasing the shine and durability of chocolate couverture.\n2.  Tempering (cooking), bringing meat to room temperature before cooking; or bringing food up to temperature slowly as in sous vide.\n3.  Tempering (spices), a cooking technique and garnish used in the cuisines of India, Bangladesh, and Pakistan, in which whole spices (and sometimes also other ingredients such as minced ginger root or sugar) are fried briefly in oil or ghee to liberate essential oils from cells and thus enhance their flavours, before being poured, together with the oil, into a dish.",
    "tenderizing": "A process to break down collagens in meat to make it more palatable for consumption.",
    "teriyaki": "Teriyaki is a cooking technique used in Japanese cuisine in which foods are broiled or grilled with a glaze of soy sauce, mirin, and sugar.",
    "thermal cooking": "Uses the concept of the haybox whereby placing hay or straw around a cooking pot of heated food the meal continues to cook without fuel.",
    "thermal immersion circulator": "A thermal immersion circulator is an electrically powered device that circulates and heats a warm fluid kept at an accurate and stable temperature. It is used in process, environmental, microbiological, hazardous waste, and other laboratories. Since 2005 they have also been used for sous-vide food cooking, a method that uses airtight plastic bags in a water bath at accurately regulated temperatures much lower than usually used for cooking.",
    "thermization": "A method of sterilizing raw milk with heat.",
    "thickening": "A thickening agent or thickener is a substance which can increase the viscosity of a liquid without substantially changing its other properties. Edible thickeners are commonly used to thicken sauces, soups, and puddings without altering their taste; thickeners are also used in paints, inks, explosives, and cosmetics.",
    "transglutaminase": "A protein binder, called meat glue.",
    "truss": "To tie the legs and wings of poultry in a way that promotes even cooking.",
    "turkey fryer": "A turkey fryer is an apparatus for deep-frying a turkey. Fried turkey has been a popular item in the Southern United States, and has recently become popular in other parts of the country because of the reduced time needed to cook a turkey in a deep fryer, versus other conventional methods such as an oven or a rotisserie grill.",
    "vacuum flask cooking": "A thermal cooker, or a vacuum flask cooker, is a cooking device that uses thermal insulation to retain heat and cook food without the continuous use of fuel or other heat source. It is a modern implementation of a haybox, which uses hay or straw to insulate a cooking pot.",
    "velveting": "A technique which involves coating pieces of raw meat or poultry in a mixture of cornstarch and liquid prior to cooking, frequently used in Chinese cuisine.",
    "vietnamese cooking techniques": "Many common culinary terms exist that are unique to Vietnam.",
    "wok cooking": "The wok is used in a significant amount of cooking methods.",
    "zest": "The colourful outer layer of citrus fruits, often scraped off and used as a flavouring ingredient.",
}


class ActionExplainCookTechniqie(Action):
    def name(self) -> Text:
        return "action_what_is_cook_technique"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("Cook technique is the way you want to cook your food")
        dispatcher.utter_message(
            "Cooking is the art of preparing food for ingestion, commonly with the application of heat. Cooking techniques and ingredients vary widely across the world, reflecting unique environments, economics, cultural traditions, and trends. The way that cooking takes place also depends on the skill and type of training of an individual cook"
        )

        dispatcher.utter_message("Here are list you can use for Cook technique")

        message = "".join(f"{key}\n" for key in tech_descriptions)

        dispatcher.utter_message(message)

        return []


class ActionSearchFoodRecipe(Action):
    def name(self) -> Text:
        return "action_explain_cook_technique"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        message_tracker = MessageTracker(**tracker.latest_message)
        correct_technique = False
        for entity in message_tracker.entities:
            if entity.type == "cook_technique":
                dispatcher.utter_message(text=tech_descriptions[entity.value.lower()])
                correct_technique = True
        if not correct_technique:
            dispatcher.utter_message(
                text="Could you repeat what you're trying to know ?"
            )
        return []
