# Prompt Engineering for Data Analysis 
Hackathon, 23 October 2024

## Introduction

Prompt engineering is crucial for leveraging LLMs in data analysis.
In this hackathon, we will explore how to optimize prompts for LLMs to perform data analysis tasks.

## Task

Given the dataset `world-data-2023.csv`, your task is to use the code in this repository, along with your own prompts, to answer questions.
You may use any LLM of your choice. The default is `gpt-4o`.
You may also use any other tools or libraries you like.

Following are example questions you may ask using the dataset:
1. What is the average population density per square kilometer across all countries?
2. Which country has the lowest infant mortality rate and what is it?
3. Can we predict co2 emissions based on density, agricultural land, and forest area?
4. Is there a correlation between birth rate and infant mortality rate among these countries?
5. Can we group countries based on their economic indicators such as GDP, tax revenue percentage, and total tax rate?

You are free to ask any other questions you like.

You may use any prompting techniques, including but not limited to few-shot, self-reflection, chain-of-thought, and rule-based prompting.

## How to use this repository

1. Clone this repository.
2. Install the required libraries using `pip install -r requirements.txt`.

### Repository Structure

The repository contains the following files:

#### `README.md`
This is the file you are currently reading.

#### `requirements.txt`
This file contains the list of required libraries. You can install them using the following command:
```bash
pip install -r requirements.txt
```

#### `world-data-2023.csv`
This is the dataset you will use for the hackathon. It contains information about various countries. This dataset has been cleaned and preprocessed, but contains missing values. You may preprocess the data further as needed.
The following columns are present in the dataset:
- `country`: The name of the country.
- `density_per_km2`: The population density per square kilometer.
- `abbreviation`: The abbreviation of the country's name.
- `agricultural_land_perc`: The percentage of land used for agriculture.
- `land_area_km2`: The total land area in square kilometers.
- `armed_forces_size`: The size of the armed forces.
- `birth_rate`: The birth rate or number of live births per 1,000 population.
- `calling_code`: The calling code of the country.
- `capital_major_city`: The capital city or a major city of the country.
- `co2_emissions`: The CO2 emissions in kilotons.
- `cpi`: The Consumer Price Index of the country. The Consumer Price Index (CPI) is a measure of the average change over time in the prices paid by urban consumers for a market basket of consumer goods and services.
- `cpi_change_perc`: The percentage change in the Consumer Price Index.
- `currency_code`: The currency code of the country.
- `fertility_rate`: The fertility rate or average number of children that are born to a woman over her lifetime.
- `forested_area_perc`: The percentage of land covered by forests.
- `gasoline_price`: The price of gasoline in US dollars per liter.
- `gdp`: The Gross Domestic Product (GDP) of the country in US dollars.
- `gross_primary_education_enrollment_perc`: The gross primary education enrollment percentage, which is the total number of students enrolled in primary education, regardless of age, as a percentage of the population of official primary education age.
- `gross_tertiary_education_enrollment_perc`: The gross tertiary education enrollment percentage, which is the total number of students enrolled in tertiary education, regardless of age, as a percentage of the population of official tertiary education age.
- `infant_mortality`: The infant mortality rate or number of deaths of infants under one year old per 1,000 live births.
- `largest_city`: The name of the largest city in the country.
- `life_expectancy`: The life expectancy at birth in years.
- `maternal_mortality_ratio`: The maternal mortality ratio or number of maternal deaths per 100,000 live births.
- `minimum_wage`: The minimum wage in US dollars.
- `official_language`: The official language of the country.
- `out_of_pocket_health_expenditure`: The out-of-pocket health expenditure as a percentage of total health expenditure, which is the direct payment made by individuals to health practitioners and suppliers of pharmaceuticals, therapeutic appliances, etc.
- `physicians_per_thousand`: The number of physicians per 1,000 population.
- `population`: The total population of the country.
- `population_labor_force_participation_perc`: The percentage of the population that is part of the labor force.
- `tax_revenue_perc`: The tax revenue as a percentage of GDP.
- `total_tax_rate`: The total tax rate, which is the sum of corporate income tax, personal income tax, and social security contributions as a percentage of commercial profits.
- `unemployment_rate`: The unemployment rate as a percentage of the labor force.
- `urban_population`: The urban population as a percentage of the total population.
- `latitude`: The latitude of the country.
- `longitude`: The longitude of the country.


#### `main.py`
This is the main script that contains the `DataAnalysis` class.
This class contains methods to load the dataset and ask questions.
- `__init__(self, filepath: str, **kwargs)` : The constructor method that initializes the `DataAnalysis` class.
It takes the filepath of the dataset as input.
You can add any additional arguments as needed.
- `analysis(self, user_input: str)` : The method that performs the analysis based on the user input.
It takes the user input, uses the LLM to generate code for the analysis, and executes the code.
It returns the result of the analysis.
- `plotting(self, user_input: str)` : The method that creates a plot based on the user input.
It takes the user input, creates a plot, and saves it as a PNG file.
It returns the path to the saved plot.
To create a plot, this method uses the LLM to generate code.
- `insights(self, user_input: str)` : The method that provides insights based on the user input.
It takes the user input, uses the LLM to summarize the analysis results, and returns the insights.
- `ask(self, user_input: str)` : The method assists the user in asking questions.
It coordinates the analysis, plotting, and insights methods.

#### `prompt_texts.py`
The script where you should add your prompts.
The dictionary `PROMPTS` is imported into `main.py` and used when calling the LLM.

#### `utils.py`
This script contains utility functions.
You will find optional functions here, and you can add your own functions as needed.

#### `example.py`
This script contains example code to demonstrate how to use the `DataAnalysis` class.
Once you have added your prompts, you may run this code to ask questions and view the results.

## Evaluation Criteria

1. **Accuracy**: Are the answers accurate, relevant, and complete? The answers should be supported by the information in the dataset.
2. **Creativity**: Have you used interesting prompts and techniques? Try a variety of prompts and techniques to see what works best.
3. **Contextual Understanding**: Do the answers show a good understanding of the dataset?
4. **Data Science Techniques**: Were any relevant data science techniques used to answer a given question? For example, data preprocessing, feature engineering, etc.

## Submission

Please submit your final code as a zip file containing all the necessary files.