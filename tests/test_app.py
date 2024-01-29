import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_most_viewed_articles_weekly(client):
    response = client.get('/pageviews/top/20220101/weekly')
    assert response.status_code == 200


def test_most_viewed_articles_monthly(client):
    response = client.get('/pageviews/top/20220101/monthly')
    assert response.status_code == 200


def test_article_pageviews_weekly(client):
    response = client.get('/pageviews/article/Main_Page/20220101/weekly')
    assert response.status_code == 200


def test_article_pageviews_monthly(client):
    response = client.get('/pageviews/article/Main_Page/20220101/monthly')
    assert response.status_code == 200


def test_day_of_most_pageviews(client):
    response = client.get('/pageviews/top/article/Main_Page/20220101/day')
    assert response.status_code == 200
