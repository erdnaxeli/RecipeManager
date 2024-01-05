from typing import Annotated

from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse
from fastui import AnyComponent, FastUI, components as c, prebuilt_html
from fastui.events import GoToEvent
from fastui.forms import fastui_form
from pydantic import BaseModel

from recipes.cookbook import Cookbook, RecipeCreation, Unit


app = FastAPI(title="recipes")
cookbook = Cookbook()


class IngredientForm(BaseModel):
    name: str
    quantity: float
    unit: str


class StepForm(BaseModel):
    text: str


class RecipeForm(BaseModel):
    name: str
    # ingredients: list[IngredientForm]
    # steps: list[StepForm]


def default_page(components: list[AnyComponent]) -> list[AnyComponent]:
    return [
        c.PageTitle(text="Recipes manager"),
        c.Navbar(
            title="Recipes manager",
            title_event=GoToEvent(url="/"),
            links=[
                c.Link(
                    components=[c.Text(text="Ajouter une recette")],
                    on_click=GoToEvent(url="/recipes/add"),
                )
            ],
        ),
        c.Page(components=components),
    ]


@app.get("/api/", response_model=FastUI, response_model_exclude_none=True)
def index() -> list[AnyComponent]:
    return default_page(
        components=[
            c.Heading(text="Recipes manager"),
            c.LinkList(
                links=[
                    c.Link(
                        components=[c.Text(text=recipe.name)],
                        on_click=GoToEvent(url=f"/recipes/{recipe.id}"),
                    )
                    for recipe in cookbook.get_recipes()
                ]
            ),
        ]
    )


@app.get(
    "/api/recipes/{recipe_id:int}",
    response_model=FastUI,
    response_model_exclude_none=True,
)
def get_recipe(recipe_id: int) -> list[AnyComponent]:
    recipe = cookbook.get_recipe(recipe_id)
    if recipe is None:
        raise HTTPException(status_code=404)

    return default_page(
        components=[
            c.Heading(text=recipe.name),
            c.Div(
                components=[
                    c.Heading(text="Ingrédients", level=2),
                    c.Markdown(
                        text="\n".join(
                            f"* {ingredient.name}: "
                            f"{ingredient.quantity} {unit_to_str(ingredient.unit)}"
                            for ingredient in recipe.ingredients
                        )
                    ),
                ]
            ),
            c.Div(
                components=[
                    c.Heading(text="Étapes", level=2),
                    c.Markdown(
                        text="\n".join(f"1. {step.text}" for step in recipe.steps)
                    ),
                ]
            ),
        ]
    )


@app.get("/api/recipes/add", response_model=FastUI, response_model_exclude_none=True)
def recipe_add_form() -> list[AnyComponent]:
    return default_page(
        components=[
            c.Heading(text="Ajouter une recette"),
            c.ModelForm(
                model=RecipeForm,
                submit_url="/api/recipes/add",
            ),
        ]
    )


@app.post("/api/recipes/add")
def recipe_add(form: Annotated[RecipeForm, fastui_form(RecipeForm)]):
    cookbook.create_recipe(RecipeCreation(name=form.name))


@app.get("/{path:path}")
def front_app() -> HTMLResponse:
    return HTMLResponse(prebuilt_html(title="Recipes"))


def unit_to_str(unit: Unit) -> str:
    match unit:
        case Unit.Kg:
            return "Kg"
        case Unit.g:
            return "g"
        case Unit.L:
            return "L"
        case Unit.mL:
            return "mL"
        case Unit.TableSpoon:
            return "cuillère à soupe"
        case Unit.TeaSpoon:
            return "cuillère à café"

    return ""
