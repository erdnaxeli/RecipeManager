from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


class Unit(Enum):
    Kg = auto()
    g = auto()
    L = auto()
    mL = auto()  # noqa: N815
    TeaSpoon = auto()
    TableSpoon = auto()


@dataclass
class Ingredient:
    name: str
    quantity: float
    unit: Optional[Unit] = None


@dataclass
class Step:
    text: str


@dataclass
class Recipe:
    name: str
    id: int
    ingredients: list[Ingredient]
    steps: list[Step]


@dataclass
class RecipeCreation:
    name: str


RECIPES: list[Recipe] = [
    Recipe(
        id=1,
        name="Ratatouille",
        ingredients=[
            Ingredient(name="huile d'olive", quantity=4, unit=Unit.TableSpoon),
            Ingredient(name="aubergine", quantity=1),
            Ingredient(name="courgette", quantity=1),
            Ingredient(name="poivron", quantity=1),
            Ingredient(name="oignons", quantity=2),
            Ingredient(name="olives", quantity=10),
            Ingredient(name="pulpe de tomates", quantity=400, unit=Unit.mL),
            Ingredient(name="bouquet garni", quantity=1),
            Ingredient(name="herbes de provences", quantity=1, unit=Unit.TeaSpoon),
        ],
        steps=[
            Step(
                text=(
                    "Émincer grossièrement les oignons. "
                    "Les faire revenir dans l'huile chaude."
                )
            ),
            Step(text="Hacher (ou presser) l'ail et l'ajouter avec les oignons."),
            Step(
                text=(
                    "Couper en cubes et ajouter dans la marmite les légumes dans "
                    "l'ordre suivant : aubergines, courgette puis poivrons."
                )
            ),
            Step(
                text=(
                    "Ajouter le bouquet garni et les hebres de provences puis "
                    "laisser revenir à feux moyen doux pendant 30 minutes."
                )
            ),
            Step(
                text=(
                    "Ajouter la pulpe de tomate puis laisser cuire encore 30 "
                    "minutes sur feux doux."
                )
            ),
            Step(text="Retirez le bouquet garne et servez :)"),
        ],
    )
]


class Cookbook:
    def create_recipe(self, recipe: RecipeCreation) -> int:
        recipe_id = RECIPES[-1].id + 1
        RECIPES.append(
            Recipe(
                id=recipe_id,
                name=recipe.name,
            )
        )

        return recipe_id

    def get_recipe(self, recipe_id: int) -> Optional[Recipe]:
        try:
            return next(r for r in RECIPES if r.id == recipe_id)
        except StopIteration:
            return None

    def get_recipes(self) -> list[Recipe]:
        return RECIPES

    def get_ingredients(self) -> list[Ingredient]:
        return [i for r in RECIPES for i in r.ingredients]
