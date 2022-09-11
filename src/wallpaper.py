from datetime import datetime
from typing import NoReturn

import yfinance as yf
from PIL.Image import Image

now = datetime.now()
current_time = now.strftime("%H:%M:%S")


def add_margin(img, top, left, bottom, right, color):
    width, height = img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(img.mode, (new_width, new_height), color)
    result.paste(img, (left, top))
    return result


def conv_to_size(path, path_to_save=NoReturn):
    z = Image.open(path)
    if z.size[0] / 1920 > z.size[1] / 1080:
        vres = z.size[0] * 1080 / 1920
        vres = vres - z.size[1]
        vres = int(vres / 2)
        res = add_margin(z, vres, 0, vres, 0, (0, 0, 0))
    else:
        hres = z.size[1] * 1920 / 1080
        hres = hres - z.size[0]
        hres = int(hres / 2)
        res = add_margin(z, 0, hres, 0, hres, (0, 0, 0))
    if path_to_save is not None:
        res.save(path_to_save)
    else:
        res.save(path)


tickers = [
    ("^GSPC", "s&p500"),
    ("aapl", "aapl"),
    ("msft", "msft"),
    ("goog", "googl"),
    ("amzn", "amzn"),
    ("tsla", "tsla"),
    ("BTC-USD", "btc"),
    ("ETH-USD", "eth"),
]


def ret_change(ticker):
    x = yf.Ticker(ticker)
    z = x.history(period="3d")
    return (
        ((z.iloc[-1]["Close"] - z.iloc[-2]["Close"]) / z.iloc[-2]["Close"]) * 100
    ).round(2), z.iloc[-1]["Close"].round(2)
