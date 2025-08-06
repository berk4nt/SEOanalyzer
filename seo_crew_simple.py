import os
import json
from datetime import datetime
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
from typing import Dict, Any
import google.generativeai as genai

# Mevcut fonksiyonları import et
from keywordcontrol import analyze_keywords
from pagespeed_tool import get_pagespeed_metrics
from serpapi_tool import get_serp_rank

# .env dosyasını yükle
load_dotenv()

# Gemini API anahtarını ayarla
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini modelini yapılandır (opsiyonel)
model = None
if GEMINI_API_KEY and GEMINI_API_KEY != "your_gemini_api_key_here":
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        print("✅ Gemini API başarıyla yapılandırıldı")
    except Exception as e:
        print(f"⚠️ Gemini API yapılandırma hatası: {str(e)}")
        model = None
else:
    print("⚠️ Gemini API anahtarı bulunamadı, basit rapor oluşturulacak")

class PageSpeedTool(BaseTool):
    name: str = "PageSpeed Tool"
    description: str = "Google PageSpeed Insights API kullanarak web sitesi performans metriklerini alır"

    def _run(self, url: str) -> str:
        try:
            result = get_pagespeed_metrics(url)
            return f"PageSpeed analizi tamamlandı: {result}"
        except Exception as e:
            return f"PageSpeed analizi sırasında hata: {str(e)}"

class SerpRankTool(BaseTool):
    name: str = "SERP Rank Tool"
    description: str = "SERP API kullanarak anahtar kelime için domain sıralamasını kontrol eder"

    def _run(self, keyword: str, domain: str) -> str:
        try:
            result = get_serp_rank(keyword, domain)
            return f"SERP analizi tamamlandı: {result}"
        except Exception as e:
            return f"SERP analizi sırasında hata: {str(e)}"

class KeywordControlTool(BaseTool):
    name: str = "Keyword Control Tool"
    description: str = "Anahtar kelime analizi, başlık kontrolü ve okunabilirlik analizi yapar"

    def _run(self, url: str, keyword: str) -> str:
        try:
            result = analyze_keywords(url, keyword)
            return f"Anahtar kelime analizi tamamlandı: {result}"
        except Exception as e:
            return f"Anahtar kelime analizi sırasında hata: {str(e)}"

def create_simple_report(url: str, keyword: str, domain: str, pagespeed_data: dict, serp_data: dict, keyword_data: dict):
    """API anahtarı olmadan basit rapor oluşturur"""
    
    report = f"""
# 📊 SEO Analiz Raporu

## 🌐 Analiz Edilen Site
- **URL**: {url}
- **Anahtar Kelime**: {keyword}
- **Domain**: {domain}
- **Analiz Tarihi**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## ⚡ PERFORMANS ANALİZİ
"""
    
    if pagespeed_data and not isinstance(pagespeed_data, str):
        report += f"""
### PageSpeed Insights Sonuçları:
- **Mobil Skor**: {pagespeed_data.get('mobile_score', 'N/A')}
- **Desktop Skor**: {pagespeed_data.get('desktop_score', 'N/A')}
- **İlk İçerik Boyama**: {pagespeed_data.get('first_contentful_paint', 'N/A')}
- **Largest Contentful Paint**: {pagespeed_data.get('largest_contentful_paint', 'N/A')}
"""
    else:
        report += "\n### PageSpeed Analizi: Veri alınamadı\n"
    
    report += f"""
## 📈 SERP SIRALAMASI
"""
    
    if serp_data and not isinstance(serp_data, str):
        report += f"""
### SERP Analizi Sonuçları:
- **Sıralama**: {serp_data.get('rank', 'N/A')}
- **Toplam Sonuç**: {serp_data.get('total_results', 'N/A')}
- **Domain**: {serp_data.get('domain', 'N/A')}
"""
    else:
        report += "\n### SERP Analizi: Veri alınamadı\n"
    
    report += f"""
## 🔍 ANAHTAR KELİME OPTİMİZASYONU
"""
    
    if keyword_data and not isinstance(keyword_data, str):
        report += f"""
### Anahtar Kelime Analizi:
- **Başlık Uyumu**: {keyword_data.get('title_match', 'N/A')}
- **Meta Açıklama**: {keyword_data.get('meta_description', 'N/A')}
- **Okunabilirlik Skoru**: {keyword_data.get('readability_score', 'N/A')}
"""
    else:
        report += "\n### Anahtar Kelime Analizi: Veri alınamadı\n"
    
    report += f"""
## 🎯 İYİLEŞTİRME ÖNERİLERİ

### Genel SEO İyileştirmeleri:
1. **Sayfa Hızı**: Sayfa yükleme hızını artırın
2. **Mobil Uyumluluk**: Mobil cihazlarda iyi performans sağlayın
3. **Anahtar Kelime Optimizasyonu**: Başlık ve meta açıklamalarda anahtar kelimeyi kullanın
4. **İçerik Kalitesi**: Kaliteli ve özgün içerik oluşturun

### Teknik SEO:
1. **Meta Etiketleri**: Title ve description etiketlerini optimize edin
2. **URL Yapısı**: Temiz ve anlaşılır URL'ler kullanın
3. **İç Linkleme**: Site içi linkleme yapısını güçlendirin
4. **Dış Linkleme**: Kaliteli sitelerden backlink alın

## 📋 EYLEM PLANI

### Kısa Vadeli (1-2 Hafta):
- [ ] Sayfa hızı optimizasyonu
- [ ] Meta etiketlerin güncellenmesi
- [ ] Anahtar kelime yoğunluğunun kontrolü

### Orta Vadeli (1-2 Ay):
- [ ] İçerik kalitesinin artırılması
- [ ] Backlink stratejisinin geliştirilmesi
- [ ] Teknik SEO sorunlarının çözülmesi

### Uzun Vadeli (3-6 Ay):
- [ ] Site genelinde SEO optimizasyonu
- [ ] İçerik stratejisinin geliştirilmesi
- [ ] Performans takip sisteminin kurulması

---
*Bu rapor otomatik olarak oluşturulmuştur. Daha detaylı analiz için Gemini API anahtarınızı ayarlayın.*
"""
    
    return report

