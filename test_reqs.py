import requests as r

print(
    r.get(
        "http://localhost:5000/films/?sort=release_date&limit=10&fields=title%2Crelease_date%2Crt_score"
    ).text
)
print("\n\n\n")
print(
    r.get(
        "http://localhost:5000/films/Princess%20Mononoke?fields=title%2Crelease_date%2Crt_score"
    ).text
)
