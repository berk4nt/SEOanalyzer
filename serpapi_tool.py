import os
import requests
from dotenv import load_dotenv

load_dotenv()
SERP_API_KEY = os.getenv("SERP_API_KEY")

def get_serp_rank(keyword, domain):
    """
    Belirtilen keyword için Google'da domain'in sıralamasını getirir.
    SerpAPI kullanır.
    """
    try:
        params = {
            "engine": "google",
            "q": keyword,
            "api_key": SERP_API_KEY,
            "num": 10
        }
        response = requests.get("https://serpapi.com/search", params=params)
        data = response.json()

        # Organik sonuçlarda domain arama
        organic_results = data.get("organic_results", [])
        for result in organic_results:
            link = result.get("link", "")
            if domain in link:
                rank = result.get("position", None)
                return {
                    "keyword": keyword,
                    "domain": domain,
                    "rank": rank
                }
        # Bulunamazsa
        return {
            "keyword": keyword,
            "domain": domain,
            "rank": None,
            "message": "Domain ilk sayfada bulunamadı."
        }

    except Exception as e:
        return {"error": str(e)}


