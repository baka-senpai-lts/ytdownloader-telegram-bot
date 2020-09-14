# ytdownloader-telegram-bot
To create image:
docker build -t telegram-bot .

To start:
docker run --rm -d -e BOT_TOKEN="%YOUR_TOKEN%" --name=bot telegram-bot

To stop:
docker stop bot
