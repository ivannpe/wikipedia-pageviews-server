import asyncio
import helper
import json
import requests

from datetime import datetime
from flask import Flask #, request, render_template 





app = Flask(__name__)

@app.route("/")
def hello_world():
    """
    Summary line.

    Extended description of function.

    Parameters
    ----------
    arg1 : int
        Description of arg1
    arg2 : str
        Description of arg2

    Returns
    -------
    int
        Description of return value

    """
    return "<p>Hello, World!</p>"


#TODO - determine assumptions about what these all mean and what api calls will be used for them

# if an article is not listed on a given day, you can assume it has 0 views
# input: date, granularity
# output: json of list of articles and their respective view count
# 
@app.route("/pageviews/top/<string:date>/<string:granularity>", methods=['GET'])
def most_viewed_articles(date: str, granularity: str):
    """
    Retrieves a list of the most viewed articles for a week or a month.

    Args:
        date (str): Description of arg1
        granularity (str): Description of arg2

    Returns:
        JSON: Description of return value
    """
    d_date = datetime.strptime(date, "%Y%m%d")

    if granularity == "weekly":
        result = asyncio.run(helper.most_viewed_articles_weekly_async(d_date))

        formatted_result = helper.aggregate_and_sort(result)
        return json.dumps(formatted_result)
    
    m_date = d_date.strftime("%Y/%m")
    response = requests.get(f'{helper.BASE_URL}{helper.MOST_VIEWED_ENDPOINT}{m_date}/all-days',headers=helper.HEADERS)

    return helper.format_result(response.json())



# input: article, date, granularity
# output: view count, json
@app.route("/pageviews/article/<string:article>/<string:date>/<string:granularity>", methods=['GET'])
def article_pageviews(article: str, date: str, granularity: str):
    """
    Retrieves the view count of a specific article for a week or a month.

    Args:
        article (str): Description of arg1
        date (str): Description of arg2
        granularity (str): Description of arg3

    Returns:
        JSON: Description of return value

    """
    return ""

# input: article, date
# output: day of month, json, page views
# todo: sort through each day, keep track of MAX val in the month
@app.route("/pageviews/top/article/<string:article>/<string:date>/day", methods=['GET'])
def day_of_most_pageviews(article: str, date: str):
    """
    Retrieves the day of the month where an article got the most page views.

    Args:
        article (str): Description of arg1
        date (str): Description of arg2

    Returns:
        JSON: Description of return value

    """
    return ""


if __name__ == '__main__':
    app.run()