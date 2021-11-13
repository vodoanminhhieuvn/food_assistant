
NUTRIENT_LIST = ["calory", "fat"]

class Constants:
  @staticmethod
  def containNutrient(nutrient: str) -> bool:
    return nutrient in NUTRIENT_LIST