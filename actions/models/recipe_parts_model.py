from typing import List, Optional
from actions.models.message_tracker_model import Entity
from pydantic import BaseModel

# part == Entity


class RecipePartsModel(BaseModel):
    parts: List[Entity] = []

    def add_part(self, entity: Entity):
        if(entity.extractor == "RegexEntityExtractor"):
            self.parts.append()

    def checkShouldClear(self, newParts: List[Entity]):
        has_ingredient_in_old = any(
            item.type == "ingredient" for item in self.parts
        )
        has_technique_in_old = any(
            item.type == "cook_technique" for item in self.parts
        )
        has_ingredient_in_new = any(
            item.type == "ingredient" for item in newParts)
        has_technique_in_new = any(
            item.type == "cook_technique" for item in newParts
        )

        if (
            has_ingredient_in_new
            and has_ingredient_in_old
            or has_technique_in_new
            and has_technique_in_old
        ):
            self.parts = []

    def append_list(self, entities: List[Entity]):
        entitiesFiltered = filter(self._isRegExtractor, entities)
        self.parts += entitiesFiltered
        input_len = entities[-1].end
        for item in self.parts:
            item.start -= input_len
            item.end -= input_len

    def refactor(self):
        self._sort()
        self._redundantOperator()

    def createSearchKeywords(self) -> list:
        # ? type or and
        # ? same x2  +
        # ? diff X   +
        search_list = []
        branch_list = []
        index = 0
        while index < len(self.parts):
            bl_len = len(branch_list)
            if self.parts[index].type == "or":
                if (
                    self.parts[index - 1].type
                    == self.parts[index + 1].type
                ):
                    for _ in range(bl_len):
                        raw_item = branch_list[0]
                        del raw_item[-1]
                        branch_list.append(raw_item + [self.parts[index - 1]])
                        branch_list.append(raw_item + [self.parts[index + 1]])
                        del branch_list[0]
                    index += 1
            elif bl_len == 0:
                branch_list.append([self.parts[index]])
            else:
                for item in branch_list:
                    item.append(self.parts[index])
            index += 1

        for item in branch_list:
            search_list.append(item[0].value)
            for i in range(1, len(item)):
                search_list[-1] += " " + item[i].value
        
        return search_list

    def _isRegExtractor(self, entity: Entity) -> bool:
        return entity.extractor == "RegexEntityExtractor"

    def _sort(self):
        def compareTo(e):
            return e.start
        self.parts.sort(key=compareTo)

    def _redundantOperator(self):
        for index, val in enumerate(self.parts):
            if (val.type == "or" and (
                index == 0
                or index == len(self.parts) - 1
                or self.parts[index + 1].type == "or"
            )):
                del self.parts[index]
