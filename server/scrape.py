import requests
from bs4 import BeautifulSoup
import json
from collections import defaultdict

restaurant_data = defaultdict(
    lambda: {"chefs": set(), "location": "", "awards": set()})


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
                name = result_item.find("p", class_="c-award-recipient__name")
                award_details = result_item.find_all(
                    "p", class_="c-award-recipient__text")

                if not name or len(award_details) < 4:
                    continue

                award_name = f"James Beard - {award_details[0].text.strip(
                )}, {award_details[-2].text.strip()}, {award_details[-1].text.strip()}"

                if any(keyword in award_details[0].text.strip() for keyword in ["Chef", "Baker", "Restauranteur", "Hospitality", "Lifetime"]) and "Bakery" not in award_details[0].text.strip():
                    chef = name.text.strip()
                    restaurant = award_details[1].text.strip() if len(
                        award_details) > 4 else "Unknown"
                    location = award_details[2].text.strip() if len(
                        award_details) > 4 else "Unknown"
                else:
                    restaurant = name.text.strip()
                    location = award_details[1].text.strip()
                    chef = "Unknown"

                restaurant_data[restaurant]["location"] = location
                restaurant_data[restaurant]["awards"].add(award_name)
                if chef != "Unknown":
                    restaurant_data[restaurant]["chefs"].add(chef)

                print("James Beard scraping complete.")


def scrape_michelin():
    print("Starting Michelin scrape...")
    base_url = "https://guide.michelin.com/us/en/california/san-francisco/restaurants/all-starred/bib-gourmand{page}?showMap=true&sort=distance&boundingBox=38.0279268585259%2C-122.20027990745969%2C37.517127976824064%2C-122.567927963724"

    for num in range(1, 11):
        url = base_url.format(page=f'/page/{num}')
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
            get_restaurant = result_item.find("a")
            get_award = result_item.find("img", class_="michelin-award")
            get_location = result_item.find(
                "div", class_="card__menu-footer--score pl-text")

            if not get_restaurant:
                continue

            restaurant = get_restaurant.text.strip()
            location = get_location.text.strip() if get_location else "Unknown"

            award = ""
            if get_award:
                src_result = get_award["src"]
                if "bib-gourmand" in src_result:
                    award = "Bib Gourmand"
                elif "1star" in src_result:
                    award = "1 Michelin Star"
                elif "2star" in src_result:
                    award = "2 Michelin Stars"
                elif "3star" in src_result:
                    award = "3 Michelin Stars"
                elif "gastronomie" in src_result:
                    award = "Michelin Green Star"

            if award:
                restaurant_data[restaurant]["location"] = location
                restaurant_data[restaurant]["awards"].add(award)

    print("Michelin scraping complete.")

# google places API


def save_to_json(filename="restaurant_awards.json"):
    formatted_data = []
    for restaurant, details in restaurant_data.items():
        formatted_data.append({
            "restaurant": restaurant,
            "chefs": list(details["chefs"]),
            "location": details["location"],
            "awards": list(details["awards"])
        })

    with open(filename, "w") as f:
        json.dump(formatted_data, f, indent=4)
    print(f"Data saved to {filename}")


if __name__ == "__main__":
    scrape_jamesbeard()
    scrape_michelin()
    save_to_json()
