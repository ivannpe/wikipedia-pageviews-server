import asyncio
import aiohttp
import calendar

from collections import defaultdict
from datetime import date, timedelta

BASE_URL = "https://wikimedia.org/api/rest_v1/metrics/pageviews/"
ARTICLE_ENDPOINT = "per-article/en.wikipedia/all-access/all-agents/"
MOST_VIEWED_ENDPOINT = "top/en.wikipedia/all-access/"
HEADERS = {'User-Agent': 'WikipediaPageviewsServer/1.0 (ivannpe@gmail.com)'}

async def most_viewed_articles_weekly_async(date: date):
    """
    Waits for and gathers responses to async calls to Wikipedia Pageviews API for every day in the calendar week of the given date

    Args:
        date (date): Date

    Returns:
        JSON: JSON Objects with the most viewed articles for every day in the calendar week of the given date

    """
    dates = get_dates_in_range(date, "weekly")

    async with aiohttp.ClientSession() as session:
        tasks = [make_async_request(session, f'{BASE_URL}{MOST_VIEWED_ENDPOINT}{curr_date.strftime("%Y/%m/%d")}') for curr_date in dates]
        results = await asyncio.gather(*tasks)
    return results

async def make_async_request(session, url):
    """
    Makes async request to Wikipedia Pageviews API
    Args:
        date (date): Date

    Returns:
        JSON: JSON Objects with the most viewed articles for a day

    """
    async with session.get(url, headers=HEADERS) as response:
        return await response.json()

def get_dates_in_range(date, granularity):
    """
    Calculates and returns a list of datetime objects, containing the range of date for a calendar week/month based on given date
    
    Args:
        date (date): Date
        granularity (str): Time period for search, weekly or monthly

    Returns:
        List[dates]: List of dates in a calendar week/month

    """
    if granularity == "weekly":
        start = date - timedelta(days=date.weekday())
        return [(start + timedelta(days=i)) for i in range(1)]
    else:
        start, end = get_date_range(date, granularity)
        return [(start + timedelta(days=i)) for i in range((end - start).days + 1)]

def get_date_range(date, granularity):
    """
    Calculates and returns a tuple of datetime objects, containing the start and end date for a calendar week/month based on given date
    
    Args:
        date (date): Date
        granularity (str): Time period for search, weekly or monthly

    Returns:
        Tuple[date, date]: Tuple of the start and end date for a calendar week/month

    """
    if granularity == "weekly":
        start = date - timedelta(days=date.weekday())
        end = start + timedelta(days=6)
    else:
        start = date - timedelta(days=date.day - 1)
        days_in_month = calendar.monthrange(date.year, date.month)[1]
        end = start + timedelta(days=days_in_month - 1)

    return start, end
  
def aggregate_and_sort(data):
    """
    Aggregates the multiple responses of most viewed articles for every day in a week, reranks and returns the 1000
    
    Args:
        data (JSON): The multiple responses of most viewed articles for every day in a week

    Returns:
        List[Dict[str, str, str]]: List of Dictionaries containing Article name, rank, and number of views

    """
    article_views = defaultdict(int)

    for item in data:
        for article_info in item["items"][0]["articles"]:
            article_views[article_info["article"]] += article_info["views"]

    sorted_articles = sorted(article_views.items(), key=lambda x: x[1], reverse=True)[:1000]

    result = []
    for rank, (article, views) in enumerate(sorted_articles, start=1):
        result.append({
            "article": article,
            "rank": rank,
            "views": views
        })

    return result

def format_result(data, article="article", key="rank", views="views"):
    """
    Formats article information
    
    Args:
        data (JSON): The JSON response object of most viewed articles in a month

    Returns:
        List[Dict[str, str, str]]: List of Dictionaries containing Article name, rank, and number of views

    """
    result = []
    for article_info in data["items"][0]["articles"]:
        result.append({
            article: article_info[article],
            key: article_info[key],
            views: article_info[views]
        })

    return result
