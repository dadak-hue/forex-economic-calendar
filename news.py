import requests
import json
from datetime import datetime


print("Stahuji ekonomický kalendář...")


url = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"


response = requests.get(
    url,
    headers={
        "User-Agent": "Mozilla/5.0"
    }
)


if response.status_code != 200:
    print("Chyba:", response.status_code)
    exit()


data = response.json()


news = []


for item in data:

    # pouze důležité zprávy
    if item.get("impact") == "High":

        event = item.get("title", "")
        currency = item.get("currency", "")


        # české vysvětlení

        if "CPI" in event:
            explanation = (
                "Inflace. Velmi důležitá zpráva. "
                "Může způsobit velký pohyb na USD párech a zlatě."
            )

        elif "NFP" in event:
            explanation = (
                "Data zaměstnanosti USA. "
                "Jedna z nejvíce volatilních zpráv."
            )

        elif "Rate" in event:
            explanation = (
                "Rozhodnutí o úrokových sazbách. "
                "Silný vliv na měnu."
            )

        else:
            explanation = (
                "Důležitá ekonomická zpráva. "
                "Může zvýšit volatilitu trhu."
            )


news.append({

    "id": len(news)+1,
    "date": item.get("date"),
    "time": item.get("time"),
    "currency": currency,
    "event": event,
    "impact": "HIGH",
    "actual": "-",
    "forecast": "-",
    "previous": "-",
    "explanation": explanation

})


with open(
    "news.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        news,
        file,
        ensure_ascii=False,
        indent=4
    )


print("Hotovo! news.json vytvořen.")