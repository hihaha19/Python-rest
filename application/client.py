import requests
from .models import Post


def get_external_data(id):
    url = "https://my-json-server.typicode.com/hihaha19/json-server/posts"
    response = requests.get(url)
    data = response.json()
    for post in data:
        if int(id) == post['id']:
            if not Post.objects.filter(title=post["title"], userID=post["userID"], body=post["body"]).exists():
                Post.objects.create(title=post["title"], userID=post["userID"], body=post["body"])
                print("saved")

            return post['id']

    return 0


def get_user_id(userid):
    url = "https://my-json-server.typicode.com/hihaha19/json-server/users"
    response = requests.get(url)
    data = response.json()
    for post in data:
        print(post)
        if int(userid) == post['userID']:
            return True

    return False
