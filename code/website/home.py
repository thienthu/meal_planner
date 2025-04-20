import streamlit as st
from st_aggrid import AgGrid, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import ColumnsAutoSizeMode

st.set_page_config(page_title="TheMealPlanner", layout="wide")

main_theme = """
<style>
    .stApp {
    background-color:#FFF7F1;
    }
</style>
"""
st.markdown(main_theme, unsafe_allow_html=True)
st.markdown(
    '<h1 style="color:#A52A2A;font-size:40px;text-align: center;">&#129368Welcome to TheMealPlanner&#129368</h1>',
    unsafe_allow_html=True,
)

# connect to sql
conn = st.connection(
    "localhost", type="sql", url="mysql://root:Verrygood_123!?@localhost:8889/recipedb"
)
area_df = conn.query(
    "select name from area where name != :exclude_name",
    params={"exclude_name": "unknown"},
)
countries = area_df["name"].str.title().tolist()

category_df = conn.query("select name from category")
categories = category_df["name"].str.capitalize().tolist()


def search_recipe(
    max_calor=None,
    favorite_ing=None,
    allergic_ing=None,
    chosen_categories=[],
    chosen_countries=[]
):
    if chosen_countries:
        countries_str = ""
        for country in chosen_countries:
            countries_str = countries_str + '"' + country.lower() + '"' + ","
        countries_str = countries_str[:-1]
        is_null = '""'

    else:
        countries_str = '""'
        is_null = "Null"

    if not(max_calor):
        max_calor = 'Null'
    
    if chosen_categories:
        categories_str = ""
        for cat in chosen_categories:
            categories_str = categories_str + '"' + cat + '"' + ","
        categories_str = categories_str[:-1]
        cat_is_null = '""'

    else:
        categories_str = '""'
        cat_is_null = "Null"
    
    recipe_df = conn.query(
        f"""select img_link, name, area, rating, recipe_id as id, ingredients
                           from recipe_search 
                           where ({is_null} is null or area in ({countries_str}))
                           and ({cat_is_null} is null or category in ({categories_str}))
                           and ({max_calor} is null or meal_calories < {max_calor})
                           order by rating desc""",
        ttl=360,
    )
    if favorite_ing:
        favorite_ing = favorite_ing.split(',')
        recipe_df = recipe_df[recipe_df['ingredients'].str.contains('|'.join(favorite_ing))]

    if allergic_ing:
        allergic_ing = allergic_ing.split(',')
        recipe_df = recipe_df[~(recipe_df['ingredients'].str.contains('|'.join(allergic_ing)))]

    recipe_df["rating"] = recipe_df["rating"].fillna("0").astype("int")
    recipe_df["rating_star"] = recipe_df["rating"].apply(lambda x: x * "⭐")
    recipe_df["area"] = recipe_df["area"].fillna("unknown").str.title()
    recipe_df["name"] = recipe_df["name"].str.title()
    return recipe_df


with st.container(border=True):
    c1, c2 = st.columns([1, 3], gap="small")
    with c1:
        with st.form("my_form", clear_on_submit=True):
            max_calor = st.number_input("**Maximum calories per person**", value=None)
            favorite_ing = st.text_input(
                "**What is your favorite ingredients**",
                placeholder="Type str1, str2,..",
            )
            allergic_ing = st.text_input(
                "**Are you alergic to any ingredient**",
                placeholder="Type str1, str2,..",
            )
            
            chosen_categories = st.multiselect("**Select category.**", categories)

            chosen_countries = st.multiselect(
                "**Which country's cuisine would you like to try**", countries
            )
            # Every form must have a submit button.
            st.write("\n")

            submitted = st.form_submit_button("Search")

            if submitted:
                st.session_state["show_data"] = True

    with c2:
        if st.session_state.get("show_data") and st.session_state["show_data"] == True:
            df = search_recipe(
                max_calor, favorite_ing, allergic_ing, chosen_categories, chosen_countries
            )
            df.insert(0, "select", False)
            if len(df) >= 15:
                height = 600
            elif len(df):
                height = int(570 / 16 * len(df) + 30)
            else:
                height = None
            editted_df = st.data_editor(
                df,
                column_config={
                    "img_link": st.column_config.ImageColumn(
                        label="Image",
                        help="Streamlit app preview screenshots",
                        width="small",
                    ),
                    "name": st.column_config.Column(
                        "Recipe Name", width="large", disabled=True
                    ),
                    "rating_star": st.column_config.Column("Rating", disabled=True),
                    "area": st.column_config.Column("Country", disabled=True),
                    "select": st.column_config.CheckboxColumn(
                        width="small", help="Link to the recipe information page"
                    ),
                },
                column_order=["select", "img_link", "name", "area", "rating_star"],
                hide_index=True,
                height=height,
                use_container_width=True,
            )
            link_val = editted_df[editted_df["select"]]["id"].values
            if link_val.any():
                st.session_state["chosen_recipe_link"] = link_val[-1]
                st.switch_page("pages/recipe.py")

css = """
<style>
    [data-testid="stForm"] {
        background: #D2B48C;
    }
</style>
"""

st.write(css, unsafe_allow_html=True)
