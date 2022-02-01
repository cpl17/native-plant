Repo Includes: 

**ERA_PA** The Excel Sheet containing records on plants native to the Chester County area, indexed by USDA Symbol  

**main.py** The script scrapes Wildflower.org for missing information related to Bloom Color, Soil Moisture, Height, Sun Exposure, Bloom Period. The scraped values
are stored in a dictionary, written to a Pandas DataFrame, and used to update a copy of the original data. Finally, the DataFrame is written to an Excel sheet. 