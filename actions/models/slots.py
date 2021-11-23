from actions.models.nutrient_model import NutrientModel


class Slot:
    nutrient_slots = NutrientModel()

    def set_nutrient_attr(self, name: str, value: int):
        self.nutrient_slots.__setattr__(name, value)


slot = Slot()
