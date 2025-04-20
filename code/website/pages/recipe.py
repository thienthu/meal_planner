import streamlit as st
import requests
import re
import math
from fractions import Fraction

def decimal2fraction(num):
    fract_string = ''
    whole_string = ''
    frac, whole = math.modf(num)
    if frac:
        fract_string = str(Fraction(frac)) 
    if whole:
        whole_string = str(int(whole)) + ' '
    return whole_string + fract_string



st.set_page_config(page_title="ShowRecipe", layout="wide")

main_theme = """
<style>
    .stApp {
    background-color:#FFF7F1;
    }
</style>
"""

conn = st.connection(
    "localhost", type="sql", url="mysql://root:Verrygood_123!?@localhost:8889/recipedb"
)

if st.session_state.get('chosen_recipe_link') and st.session_state['chosen_recipe_link']:
    val = st.session_state['chosen_recipe_link']
    recipe_df = conn.query(
        f'''select a1.img_link, a1.name, a1.area, a1.instruction, a1.tags, a1.rating, a1.total_user_rated, a1.source_link, a1.time_cooking, a1.youtube_link, round(a2.meal_calories,0) as calories
                           from recipe a1 
                           left join recipe_search a2 on a1.id=a2.recipe_id
                           where id = :id''', params={"id":val}
    )
    measure_df = conn.query(
        f'''select map_ingredient_id, map_ingredient_name, measure_quantity, measure_unit
                           from measure 
                           where recipe_id = :id''', params={"id":val}
    )
    
    st.markdown('<h1 style="color:#A52A2A;font-size:40px;text-align: center;">{} </h1> <p>'.format(recipe_df["name"].str.title().values[0]),
                    unsafe_allow_html=True)
    with st.container(border=True):
        c11, c12 = st.columns([1, 2], gap="small")

        with c11:
            st.image(recipe_df['img_link'].values[0], use_column_width = "always" )
            st.markdown("**Source:** 🔗:  \n {}".format(recipe_df.iloc[0]['source_link']))
        with c12:
            with st.container(border=True):
                st.markdown('<h3 style="color:#A52A2A;font-size:28px;text-align: center;">🔥Instruction🔥</h3>',
                            unsafe_allow_html=True)
                instructions = ':bento: ' + recipe_df['instruction'].values[0].replace(r'\r\n\r\n',r'\r\n')
                instructions = re.sub(r'(\n *)([a-zA-Z]+)',r'  \n:bento: \2', instructions)
                st.markdown('''{}.'''.format(instructions))

    c21, c22, c23 = st.columns([1, 2, 2], gap="small")
    with c21:
            st.markdown("#### Information \n **Calories** : {}  \n **Cooking time** ⏰: {}  \n **Country** 🌎: {}  \n  **Tags** 🍝: {} \
                         \n  **Rating:** {}".
                        format(recipe_df.iloc[0]['calories'], recipe_df.iloc[0]['time_cooking'], recipe_df['area'].fillna('').values[0], recipe_df['tags'].fillna('').values[0], 
                              "⭐" * int(recipe_df['rating'].fillna(0).values[0])))
    with c22:
        serving_num = st.number_input(label="Serving", min_value=1,value="min")
        measure_df['measure_quantity'] = measure_df['measure_quantity'] * serving_num
        measure_df['quant_unit'] = measure_df['measure_quantity'].fillna(1).apply(lambda x: decimal2fraction(x)).astype(str) + ' ' + measure_df['measure_unit'].fillna('')
        st.data_editor(
            measure_df,
            column_config={
                "quant_unit": st.column_config.Column("Quantity", disabled=True),
                "map_ingredient_name": st.column_config.Column("Ingredient", disabled=True),
            },
            column_order=["quant_unit", "map_ingredient_name"],
            hide_index=True,
            use_container_width=True,
        )

    with c23:
        with st.container(border=True):
            ingredient_options = measure_df['map_ingredient_name'].to_list()
            selected_ingredient = st.selectbox('Check nutrient fact.',
                                            ingredient_options)
            selected_ingredient_id = measure_df[measure_df['map_ingredient_name']==selected_ingredient]['map_ingredient_id'].values[0]
            ingredient_df = conn.query(
                f'''select id, name, serving_unit, serving_size, amount_g, calories, 
                    total_fat_g, cholesterol_mg, sodium_mg, carbonhydrate_g, protein_g, calcium_mg, iron_mg, 
                    potassium_mg, vitamin_d_mcg, caffeine_mg, img_link
                                from ingredient 
                                where id = :id''', params={"id":selected_ingredient_id}
            )

            sub1, sub2 = st.columns([1,1], gap="small")
            with sub1:
                st.markdown("### Nutritient Fact\n **Serving:** {} {}  \n **Calories:** {}". format(ingredient_df.iloc[0]['serving_size'], ingredient_df.iloc[0]['serving_unit'], ingredient_df.iloc[0]['calories']))

            with sub2:
                st.image(ingredient_df['img_link'].values[0], use_column_width = "always")

            st.markdown("\n - **Total Fat:** {} g  \n - **Cholesterol:** {} mg \n - **Sodium:** {} mg \n - **Total Carbohydrates:** {} g \
                        \n - **Protein** {} g \n - **Caffeine:** {} mg".
                        format(ingredient_df.iloc[0]['total_fat_g'],ingredient_df.iloc[0]['cholesterol_mg'],ingredient_df.iloc[0]['sodium_mg'],
                               ingredient_df.iloc[0]['carbonhydrate_g'],ingredient_df.iloc[0]['protein_g'],ingredient_df.iloc[0]['caffeine_mg']))

          
    video_link = recipe_df['youtube_link'].values[0]    
    if video_link:
        request = requests.get(recipe_df['youtube_link'].values[0], allow_redirects=False)
        if request.status_code != 200:
            st.write(":orange[Video link]")
            st.text('\n\n')
            st.video("{}".format("video_link"))
    

else:
    st.write('Non')