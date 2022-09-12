import glob
import pathlib
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


def conv_to_size(path_to_save=NoReturn):
    image_dir = glob.glob("/*.png")

    for image in image_dir:
        image = Image.open(image)
        if image.size[0] / 1920 > image.size[1] / 1080:
            vertical_resolution = image.size[0] * 1080 / 1920
            vertical_resolution = vertical_resolution - image.size[1]
            vertical_resolution = int(vertical_resolution / 2)
            resolution = add_margin(
                image, vertical_resolution, 0, vertical_resolution, 0, (0, 0, 0)
            )
        else:
            horizontal_resolution = image.size[1] * 1920 / 1080
            horizontal_resolution = horizontal_resolution - image.size[0]
            horizontal_resolution = int(horizontal_resolution / 2)
            resolution = add_margin(
                image, 0, horizontal_resolution, 0, horizontal_resolution, (0, 0, 0)
            )
        resolution.save(path_to_save) if path_to_save is not None else resolution.save(
            image_dir
        )


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
