def parse_user_data(user_data: dict) -> dict:
    for key in ["first_name", "last_name", "email"]:
        if user_data.get(key):
            user_data[key] = user_data[key].strip().title()

    return user_data
