import base64
from datetime import datetime
from requests import get, post
from pdf2image import convert_from_path
from PIL import Image
from discord_webhook import DiscordWebhook, DiscordEmbed
from environs import Env  # For environment variables

# Setting up environment variables
env = Env()
env.read_env()  # read .env file, if it exists


def embed_to_discord(link):
    # Webhooks to send to
    webhook = DiscordWebhook(url=env.list("WEBHOOKS"))

    # create embed object for webhook
    title ="The New York Times Front Page"
    day_today = now.strftime("%b. ") + str(int(now.strftime("%d"))) + now.strftime(", %Y")
    embed = DiscordEmbed(title=title, description=day_today, color="000000")

    # Mentioning the link to the article
    embed.add_embed_field(name="Link", value= "[Read Full Page Here](" + link + ")", inline=False)
    
    # set image
    with open("out.png", "rb") as f:
        webhook.add_file(file=f.read(), filename='out.png')
    embed.set_image(url='attachment://out.png')

    # set footer
    embed.set_footer(text="\"All the News That's Fit to Print\"")

    # add embed object to webhook(s)
    webhook.add_embed(embed)
    webhook.execute()


# Get todays date and get the link to todays paper
now = datetime.now()
link = "https://static01.nyt.com/images/" + now.strftime("%Y/%m/%d/") + "nytfrontpage/scan.pdf"

f = open('Paper.pdf', "wb")
f.write(get(link).content)
f.close()

pages = convert_from_path('Paper.pdf')
for page in pages:
    page.save('out.png', 'PNG')

im = Image.open(".\out.png")
width, height = im.size

# Setting the points for cropped image
left = 0
top = 125
right = width
bottom = height

im1 = im.crop((left, top, right, bottom))
im1.save(".\out.png")


# defining the api-endpoint
API_ENDPOINT = "https://api.imgbb.com/1/upload"


with open("out.png", "rb") as file:
    payload = {
        "key": env('API_KEY'),
        "image": base64.b64encode(file.read()),
    }
    res = post(API_ENDPOINT, payload)


front_page_url = res.json()["data"]["url"]

embed_to_discord(front_page_url)
