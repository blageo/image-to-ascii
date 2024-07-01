import discord
from discord.ext import commands
from io import BytesIO
import PIL.Image
from config import BOT_TOKEN

# ASCII_CHARS and image processing functions from your original script
ASCII_CHARS = [
    "$",
    "@",
    "%",
    "&",
    "#",
    "+",
    "=",
    "-",
    ";",
    ":",
    ",",
    '"',
    "^",
    ".",
    " ",
]

# Define intents with required intents
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent

# Initialize the bot with intents
bot = commands.Bot(command_prefix="!", intents=intents)


# Resize image function (from your script)
def resize_image(image, new_width=44):
    width, height = image.size
    ratio = height / width / 1.65
    new_height = int(new_width * ratio)
    resized_image = image.resize((new_width, new_height))
    return resized_image


# Convert image to grayscale function (from your script)
def convert_to_grayscale(image):
    grayscale_image = image.convert("L")
    return grayscale_image


# Convert pixels to ASCII characters function (from your script)
def pixels_to_ascii(image):
    pixels = image.getdata()
    characters = ""
    for pixel in pixels:
        pixel_value = pixel // 15
        if pixel_value < 0:
            pixel_value = 0
        elif pixel_value >= len(ASCII_CHARS):
            pixel_value = len(ASCII_CHARS) - 1
        characters += ASCII_CHARS[pixel_value]
    return characters


# Define the main command for the bot
@bot.command()
async def ascii(ctx):
    # Check if an image is attached to the message
    if not ctx.message.attachments:
        await ctx.send("Please attach an image to convert to ASCII art.")
        return

    # Get the first attachment (assuming only one image is attached)
    attachment = ctx.message.attachments[0]

    # Check if the attachment is an image
    if not attachment.content_type.startswith("image"):
        await ctx.send("Please attach an image file.")
        return

    # Download the image
    try:
        image_bytes = await attachment.read()
        image = PIL.Image.open(BytesIO(image_bytes))
    except Exception as e:
        await ctx.send(f"Error processing image: {e}")
        return

    # Convert image to ASCII
    new_image_data = pixels_to_ascii(convert_to_grayscale(resize_image(image)))

    # Format ASCII art
    new_width = 44
    pixel_count = len(new_image_data)
    ascii_image = "\n".join(
        new_image_data[i : (i + new_width)] for i in range(0, pixel_count, new_width)
    )

    # Send ASCII art as a message
    await ctx.send(f"```\n{ascii_image}\n```")


# Run the bot
if __name__ == "__main__":
    bot.run(BOT_TOKEN)
