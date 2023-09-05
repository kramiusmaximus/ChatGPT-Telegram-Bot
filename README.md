# ChatGPT-Telegram-Bot
A telegram bot which connects to the OpenAI GPT4 model through their official API and implements basic context management of 8k tokens.

## Installation
In order to set this bot up on your local computer, you need to first create a telegram bot and place the token authorization token, then you'll need an OpenAI account.

1. Obtain Telegram Bot token, and OpenAI access tokens (see .env_example for extensive list of required tokens/Id's), and place the tokens into a .env file
2. Create virtual environment
   
```python3 -m venv venv```
3. Activate the virtual environment

```source venv/bin/activate```
4. Install python dependencies

```pip install -r requirements.txt```
5. Create and fill out .env file with necessary access data (see .env_example)

6. Start the main.py using Python

```python main.py```
7. Done! Try sending a message to your bot.

