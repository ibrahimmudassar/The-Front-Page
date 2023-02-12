from datetime import datetime

import fitz
from discord_webhook import DiscordEmbed, DiscordWebhook
from environs import Env  # For environment variables
from requests import get

# Setting up environment variables
env = Env()
env.read_env()  # read .env file, if it exists


def embed_to_discord():
    # create embed object for webhook
    title = "The New York Times Front Page"
    day_today = datetime.now().strftime("%b. %d, %Y")
    embed = DiscordEmbed(title=title, description=day_today, color="000000")

    # set image
    embed.set_image(url='attachment://out.png')

    # set footer
    embed.set_footer(text="\"All the News That's Fit to Print\"")

    # add embed object to webhook(s)
    # Webhooks to send to
    for webhook_url in env.list("WEBHOOKS"):
        webhook = DiscordWebhook(url=webhook_url)

        with open("out.png", "rb") as f:
            webhook.add_file(file=f.read(), filename='out.png')

        webhook.add_embed(embed)
        webhook.execute()


# Get todays date and get the link to todays paper
now = datetime.now().strftime("%Y/%m/%d/")
link = f"https://static01.nyt.com/images/{now}nytfrontpage/scan.pdf"

f = open('Paper.pdf', "wb")
f.write(get(link).content)
f.close()

# To get better resolution
zoom_x = 2.0  # horizontal zoom
zoom_y = 2.0  # vertical zoom
mat = fitz.Matrix(zoom_x, zoom_y)  # zoom factor 2 in each dimension

# To convert single page
doc = fitz.open("Paper.pdf")
page = doc.load_page(0)  # first and only page
pix = page.get_pixmap(matrix=mat)
pix.save("out.png")

embed_to_discord()

#
#   BELOW IS ARCHIVED CODE FOR REFERENCE
#

# CROPPING AN IMAGE

# im = Image.open("out.png")
# width, height = im.size

# # Setting the points for cropped image
# left = 0
# top = 125
# right = width
# bottom = height

# im1 = im.crop((left, top, right, bottom))
# im1.save('out.png')

#   UPLOADING AN IMAGE TO A WEBHOST AND LINKING

# defining the api-endpoint
# API_ENDPOINT = "https://api.imgbb.com/1/upload"


# with open("out.png", "rb") as file:
#     payload = {
#         "key": env('API_KEY'),
#         "image": base64.b64encode(file.read()),
#     }
#     res = post(API_ENDPOINT, payload)


# front_page_url = res.json()["data"]["url"]
