from instagrapi import Client

cl = Client()
cl.login("", "")

cl.photo_upload(
    path="gg.jpg",
    caption="Hello from Python! 🌟"
)