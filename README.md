![Ironhack logo](https://i.imgur.com/1QgrNNw.png)

# Lab | ETL

The goal of this project is to mix data from multiple sources, putting into practice what we have learned this week about ETL (extract, transform and load). Perform a proper cleaning of the data obtained using all the techniques learned for it, such as Python, Pandas or SQL. Creating functions and storing them in a `.py` file. 


## About the project


The World Cup organized by FIFA is a soccer competition that brings together teams from all the countries of the world. All countries wishing to participate play in the qualifying phase, but only the teams that qualify play in the competition. This competition is held once every 4 years.

On the occasion of the next World Cup to be held from November in Qatar, we have compiled information on all the matches that have been played in the past competitions to filter and obtain interesting information on the results obtained by each team.

With the code found in the `main.ipynb` file, you can enter the name of two teams and it will return a table with the data of all the occasions in which those two teams have faced each other, number of goals scored by each one, wins, defeats, draws and how many world titles each one has, as well as how many times they have been runner-up and how many times they have finished third.

Country names can be entered in either English or Spanish.


## What we have done:

- The data has been obtained from 3 sources and using 2 different techniques as requested by the exercise: the history and information about past matches from 2 csv files and the match calendar from a web page using the web scraping technique with Selenium.
- Database cleaning and preservation of the necessary information to obtain our objective.
- Creation of a `.py` file with all the functions created and used.



## Submission:

- `main.ipynb` 
- `WorldCup.csv` 
- `WorldCupMatches.csv` 


## Links & Resources

- https://www.google.com/search?q=fifa+world+cup&rlz=1C1CHBF_esES983ES983&oq=fifa+wor&aqs=chrome.0.0i131i355i433i512j46i131i433i512j0i131i433i512l3j69i57j69i60l2.5699j1j7&sourceid=chrome&ie=UTF-8#sie=lg;/m/0fp_8fm;2;/m/030q7;mt;fp;1;;;
- <https://www.kaggle.com/teajay/global-shark-attacks>
- <https://numpy.org/doc/1.18/>
- <https://pandas.pydata.org/>
- https://docs.python.org/3/library/functions.html
- https://plotly.com/python/
- https://matplotlib.org/
- https://seaborn.pydata.org/
- https://pandas.pydata.org/docs/
- https://towardsdatascience.com/beware-of-storytelling-with-data-1710fea554b0?gi=537e0c10d89e