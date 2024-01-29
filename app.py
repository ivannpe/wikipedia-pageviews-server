import asyncio
import helper
import requests

from datetime import datetime
from flask import Flask, jsonify


app = Flask(__name__)


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
        return formatted_result
    
    m_date = d_date.strftime("%Y/%m")
    response = requests.get(f'{helper.BASE_URL}{helper.MOST_VIEWED_ENDPOINT}{m_date}/all-days',headers=helper.HEADERS)

    return helper.format_result(response.json())


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

    d_date = datetime.strptime(date, "%Y%m%d")
    if granularity == "weekly":
        views = 0
        start, end = helper.get_date_range(d_date, "weekly")
        response = requests.get(f'{helper.BASE_URL}{helper.ARTICLE_ENDPOINT}{article}/daily/{start.strftime("%Y%m%d")}/{end.strftime("%Y%m%d")}', headers=helper.HEADERS)
        for i in response.json()["items"]:
            views += i["views"]
        result =  {
            "article": response.json()["items"][0]["article"],
            "week": response.json()["items"][0]["timestamp"],
            "views": views
        }
        return jsonify(result)
    
    start, end = helper.get_date_range(d_date, "monthly")
    response = requests.get(f'{helper.BASE_URL}{helper.ARTICLE_ENDPOINT}{article}/monthly/{start.strftime("%Y%m%d")}/{end.strftime("%Y%m%d")}', headers=helper.HEADERS)

    result = {
        "article": response.json()["items"][0]["article"],
        "month": response.json()["items"][0]["timestamp"],
        "views": response.json()["items"][0]["views"]
    }

    return jsonify(result)


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
    d_date = datetime.strptime(date, "%Y%m%d")
    start, end = helper.get_date_range(d_date, "monthly")
    print(start, end)
    response = requests.get(f'{helper.BASE_URL}{helper.ARTICLE_ENDPOINT}{article}/daily/{start.strftime("%Y%m%d")}/{end.strftime("%Y%m%d")}', headers=helper.HEADERS)
    
    max_views = 0
    max_views_day = None

    for day in response.json()["items"]:
        timestamp = datetime.strptime(day["timestamp"], "%Y%m%d%H")
      
        if day["views"] > max_views:
            max_views = day["views"]
            max_views_day = timestamp.strftime("%Y-%m-%d")

    result = {
        "article": response.json()["items"][0]["article"],
        "day": max_views_day,
        "views": max_views
    } 
    return jsonify(result)


if __name__ == '__main__':
    app.run()