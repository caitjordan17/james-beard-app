import json


def load_json_data(filename="restaurant_awards.json"):
    with open(filename, "r") as f:
        data = json.load(f)
    return data


restaurant_data = load_json_data()


def init_seed_chef_json(filename="manual_chef_db.json"):
    chef_dict = {}
    for entry in restaurant_data:
        restaurant = entry["restaurant"]
        for chef in entry["chefs"]:
            if chef not in chef_dict:
                chef_dict[chef] = set()
            chef_dict[chef].add(restaurant)

    formatted_data = [
        {
            "chef": chef,
            "award_restaurants": list(restaurants),
            "other_restaurants": []
        }
        for chef, restaurants in chef_dict.items()
    ]

    with open(filename, "w") as f:
        json.dump(formatted_data, f, indent=4)
    print(f"Chef data saved to {filename}")


if __name__ == "__main__":
    init_seed_chef_json()

# subsequent_seed_chef.py to notify me of any new chefs I need to manaully check
# but what if they open a new restaurant? how do i continually check for that?
# and what if a restaurant I manually added wins award?
