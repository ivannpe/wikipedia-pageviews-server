# Wikipedia Pageviews Server
Web Server interacting with Wikipedia API


## Installation
Clone Repository:
```sh
$ git clone https://github.com/ivannpe/wikipedia-pageviews-server.git
$ cd wikipedia-pageviews-server
```
Setup Virtual Environment:
```sh
$ python -m venv .venv
$ . .venv/bin/activate
```
Install Dependencies with pip:

```sh
$ pip install -r requirements.txt
```

## Run Application
To start server:
```sh
$ flask run
```

## Run Tests
```sh
$ cd tests
$ pytest {file_name}.py
```
## API Endpoints
### `GET` `/pageviews/top/<string:date>/<string:granularity>`
__Most Viewed Article for a Week or Month__

Accepts a `date`(YYYYMMDD) and `granularity`(weekly OR monthly) and retrieves a list of dictionaries with the 1000 most viewed articles, their rank, and views, for a week or a month.

#### Arguments:
`date(str)`: Date in String format (YYYYMMDD)  
`granularity(str)`: Time period for search, (weekly OR monthly)
#### Returns:
`List[Dict[str, str, str]]`: List of dictionaries with the 1000 most viewed articles, their rank, and views, for a week or a month.

#### Examples:
Weekly
```sh
curl -XGET "http://127.0.0.1:5000/pageviews/top/20240119/weekly"
```
Monthly
```sh
curl -XGET "http://127.0.0.1:5000/pageviews/top/20240119/monthly"
```
__________________________________________________________________________________
### `GET` `/pageviews/article/<string:article>/<string:date>/<string:granularity>`
__View Count of a Specific Article for a Week or Month__

Accepts the title of any `article`(Any spaces should be replaced with underscores. It also should be URI-encoded, so that non-URI-safe characters like %, / or ? are accepted. Example: Are_You_the_One%3F'), `date`(YYYYMMDD) and `granularity`(weekly OR monthly) and retrieves a JSON object with the Article name, Timestamp for granularity, and number of views for inputed `article`. 

#### Arguments:
`article(str)`: Article name  
`date(str)`: Date in String format (YYYYMMDD)  
`granularity(str)`: Time period for search, (weekly OR monthly)
#### Returns:
`JSON`: JSON Object with Article name, Timestamp for granularity, and number of views

#### Examples:
Weekly
```sh
curl -XGET "http://127.0.0.1:5000/pageviews/article/Albert_Einstein/20240119/weekly"
```
Monthly
```sh
curl -XGET "http://127.0.0.1:5000/pageviews/article/Albert_Einstein/20240119/monthly"
```
__________________________________________________________________________________
### `GET` `/pageviews/top/article/<string:article>/<string:date>/day`
__Day of the Month where an Article got the Most Pageviews__
Accepts the title of any `article`(Any spaces should be replaced with underscores. It also should be URI-encoded, so that non-URI-safe characters like %, / or ? are accepted. Example: Are_You_the_One%3F') and `date`(YYYYMMDD) and retrieves a JSON Object with Article name, Timestamp of the day with the most page views, and number of views.

#### Arguments:
`article(str)`: Article name  
`date(str)`: Date in String format (YYYYMMDD)
#### Returns:
`JSON`: JSON Object with Article name, Timestamp of the day with the most page views, and number of views

#### Examples:
```sh
curl -XGET "http://127.0.0.1:5000/pageviews/top/article/Albert_Einstein/20240119/day"
```
## Assumptions
- Week starts on Monday
- A week/month refers to a calendar week/month
- Most Viewed Articles Weekly limited to 1000 entries similar to responses of other calls

## Improvements & Next Steps
- __Error Handling:__ I should be more thorough in Error Handling given the pageview api calls are sensitive to proper formatting of inputs to these endpoints. As well as many things are dependent on the success, `200` response of these calls.
- __Testing:__ More thorough on testing based on error handling, and other unexpected behaviors and responses
- __Rate Limiting:__ Implementing rate limiting, such that Wikipedia API limits aren't exceeded. Especially since there are instances of making asynchronous requests
- __Website:__ Currently calls to the API endpoints are made through a curl request. Having an interface to interact with the calls being made, and that properly formats the responses would be ideal
- __Links:__ In the vein of better interaction, having links to the articles shown and listed to bring users to interact with Wikipedia and have a better understanding of perhaps why view counts are what they are. 
