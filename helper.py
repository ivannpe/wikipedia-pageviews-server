import asyncio
import aiohttp
import calendar

from collections import defaultdict
from datetime import date, timedelta

BASE_URL = "https://wikimedia.org/api/rest_v1/metrics/pageviews/"
ARTICLE_ENDPOINT = "per-article/en.wikipedia/all-access/all-agents/"
MOST_VIEWED_ENDPOINT = "top/en.wikipedia/all-access/"
HEADERS = {'User-Agent': 'GrowTherapyTakeHome/1.0 (ivannpe@gmail.com)'}

async def most_viewed_articles_weekly_async(date: date):
    dates = get_dates_in_range(date, "weekly")

    async with aiohttp.ClientSession() as session:
        tasks = [make_async_request(session, f'{BASE_URL}{MOST_VIEWED_ENDPOINT}{curr_date.strftime("%Y/%m/%d")}') for curr_date in dates]
        results = await asyncio.gather(*tasks)
    return results

async def make_async_request(session, url):
    async with session.get(url, headers=HEADERS) as response:
        return await response.json()

def get_dates_in_range(date, granularity):
    if granularity == "weekly":
        start = date - timedelta(days=date.weekday())
        return [(start + timedelta(days=i)) for i in range(1)]
    else:
        start, end = get_date_range(date, granularity)
        return [(start + timedelta(days=i)) for i in range((end - start).days + 1)]

def get_date_range(date, granularity):
    if granularity == "weekly":
        start = date - timedelta(days=date.weekday())
        end = start + timedelta(days=6)
    else:
        start = date - timedelta(days=date.day - 1)
        days_in_month = calendar.monthrange(date.year, date.month)[1]
        end = start + timedelta(days=days_in_month - 1)

    return start, end
  
def aggregate_and_sort(data):
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

    result = []
    for article_info in data["items"][0]["articles"]:
        result.append({
            article: article_info[article],
            key: article_info[key],
            views: article_info[views]
        })

    return result
