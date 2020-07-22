import ast
from flask import Flask, jsonify, request, url_for
import requests as r

app = Flask(__name__)

# Using Studio Ghibli API
SG_URL = "https://ghibliapi.herokuapp.com"
# FIELDS = ('id', 'title', 'description', 'director', 'producer', 'release_date', 'rt_score')


@app.route("/films/", methods=["GET"])
def films():
    """A method to get a list of films sorted by a specified field and limited to a specified max size.
    Fields to show in the result can be specified as a string comma-separated field names.
    """
    # first, get all the films (API specifies 250 as a max value for 'limit') to properly sort
    res = r.get(
        SG_URL + "/films", params={"limit": "250", "fields": request.args.get("fields")}
    )
    if res.ok:
        res = ast.literal_eval(res.text)
        if request.args.get("sort"):
            reverse = False
            if request.args.get("r") == "True":
                reverse = True
            res = sorted(
                res, key=lambda x: x[request.args.get("sort")], reverse=reverse
            )
        if request.args.get("limit"):
            res = res[: int(request.args.get("limit"))]
        # Couldn't figure out how to return the list of jsonified dicts so the response doesn't look great
        return jsonify(res)
    else:
        return res


@app.route("/films/<string:title>", methods=["GET"])
def film_by_title(title):
    """A method to get a specific film by its title.
    Fields to show in the result can be specified as a string comma-separated field names.
    """
    # first, get all the films (API specifies 250 as a max value for 'limit') to properly search
    res = r.get(
        SG_URL + "/films", params={"limit": "250", "fields": request.args.get("fields")}
    )
    if res.ok:
        res = ast.literal_eval(res.text)
        try:
            res = list(filter(lambda x: x["title"] == title, res))[0]
        except IndexError:
            return 404
        # Couldn't figure out how to return the list of jsonified dicts so the response doesn't look great
        return jsonify(res)
    else:
        return res


# URLs for test requests
with app.test_request_context():
    print(
        url_for(
            "films",
            sort="release_date",
            limit="10",
            fields="title,release_date,rt_score",
        )
    )
    print(
        url_for(
            "film_by_title",
            title="Princess Mononoke",
            fields="title,release_date,rt_score",
        )
    )
