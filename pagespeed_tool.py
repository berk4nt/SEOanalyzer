import requests
import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

def get_pagespeed_metrics(url):
    api_key = os.getenv("PAGESPEED_API_KEY")
    endpoint = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"

    params = {
        "url": url,
        "key": api_key,
        "strategy": "desktop"  # mobile için değiştirilebilir
    }

    response = requests.get(endpoint, params=params)

    if response.status_code == 200:
        data = response.json()

        lighthouse = data.get("lighthouseResult", {})
        performance_score = lighthouse.get("categories", {}).get("performance", {}).get("score", None)
        audits = lighthouse.get("audits", {})

        return {
            "performance_score": performance_score,
            "first_contentful_paint": audits.get("first-contentful-paint", {}).get("displayValue"),
            "speed_index": audits.get("speed-index", {}).get("displayValue"),
            "largest_contentful_paint": audits.get("largest-contentful-paint", {}).get("displayValue"),
            "total_blocking_time": audits.get("total-blocking-time", {}).get("displayValue"),
            "cumulative_layout_shift": audits.get("cumulative-layout-shift", {}).get("displayValue")
        }
    else:
        return {"error": f"API error: {response.status_code}"}

