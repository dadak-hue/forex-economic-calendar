import requests
import json


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
        
        currency = item.get("country", "")


        # pokud měna chybí, odvodíme ji

        if currency == "":
            
            text = event.upper()

            if any(x in text for x in ["FED", "CPI", "GDP", "FOMC", "NFP"]):
                currency = "USD"

            elif "BOE" in text or "GBP" in text:
                currency = "GBP"

            elif "ECB" in text or "EUR" in text:
                currency = "EUR"

            elif "BOJ" in text or "JPY" in text:
                currency = "JPY"

            else:
                currency = "OTHER"



        # české vysvětlení

        if "CPI" in event.upper():

            explanation = (
                "Inflace. Velmi důležitá zpráva. "
                "Může způsobit velký pohyb na USD párech a zlatě."
            )

        elif "NFP" in event.upper():

            explanation = (
                "Data zaměstnanosti USA. "
                "Jedna z nejvíce volatilních zpráv."
            )

        elif "RATE" in event.upper():

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
            "time": item.get("time", "N/A"),
            "currency": currency,
            "event": event,
            "impact": "HIGH",
            "actual": item.get("actual", "-"),
            "forecast": item.get("forecast", "-"),
            "previous": item.get("previous", "-"),
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
