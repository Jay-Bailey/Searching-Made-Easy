from enum import Enum

DISALLOWED_FEATURES = ["Create Search Terms with AI"]

CHROME_PATH ='C:/Program Files/Google/Chrome/Application/chrome.exe'
FIREFOX_PATH = 'C:/Program Files/Mozilla Firefox/firefox.exe'

class BrowserString(Enum):
    CHROME = 'Chrome'
    FIREFOX = 'Firefox'

    @classmethod
    def from_string(cls, browser):
        try:
            return cls[browser]
        except KeyError:
            raise ValueError(f"Invalid color: {browser}")
