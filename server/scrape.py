import requests
from bs4 import BeautifulSoup
import json
from collections import defaultdict

restaurant_awards = defaultdict(list)
chef_awards = defaultdict(list)


def scrape_jamesbeard():
    print("Starting James Beard scrape...")

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

                award_details = result_item.find_all(
                    "p", class_="c-award-recipient__text")

                if any(keyword in award_details[0].text.strip() for keyword in ["Chef", "Baker", "Restauranteur", "Hospitality", "Lifetime"]) and "Bakery" not in award_details[0].text.strip():
                    nominee["chef"] = name.text.strip()
                else:
                    nominee["restaurant"] = name.text.strip()

                if len(award_details) == 5:
                    nominee["location"] = award_details[1].text.strip()
                    nominee["award"] = {
                        f'James Beard - {award_details[0].text.strip()}, {award_details[3].text.strip()}, {
                            award_details[4].text.strip()}'
                    }

                if len(award_details) == 6:
                    nominee["restaurant"] = award_details[1].text.strip()
                    nominee["location"] = award_details[2].text.strip()
                    nominee["award"] = {
                        f'James Beard - {award_details[0].text.strip()}, {award_details[4].text.strip()}, {
                            award_details[5].text.strip()}'
                    }

                if "restaurant" in nominee:
                    restaurant_awards[nominee["restaurant"]].append(nominee)
                if "chef" in nominee:
                    chef_awards[nominee["chef"]].append(nominee)
    print("James Beard scraping complete.")

    return restaurant_awards, chef_awards

# need to append awards to restaurant list


def scrape_michelin():
    print("Starting Michelin scrape...")
    base_url = "https://guide.michelin.com/us/en/california/san-francisco/restaurants/all-starred/bib-gourmand{page}?showMap=true&sort=distance&boundingBox=38.0279268585259%2C-122.20027990745969%2C37.517127976824064%2C-122.567927963724"

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

        result_list = results.find_all(
            "div", class_="card__menu-content card__menu-content--flex js-match-height-content")

        for result_item in result_list:
            winner = {}
            # print("CAIT:", {result_item})
            get_restaurant = result_item.find("a")
            get_award = result_item.find("img", class_="michelin-award")
            get_location = result_item.find(
                "div", class_="card__menu-footer--score pl-text")
            # print("CAIT:", len(get_award))
            """
            winner["restaurant"]
            winner["location"]
            winner["award"]
            """

            # RESTAURANT NAME
            if get_restaurant:
                winner["restaurant"] = get_restaurant.text.strip()
                # print("NAME:", {get_restaurant.text.strip()})

            # RESTAURANT LOCATION
            if get_location:
                winner["location"] = get_location.text.strip()

            # AWARD NAME
            if len(get_award) == 0:
                src_result = get_award["src"]
                if "bib-gourmand" in src_result:
                    winner["award"] = "Bib Gourmand"
                elif "1star" in src_result:
                    winner["award"] = "1 Michelin Star"

            elif len(get_award) == 1:
                src_result = get_award["src"]
                if "gastronomie" in src_result:
                    winner["award"] = {
                        "1 Michelin Star",
                        "Michelin Green Star"
                    }
                else:
                    winner["award"] = "2 Michelin Stars"

            elif len(get_award) == 2:
                src_result = get_award["src"]
                if "gastronomie" in src_result:
                    winner["award"] = {
                        "2 Michelin Stars",
                        "Michelin Green Star"
                    }
                else:
                    winner["award"] = "3 Michelin Stars"
            elif len(get_award) == 3:
                winner["award"] = {
                    "3 Michelin Stars",
                    "Michelin Green Star"
                }

            print("WINNER:", winner)
