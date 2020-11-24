 Author: Jost von Petersdorff-Campen

# Data 

## Cases 

1. Germany

   - *RKI_COVID_individuals.csv* - cases in Germany over time over Bundesländer
   - *rki_wochenberichte* PDFs - Test data in Germany over time

   

2. Italy

   - *dpc-covid19-ita-regioni-202002**t*** - cases and tests in Italy over region at time **t**
   - *Italy_pop.csv* - Italian population over regions



## Weather

1. Germany
   - *data_TXK_MN004.csv* - temperature of stations in Germany over time 
   - *sdo_TXK_MN004.csv* - stations matched to cities in Germany
   - https://www.dwd.de/DE/leistungen/klimadatendeutschland/statliste/statlex_html.html?view=nasPublication&nn=16102 - cities matched to Bundesländer
   - Preprocessed and merged: Germany_cases_weather.csv
   
   
   
   
   
   # Scripts
   
   1. preprocess_germany.py : Merge Bundesländer, cases, tests and weather into Germany_cases_weather.csv
   2. 
   
   

