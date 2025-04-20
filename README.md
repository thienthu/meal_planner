# 🍽️ Meal Planner

## 📌 Overview

**Meal Planner** is an end-to-end data engineering and web application project designed to help users find delicious recipes that align with their **dietary preferences** and **nutritional goals**. With so many recipe options available online, finding meals that match specific needs can be overwhelming—this project aims to simplify that process.

By building a full **ETL pipeline** and a **Streamlit-based web app**, this project enables users to seamlessly discover meals that fit their personal criteria, including calorie limits, preferred ingredients, and allergies.

## ⚙️ Features

- 🔎 Search for recipes based on dietary preferences  
- 📊 Filter by calorie, ingredient type, and allergen info  
- 🍲 View detailed recipe instructions, ingredients, and nutrition info  
- 💾 Store and query recipes through a structured relational database  
- 🌐 Clean, interactive web interface using Streamlit

## 🔄 Data Pipeline (ETL Process)

The project follows a complete ETL pipeline with the following steps:

1. **Extract (Web Scraping)**  
   - Data is collected using **Selenium** from:
     - [Nutritionix](https://www.nutritionix.com/) – nutritional details for ingredients
     - [Food.com](https://www.food.com/) – recipe source
     - [TheMealDB](https://www.themealdb.com/) – additional recipe data

2. **Transform**  
   - Raw JSON data is cleaned and normalized
   - Ingredients are matched with their nutrition info
   - Measurement units are standardized

3. **Load**  
   - Data is stored in a **Relational Database (RDBMS)** with the following schema:
![EDT_P3](https://github.com/user-attachments/assets/025f0f05-b72c-44cd-9948-ee7d987cf74f)


- `Recipe` table: stores recipe metadata (title, category, instructions, etc.)
- `Ingredient` table: stores nutritional information (calories, protein, fat, etc.)
- `Measure` table: maps quantity of each ingredient per recipe

## 🌍 Web Application (Frontend)

The web app is built using **Streamlit**, offering a user-friendly interface with the following workflow:

1. **User Input**  
- Max calorie intake  
- Favorite ingredients  
- Ingredients to avoid (allergies)

2. **Recipe Recommendations**  
- A filtered list of matching recipes is displayed

3. **Detailed View**  
- Upon selecting a recipe, users can view:
  - Cooking instructions
  - Ingredient list with exact measures
  - Nutrition facts per recipe


## 🧪 Tech Stack

- **Selenium** – for web scraping  
- **Pandas / NumPy** – for data transformation  
- **SQLite / PostgreSQL** – for relational data storage  
- **SQLAlchemy** – for ORM and database access  
- **Streamlit** – for frontend web interface

## 🚀 Run Web
```
streamlit run website/home.py
```
![TheMealPlanner-GoogleChrome2025-04-2023-38-56-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/a6930d0c-9145-4ec9-ab67-cf9b04502df7)

## 🧪 Author
- **Author**: Thu Nguyen.
- **Disclaimer**: This project was developed as part of the Database course at Ghent University.
