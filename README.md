
# AGRO 365

## Authors

- Dorely Medina Leal [@dorely_ml](https://www.instagram.com/dorely_ml)
- Isaí Vilches [@capitansombrero](https://www.instagram.com/capitansombrero)
- Andrey Balvaneda [@andrei.balv](https://www.instagram.com/andrei.balv)
- Carlos Carillo [@charles.avionistico](https://www.instagram.com/charles.avionistico)
- Ernesto G. Santana [dernestogsantana@gmail.com](dernestogsantana@gmail.com)

---

## Nierika Bot

Nierika Bot is a helpful and conversational Telegram bot designed to provide geographic data, such as coordinates extracted from Google Maps URLs, and environmental imagery from NASA's ECOSTRESS mission. The bot is built with a user-friendly interface, provides natural language suggestions, and offers personalized assistance.

## Features

- **Extract Coordinates from Google Maps URLs**: Simply provide a Google Maps link, and the bot will return the corresponding latitude and longitude.
- **ECOSTRESS Imagery**: Given a location URL, Nierika Bot can fetch thermal imagery from NASA’s ECOSTRESS mission.
- **Natural Language Understanding**: The bot provides proactive suggestions when it detects incomplete inputs or common requests.
- **Error Handling**: Nierika Bot gracefully handles errors, providing clear, friendly error messages to users.
- **Personalization**: The bot keeps track of users' interactions, offering a more personalized experience with returning users.
- **Group Chat Support**: The bot can respond to commands in group chats when tagged with its username.

## Commands

- `/start`: Start a conversation with the bot. The bot will greet the user and offer guidance.
- `/help`: Display the list of available commands and instructions on how to interact with the bot.
- `/coords <maps_url>`: Extract coordinates (latitude and longitude) from a Google Maps URL.
- `/ecostress <maps_url>`: Fetch ECOSTRESS imagery based on the coordinates of a Google Maps location.

## Setup Instructions

### Prerequisites

To run this bot, you will need the following:
- **Python 3.8+** installed on your machine.
- A **Telegram Bot Token** from [BotFather](https://core.telegram.org/bots#botfather) on Telegram.
- **Nominatim API** for geocoding (used to extract coordinates from postal codes).
- The following Python libraries:
  - `python-telegram-bot`
  - `requests`
  - `geopy`
  - `re` (standard library)
  - `ecostress_image_download` (Assumed to be a custom module you have access to)

### Installation

1. Clone the repository or copy the bot code to your local environment.
   
   ```bash
   git clone https://github.com/your-username/nierika-bot.git
   cd nierika-bot
   ```

2. Create a virtual environment and install the required Python packages:

   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Create a `.env` file or set your Telegram bot token as an environment variable:

   ```bash
   echo "TELEGRAM_TOKEN=your-telegram-token-here" > .env
   ```

4. If you are using the ECOSTRESS image functionality, make sure you have access to the required data sources or APIs. The `ecostress_image_download` module should be properly configured to interact with the imagery APIs.

### Running the Bot

Once you have the environment set up and the token ready:

```bash
python bot.py
```

This will start the bot and allow it to respond to commands in your Telegram chat.

## Usage Examples

### Extracting Coordinates from Google Maps

- Send the bot a Google Maps URL like:

  ```
  /coords https://www.google.com/maps/place/40.748817,-73.985428
  ```

- The bot will respond with:

  ```
  Here are the coordinates: lat, lon = 40.748817, -73.985428 🌍
  ```

### Fetching ECOSTRESS Imagery

- Send the bot a Google Maps URL to get ECOSTRESS imagery:

  ```
  /ecostress https://www.google.com/maps/place/34.052235,-118.243683
  ```

- The bot will fetch and respond with the ECOSTRESS image.

### Help Command

- If you're unsure of how to use the bot, simply type:

  ```
  /help
  ```

- The bot will respond with a list of available commands and instructions.

### Group Chat Support

In a group chat, mention the bot with its username to trigger it:

```
@Nierika_bot /coords https://www.google.com/maps/place/48.8588443,2.2943506
```

The bot will respond with the extracted coordinates.

## Error Handling

Nierika Bot handles common errors gracefully, providing helpful feedback if:
- The Google Maps URL is invalid.
- There are network issues fetching the data.
- ECOSTRESS imagery cannot be retrieved.

For example, if you provide an invalid URL, the bot might respond with:

```
Oops! Something went wrong while fetching the coordinates: Invalid URL format.
```

## Customization

If you'd like to customize Nierika Bot further:
- You can add more features by expanding the `handle_response` function.
- Customize the greetings and help texts to match your bot's personality.

## Contributing

Feel free to fork the repository, create new features, or fix bugs. Pull requests are welcome!

---

### Notes

- Replace `your-telegram-token-here` with your actual Telegram bot token.
- The bot assumes the `ecostress_image_download` module is available. Ensure that this module is set up to work correctly.
- This bot was developed with Python's asynchronous capabilities (`asyncio`), so make sure to keep the code consistent with async functions when adding new features.

Enjoy using Nierika Bot! 😊

## Authors

- Dorely Medina Leal [@octokatherine](https://www.github.com/octokatherine)
- Isaí Vilches[@octokatherine](https://www.github.com/octokatherine)
- Andrey [@octokatherine](https://www.github.com/octokatherine)
- Carlos [@octokatherine](https://www.github.com/octokatherine)
- Ernesto G. Santana [dernestogsantana@gmail.com](dernestogsantana@gmail.com)

