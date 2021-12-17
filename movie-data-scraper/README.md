# Movie Data Scraper

## Information:
This is a data scraper that scrapes horror movies and tv shows data from various websites. (Sample set of 100 titles)
The goal was to store this data in a database.
<br>
The data collected will consist of the following:
- Title, Type, Genre / Sub Genre, Director(s), Actor(s), Run Time, Release Date and the Media Cover or a link to the file.

## Prerequisites:
- Install `Python3`. To install, follow the tutorial [here](https://realpython.com/installing-python/) 
  and find the downloads [here](https://www.python.org/downloads/).
- Configure a python virtual environment. Follow [this](https://docs.python.org/3/library/venv.html) tutorial to know how.
- Install all the requirements as specified in the [requirements](requirements.txt) file.
- Clone or Download the repository onto your machine.
- Or fork the repo if contributing.

## How to run:
- Navigate into the repository directory on your machine.
- Make sure all the globals are set as per requirements in the [main](main.py) script.
- Activate the venv created earlier.
- Run: `python3 main.py`

## Libraries used:
`Requests`
`Beautiful Soup`
`PyMongo`

### Note:
Find the output of the script [here](data/output.md)
