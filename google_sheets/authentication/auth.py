from database.db import exist_user, add_user, update_url


def user_connect(user_id, url):
    msg = ''
    try:
        if exist_user(user_id):
            msg = update_url(user_id, url)
        else:
            msg = add_user(user_id, url)
    finally:
        return msg
