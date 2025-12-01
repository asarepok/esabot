import json
import os
import chevron
import logging

LOCALES_DIR = os.path.join(os.path.dirname(__file__))

locales = {}

def load_locales():
    global locales
    for filename in os.listdir(LOCALES_DIR):
        if filename.endswith(".json"):
            lang = filename.replace(".json", "")
            with open(os.path.join(LOCALES_DIR, filename), "r", encoding="utf8") as f:
                # store translations for different locales once
                locales[lang] = json.load(f)

# load locales onces on import of the locales module
load_locales()


def l(key: str, lang: str = "en", **kwargs) -> str:
    # Retrieve translations from a specific locale. You can also pass arguments to fill arguments in the locale text.
    # Example locale json: {"welcome":"Welcome {{username}}"}
    # l("welcome", lang="en", username="user1") will render the text "Welcome user1"

    try:
        raw_str = locales.get(key)
    except KeyError:
        logging.error(f"The local {lang}.json does not have a {key} key.")

    print(chevron.render(raw_str, data=kwargs))
    return chevron.render(raw_str, kwargs).strip()