def run_seo_analysis(url: str, keyword: str, domain: str):
    """
    SEO analizi için basit sistem çalıştırır
    """
    try:
        print("🔍 PageSpeed analizi yapılıyor...")
        pagespeed_data = get_pagespeed_metrics(url)
        
        print("📊 SERP analizi yapılıyor...")
        serp_data = get_serp_rank(keyword, domain)
        
        print("🔤 Anahtar kelime analizi yapılıyor...")
        keyword_data = analyze_keywords(url, keyword)
        
        # Gemini API varsa kullan, yoksa basit rapor oluştur
        if model:
            print("🤖 Gemini ile kapsamlı analiz yapılıyor...")
            
            analysis_prompt = f"""
            Aşağıdaki SEO analiz verilerini kullanarak kapsamlı bir SEO raporu oluştur:

            WEB SİTESİ: {url}
            ANAHTAR KELİME: {keyword}
            DOMAIN: {domain}

            PAGESPEED VERİLERİ:
            {json.dumps(pagespeed_data, indent=2, ensure_ascii=False)}

            SERP VERİLERİ:
            {json.dumps(serp_data, indent=2, ensure_ascii=False)}

            KEYWORD ANALİZ VERİLERİ:
            {json.dumps(keyword_data, indent=2, ensure_ascii=False)}

            Lütfen aşağıdaki başlıklar altında detaylı bir SEO raporu oluştur:

            1. 📊 GENEL SEO DURUMU
            2. ⚡ PERFORMANS ANALİZİ
            3. 🔍 ANAHTAR KELİME OPTİMİZASYONU
            4. 📈 SERP SIRALAMASI
            5. 🎯 İYİLEŞTİRME ÖNERİLERİ
            6. 📋 EYLEM PLANI

            Raporu Türkçe olarak, emoji'lerle zenginleştirilmiş ve anlaşılır bir şekilde hazırla.
            """
            
            try:
                response = model.generate_content(analysis_prompt)
                return response.text
            except Exception as e:
                print(f"⚠️ Gemini API hatası: {str(e)}")
                return create_simple_report(url, keyword, domain, pagespeed_data, serp_data, keyword_data)
        else:
            print("📝 Basit rapor oluşturuluyor...")
            return create_simple_report(url, keyword, domain, pagespeed_data, serp_data, keyword_data)
        
    except Exception as e:
        return f"SEO analizi sırasında hata oluştu: {str(e)}"

if __name__ == "__main__":
    # Test için örnek kullanım
    url = "https://example.com"
    keyword = "seo analiz"
    domain = "example.com"
    
    result = run_seo_analysis(url, keyword, domain)
    print("SEO Analiz Sonucu:")
    print(result) 