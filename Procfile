web: gunicorn -b :$PORT -w 4 -k uvicorn.workers.UvicornWorker bot.main:application
worker: python -m bot.main
clock: python clock.py
