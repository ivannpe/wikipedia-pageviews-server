import asyncio
import datetime
import pytest

from helper import most_viewed_articles_weekly_async,make_async_request, get_dates_in_range, get_date_range, aggregate_and_sort, format_result


MOCK_RESPONSE_DATA = {
    "items": [
        {
            "project": "en.wikipedia",
            "access": "all-access",
            "year": "2020",
            "month": "02",
            "day": "all-days",
            "articles": [
                {"article": "Main_Page", "views": 303451296, "rank": 1},
                {"article": "Joseph_Buttigieg", "views": 268085, "rank": 1000}
            ]
        }
    ]
}


class MockResponse:
    def __init__(self, data):
        self.data = data

    async def json(self):
        return self.data


class MockSession:
    async def get(self, url, headers):
        return MockResponse(MOCK_RESPONSE_DATA)


@pytest.mark.asyncio
async def test_most_viewed_articles_weekly_async():
    date = datetime.date(2022, 1, 1)
    result = await most_viewed_articles_weekly_async(date, session_class=MockSession)
    assert result == [MOCK_RESPONSE_DATA] * 7  # Adjust based on your actual expected results


@pytest.mark.asyncio
async def test_make_async_request():
    url = "https://example.com"
    result = await make_async_request(session=MockSession(), url=url)
    assert result == MOCK_RESPONSE_DATA


def test_get_dates_in_range_weekly():
    date = datetime.date(2022, 1, 1)
    result = get_dates_in_range(date, "weekly")
    assert result[0] == datetime.date(2021, 12, 27)


def test_get_dates_in_range_monthly():
    date = datetime.date(2022, 1, 1)
    result = get_dates_in_range(date, "monthly")
    expected_result = [datetime.date(2022, 1, i) for i in range(1, 32)]
    assert result == expected_result


def test_get_date_range_weekly():
    date = datetime.date(2022, 1, 1)
    start, end = get_date_range(date, "weekly")
    assert start == datetime.date(2021, 12, 27)
    assert end == datetime.date(2022, 1, 2)


def test_get_date_range_monthly():
    date = datetime.date(2022, 1, 1)
    start, end = get_date_range(date, "monthly")
    assert start == datetime.date(2022, 1, 1)
    assert end == datetime.date(2022, 1, 31)


def test_aggregate_and_sort():
    input_data = [MOCK_RESPONSE_DATA] * 7
    result = aggregate_and_sort(input_data)
    assert len(result) == 2


def test_format_result():
    input_data = MOCK_RESPONSE_DATA
    result = format_result(input_data)
    expected_result = [
        {"article": "Main_Page", "rank": 1, "views": 303451296},
        {"article": "Joseph_Buttigieg", "rank": 1000, "views": 268085}
    ]
    assert result == expected_result
