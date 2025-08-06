import requests
from bs4 import BeautifulSoup
import re
import textstat

def analyze_keywords(url, keyword):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Metin içeriğini al
        text = soup.get_text(separator=' ', strip=True)
        word_list = re.findall(r'\b\w+\b', text.lower())
        total_words = len(word_list)

        # Anahtar kelime sayısı
        keyword_lower = keyword.lower()
        keyword_count = word_list.count(keyword_lower)

        # Yoğunluk hesaplama
        density = (keyword_count / total_words) * 100 if total_words > 0 else 0

        # Başlık ve meta açıklama kontrolü
        title = soup.title.string if soup.title else ''
        meta_description = ''
        meta_tag = soup.find('meta', attrs={'name': 'description'})
        if meta_tag and 'content' in meta_tag.attrs:
            meta_description = meta_tag['content']

        in_title = keyword_lower in title.lower()
        in_description = keyword_lower in meta_description.lower()

        # Okunabilirlik puanı
        readability_score = textstat.flesch_reading_ease(text)

        return {
            "keyword": keyword,
            "total_words": total_words,
            "keyword_count": keyword_count,
            "keyword_density_percent": round(density, 2),
            "in_title": in_title,
            "in_meta_description": in_description,
            "readability_score": readability_score
        }

    except Exception as e:
        return {"error": str(e)}

