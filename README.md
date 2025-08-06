# 🚀 SEO Analiz Aracı

Bu proje, resimdeki mimariye uygun olarak geliştirilmiş kapsamlı bir SEO analiz aracıdır. 4 agent'tan oluşan bir crew sistemi kullanarak Gemini API ile entegre çalışır.

## 📋 Özellikler

### 🤖 Agent Yapısı
- **Technical SEO Agent**: PageSpeed Insights ve SERP API kullanarak teknik SEO analizi
- **Keyword Control Agent**: Anahtar kelime analizi, başlık kontrolü ve okunabilirlik analizi
- **Report Agent**: Kapsamlı SEO raporları oluşturma
- **Report Quality Agent**: Rapor kalite kontrolü ve iyileştirme önerileri

### 🔧 Teknik Özellikler
- CrewAI framework kullanımı
- Gemini API entegrasyonu
- PageSpeed Insights API entegrasyonu
- SerpAPI entegrasyonu
- Otomatik rapor kaydetme
- Etkileşimli kullanıcı arayüzü

## 🛠️ Kurulum

### 1. Gereksinimler
```bash
pip install crewai google-generativeai python-dotenv requests beautifulsoup4 textstat
```

### 2. API Anahtarları
`env_example.txt` dosyasını `.env` olarak kopyalayın ve API anahtarlarınızı ekleyin:

```bash
cp env_example.txt .env
```

Gerekli API anahtarları:
- **Gemini API**: https://makersuite.google.com/app/apikey
- **PageSpeed API**: https://console.cloud.google.com/apis/credentials
- **SerpAPI**: https://serpapi.com/

### 3. .env Dosyası Örneği
```env
GEMINI_API_KEY=your_gemini_api_key_here
PAGESPEED_API_KEY=your_pagespeed_api_key_here
SERP_API_KEY=your_serp_api_key_here
```

## 🚀 Kullanım

### 🌐 Web Arayüzü (Önerilen)
```bash
python gradio_app.py
```
Tarayıcınızda `http://localhost:7860` adresine gidin.

### 📱 Terminal Arayüzü
```bash
python main.py
```

### 🔧 Programatik Kullanım
```python
from seo_crew import run_seo_analysis

result = run_seo_analysis(
    url="https://example.com",
    keyword="seo analiz",
    domain="example.com"
)
print(result)
```

## 📁 Dosya Yapısı

```
seoanalyzer/
├── gradio_app.py          # 🌐 Web arayüzü (Gradio)
├── main.py                # 📱 Terminal arayüzü
├── seo_crew.py            # 🤖 Crew yapısı ve agent'lar
├── keywordcontrol.py      # 🔍 Anahtar kelime analiz fonksiyonu
├── pagespeed_tool.py      # ⚡ PageSpeed API fonksiyonu
├── serpapi_tool.py        # 📊 SERP API fonksiyonu
├── env_example.txt        # 🔑 API anahtarları örneği
├── requirements.txt        # 📦 Gerekli kütüphaneler
└── README.md              # 📖 Bu dosya
```

## 🔍 Analiz Özellikleri

### Technical SEO Analizi
- PageSpeed performans skoru
- First Contentful Paint
- Speed Index
- Largest Contentful Paint
- Total Blocking Time
- Cumulative Layout Shift

### Anahtar Kelime Analizi
- Anahtar kelime yoğunluğu
- Başlık optimizasyonu
- Meta açıklama kontrolü
- Okunabilirlik puanı (Flesch Reading Ease)

### SERP Analizi
- Google sıralama kontrolü
- Domain pozisyon analizi

## 📊 Çıktı Formatı

Analiz sonuçları JSON formatında kaydedilir:
```json
{
  "timestamp": "20241201_143022",
  "url": "https://example.com",
  "keyword": "seo analiz",
  "domain": "example.com",
  "result": {
    "technical_seo": {...},
    "keyword_analysis": {...},
    "comprehensive_report": {...},
    "quality_control": {...}
  }
}
```

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Commit yapın (`git commit -m 'Add some AmazingFeature'`)
4. Push yapın (`git push origin feature/AmazingFeature`)
5. Pull Request oluşturun

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 🆘 Sorun Giderme

### Yaygın Hatalar

1. **API Anahtarı Hatası**
   - `.env` dosyasının doğru konumda olduğundan emin olun
   - API anahtarlarının geçerli olduğunu kontrol edin

2. **Bağlantı Hatası**
   - İnternet bağlantınızı kontrol edin
   - API servislerinin erişilebilir olduğunu doğrulayın

3. **Import Hatası**
   - Gerekli kütüphanelerin yüklendiğinden emin olun
   - Python sürümünüzün uyumlu olduğunu kontrol edin

## 📞 İletişim

Sorularınız için issue açabilir veya pull request gönderebilirsiniz. 