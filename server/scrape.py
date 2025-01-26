import requests
from bs4 import BeautifulSoup
import json
from collections import defaultdict


def scrape_jamesbeard():
    print("Starting James Beard scrape...")
    restaurant_awards = defaultdict(list)
    chef_awards = defaultdict(list)

    cities = ["san+francisco", "berkeley", "oakland"]
    base_url = "https://www.jamesbeard.org/awards/search?categories%5BRestaurant+%26+Chef%5D=1&year=&keyword={city}&page={page}"

    for city in cities:
        print("Scraping {city}...")
        for page in range(1, 11):
            url = base_url.format(city=city, page=page)
            r = requests.get(url)
            r.raise_for_status()

            soup = BeautifulSoup(r.content, 'html.parser')

            results = soup.find('div', class_="c-results c-results--awards")
            if not results:
                break

            result_list = results.find_all("div", class_="c-award-recipient")

            for result_item in result_list:
                nominee = {}
                name = result_item.find("p", class_="c-award-recipient__name")
                if name:
                    nominee["name"] = name.text.strip()

                award_details = result_item.find_all(
                    "p", class_="c-award-recipient__text")

                if len(award_details) == 5:
                    nominee["location"] = award_details[1].text.strip() if len(
                        award_details) > 1 else None
                    nominee["category"] = f'James Beard - {award_details[2].text.strip() if len(
                        award_details) > 2 else None}'
                    nominee["level"] = award_details[3].text.strip() if len(
                        award_details) > 3 else None
                    nominee["year"] = award_details[4].text.strip() if len(
                        award_details) > 4 else None
                elif len(award_details) == 6:
                    nominee["restaurant"] = award_details[1].text.strip() if len(
                        award_details) > 1 else None
                    nominee["location"] = award_details[2].text.strip() if len(
                        award_details) > 2 else None
                    nominee["category"] = f'James Beard - {award_details[3].text.strip() if len(
                        award_details) > 3 else None}'
                    nominee["level"] = award_details[4].text.strip() if len(
                        award_details) > 4 else None
                    nominee["year"] = award_details[5].text.strip() if len(
                        award_details) > 5 else None

                if "restaurant" in nominee:
                    restaurant_awards[nominee["restaurant"]].append(nominee)
                if "name" in nominee:
                    chef_awards[nominee["name"]].append(nominee)
    print("James Beard scraping complete.")
    return restaurant_awards, chef_awards


def scrape_michelin():
    print("Starting Michelin scrape...")
    restaurant_awards = defaultdict(list)
    base_url = "https://guide.michelin.com/us/en/california/san-francisco/restaurants{page}?showMap=true&sort=distance&boundingBox=38.0279268585259%2C-122.20027990745969%2C37.517127976824064%2C-122.567927963724"

    for num in range(1, 11):
        url = base_url.format(page=f'/page/{num}')

    # grab results from michelin html

    r = requests.get(url)
    r.raise_for_status()

    soup = BeautifulSoup(r.content, 'html.parser')

    results = soup.find(
        'div', class_='row restaurant__list-row js-restaurant__list_items')
    if not results:
        break

    # https://guide.michelin.com/us/en/california/san-francisco/restaurants/page/4?showMap=true&sort=distance&boundingBox=37.96280254344287%2C-122.15305189008589%2C37.58020920761482%2C-122.53772303952611
