import os
import gradio as gr
import json
from datetime import datetime
from dotenv import load_dotenv
from seo_crew_simple import run_seo_analysis

# .env dosyasını yükle
load_dotenv()

def check_api_keys():
    """API anahtarlarının varlığını kontrol eder"""
    required_keys = ["GEMINI_API_KEY", "PAGESPEED_API_KEY", "SERP_API_KEY"]
    missing_keys = []
    
    for key in required_keys:
        if not os.getenv(key):
            missing_keys.append(key)
    
    if missing_keys:
        return False, f"❌ Eksik API anahtarları: {', '.join(missing_keys)}"
    
    return True, "✅ Tüm API anahtarları mevcut!"

def format_seo_report(result):
    """SEO raporunu güzel bir formatta döndürür"""
    if not result:
        return "❌ Analiz sonucu alınamadı."
    
    try:
        # Eğer result bir string ise, direkt döndür
        if isinstance(result, str):
            return result
        
        # Eğer result bir dict ise, formatla
        if isinstance(result, dict):
            formatted = "## 📊 SEO Analiz Raporu\n\n"
            
            for key, value in result.items():
                if isinstance(value, dict):
                    formatted += f"### {key.replace('_', ' ').title()}\n"
                    for sub_key, sub_value in value.items():
                        formatted += f"- **{sub_key.replace('_', ' ').title()}**: {sub_value}\n"
                    formatted += "\n"
                else:
                    formatted += f"**{key.replace('_', ' ').title()}**: {value}\n\n"
            
            return formatted
        
        return str(result)
    
    except Exception as e:
        return f"❌ Rapor formatlanırken hata oluştu: {str(e)}"

def analyze_seo(url, keyword, domain, progress=gr.Progress()):
    """SEO analizi yapar ve sonucu döndürür"""
    
    # API anahtarlarını kontrol et
    keys_ok, message = check_api_keys()
    if not keys_ok:
        return message, None, "❌ API Anahtarları Eksik"
    
    # Giriş parametrelerini doğrula
    if not url or not url.strip():
        return "❌ URL boş olamaz!", None, "❌ Geçersiz Giriş"
    
    if not keyword or not keyword.strip():
        return "❌ Anahtar kelime boş olamaz!", None, "❌ Geçersiz Giriş"
    
    if not domain or not domain.strip():
        return "❌ Domain boş olamaz!", None, "❌ Geçersiz Giriş"
    
    # URL formatını kontrol et
    if not url.startswith(('http://', 'https://')):
        return "❌ Geçerli bir URL girin (http:// veya https:// ile başlamalı)", None, "❌ Geçersiz URL"
    
    try:
        progress(0.1, desc="🔍 Analiz başlatılıyor...")
        
        # SEO analizini çalıştır
        progress(0.3, desc="🤖 Agent'lar çalışıyor...")
        result = run_seo_analysis(url.strip(), keyword.strip(), domain.strip())
        
        progress(0.8, desc="📊 Rapor hazırlanıyor...")
        
        # Raporu formatla
        formatted_result = result if result else "❌ Analiz sonucu alınamadı."
        
        # JSON raporu oluştur
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_data = {
            "timestamp": timestamp,
            "url": url.strip(),
            "keyword": keyword.strip(),
            "domain": domain.strip(),
            "result": result
        }
        
        # JSON dosyasını kaydet
        filename = f"seo_report_{timestamp}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        
        progress(1.0, desc="✅ Analiz tamamlandı!")
        
        return formatted_result, filename, "✅ Analiz Tamamlandı"
        
    except Exception as e:
        return f"❌ Analiz sırasında hata oluştu: {str(e)}", None, "❌ Hata Oluştu"

def download_report(filename):
    """Rapor dosyasını indirme linki oluşturur"""
    if filename and os.path.exists(filename):
        return filename
    return None

# Gradio arayüzünü oluştur
def create_interface():
    with gr.Blocks(
        title="🚀 Infera - Yapay Zeka Tabanlı SEO Analiz Platformu",
        theme=gr.themes.Soft(
            primary_hue="blue",
            secondary_hue="gray",
            neutral_hue="slate",
        ),
        css="""
        .gradio-container {
            max-width: 1600px !important;
            margin: 0 auto !important;
            padding: 0 !important;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%) !important;
            min-height: 100vh;
            position: relative;
            overflow: hidden;
        }
        
        .gradio-container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: 
                radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
                radial-gradient(circle at 40% 40%, rgba(120, 219, 255, 0.2) 0%, transparent 50%);
            pointer-events: none;
        }
        
        .main-content {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-radius: 30px;
            margin: 1rem;
            padding: 2.5rem;
            box-shadow: 
                0 25px 50px rgba(0, 0, 0, 0.15),
                0 0 0 1px rgba(255, 255, 255, 0.1),
                inset 0 1px 0 rgba(255, 255, 255, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.2);
            position: relative;
            overflow: hidden;
            width: calc(100% - 2rem);
            box-sizing: border-box;
        }
        
        .main-content::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.5), transparent);
        }
        
        .hero-section {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            border-radius: 25px;
            padding: 3rem 2rem;
            margin-bottom: 3rem;
            color: white;
            text-align: center;
            position: relative;
            overflow: hidden;
            box-shadow: 
                0 20px 40px rgba(102, 126, 234, 0.3),
                0 0 0 1px rgba(255, 255, 255, 0.1);
        }
        
        .hero-section::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: 
                radial-gradient(circle at 30% 30%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 70% 70%, rgba(255, 255, 255, 0.05) 0%, transparent 50%);
            animation: float 6s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(180deg); }
        }
        
        .hero-title {
            font-size: 3.5rem;
            font-weight: 800;
            margin-bottom: 1rem;
            color: #f093fb;
            text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
            position: relative;
            z-index: 2;
            background: linear-gradient(45deg, #f093fb, #667eea);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: 2px;
        }
        
        .hero-logo {
            text-align: center;
            margin-bottom: 2rem;
            position: relative;
            z-index: 2;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .hero-logo img {
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            max-width: 200px;
            height: auto;
        }
        
        .hero-logo img:hover {
            transform: scale(1.05);
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.4);
        }
        
        .logo-container {
            display: inline-block;
            text-align: center;
            margin-bottom: 1rem;
        }
        
        .logo-shapes {
            display: flex;
            justify-content: center;
            align-items: flex-end;
            gap: 8px;
            margin-bottom: 15px;
            height: 60px;
        }
        
        .shape {
            background: linear-gradient(to top, #8B5CF6, #EC4899);
            border-radius: 4px;
            position: relative;
        }
        
        .shape-1 {
            width: 20px;
            height: 50px;
            background: linear-gradient(to top, #8B5CF6, #EC4899);
        }
        
        .shape-1::after {
            content: '';
            position: absolute;
            top: 0;
            right: -8px;
            width: 12px;
            height: 15px;
            background: linear-gradient(to top, #8B5CF6, #EC4899);
            border-radius: 4px;
        }
        
        .shape-2 {
            width: 18px;
            height: 40px;
            background: linear-gradient(to top, #8B5CF6, #EC4899);
        }
        
        .shape-2::after {
            content: '';
            position: absolute;
            top: 0;
            right: -6px;
            width: 10px;
            height: 12px;
            background: linear-gradient(to top, #8B5CF6, #EC4899);
            border-radius: 4px;
        }
        
        .shape-3 {
            width: 16px;
            height: 30px;
            background: linear-gradient(to top, #8B5CF6, #EC4899);
        }
        
        .shape-3::after {
            content: '';
            position: absolute;
            bottom: -8px;
            left: 0;
            width: 8px;
            height: 10px;
            background: linear-gradient(to top, #8B5CF6, #EC4899);
            border-radius: 4px;
        }
        
        .logo-text {
            font-size: 2.5rem;
            font-weight: 800;
            color: #EC4899;
            letter-spacing: 3px;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
            font-family: 'Arial', sans-serif;
        }
        
        .hero-subtitle {
            font-size: 1.4rem;
            opacity: 0.95;
            margin-bottom: 1rem;
            font-weight: 500;
            position: relative;
            z-index: 2;
        }
        
        .hero-slogan {
            font-size: 1.1rem;
            font-style: italic;
            opacity: 0.9;
            margin-bottom: 1.5rem;
            font-weight: 400;
            position: relative;
            z-index: 2;
            color: #f0f0f0;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        }
        
        .hero-description {
            font-size: 1.1rem;
            opacity: 0.9;
            max-width: 600px;
            margin: 0 auto;
            line-height: 1.7;
            position: relative;
            z-index: 2;
        }
        
        .stats-section {
            display: flex;
            justify-content: space-between;
            gap: 1.5rem;
            margin-bottom: 3rem;
            flex-wrap: wrap;
            overflow: hidden;
        }
        
        .stat-card {
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            border-radius: 20px;
            padding: 2rem 1.5rem;
            text-align: center;
            box-shadow: 
                0 15px 35px rgba(0, 0, 0, 0.1),
                0 0 0 1px rgba(255, 255, 255, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.3);
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            position: relative;
            overflow: hidden;
            flex: 1;
            min-width: 140px;
        }
        
        .stat-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        }
        
        .stat-card::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 50%, rgba(240, 147, 251, 0.05) 100%);
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        
        .stat-card:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: 
                0 25px 50px rgba(0, 0, 0, 0.15),
                0 0 0 1px rgba(255, 255, 255, 0.3);
        }
        
        .stat-card:hover::after {
            opacity: 1;
        }
        
        .stat-icon {
            font-size: 2.5rem;
            margin-bottom: 1rem;
            display: block;
            filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
        }
        
        .stat-number {
            font-size: 2.2rem;
            font-weight: 800;
            color: #1e293b;
            margin-bottom: 0.5rem;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        .stat-label {
            color: #64748b;
            font-size: 0.95rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .agent-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin-bottom: 3rem;
            overflow: hidden;
        }
        
        .agent-card {
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            border-radius: 25px;
            padding: 2.5rem;
            box-shadow: 
                0 20px 40px rgba(0, 0, 0, 0.1),
                0 0 0 1px rgba(255, 255, 255, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.3);
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            position: relative;
            overflow: hidden;
        }
        
        .agent-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        }
        
        .agent-card::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 50%, rgba(240, 147, 251, 0.05) 100%);
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        
        .agent-card:hover {
            transform: translateY(-10px) scale(1.03);
            box-shadow: 
                0 30px 60px rgba(0, 0, 0, 0.15),
                0 0 0 1px rgba(255, 255, 255, 0.3);
        }
        
        .agent-card:hover::after {
            opacity: 1;
        }
        
        .agent-icon {
            font-size: 3rem;
            margin-bottom: 1.5rem;
            display: block;
            text-align: center;
            filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.1));
        }
        
        .agent-title {
            font-size: 1.3rem;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 1rem;
            text-align: center;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        .agent-description {
            color: #64748b;
            font-size: 1rem;
            line-height: 1.6;
            text-align: center;
            margin-bottom: 1.5rem;
        }
        
        .agent-features {
            margin-top: 1.5rem;
            padding-top: 1.5rem;
            border-top: 1px solid rgba(226, 232, 240, 0.5);
        }
        
        .agent-features ul {
            list-style: none;
            padding: 0;
            margin: 0;
        }
        
        .agent-features li {
            color: #64748b;
            font-size: 0.9rem;
            margin-bottom: 0.5rem;
            padding-left: 1.5rem;
            position: relative;
            font-weight: 500;
        }
        
        .agent-features li::before {
            content: '✓';
            position: absolute;
            left: 0;
            color: #667eea;
            font-weight: bold;
            font-size: 1rem;
        }
        
        .dashboard-section {
            display: flex;
            flex-direction: column;
            gap: 2rem;
            margin-bottom: 3rem;
            overflow: hidden;
        }
        
        .input-container {
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            border-radius: 25px;
            padding: 2.5rem;
            box-shadow: 
                0 20px 40px rgba(0, 0, 0, 0.1),
                0 0 0 1px rgba(255, 255, 255, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.3);
            position: relative;
            overflow: hidden;
        }
        
        .input-container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        }
        
        .input-title {
            font-size: 1.5rem;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 2rem;
            text-align: center;
            position: relative;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        .input-title::after {
            content: '';
            position: absolute;
            bottom: -10px;
            left: 50%;
            transform: translateX(-50%);
            width: 60px;
            height: 3px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            border-radius: 2px;
        }
        
        .gradio-textbox {
            border-radius: 15px !important;
            border: 2px solid rgba(226, 232, 240, 0.8) !important;
            transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
            background: rgba(248, 250, 252, 0.8) !important;
            margin-bottom: 1.5rem !important;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
        }
        
        .gradio-textbox:focus-within {
            border-color: #667eea !important;
            box-shadow: 
                0 0 0 4px rgba(102, 126, 234, 0.1),
                0 10px 25px rgba(102, 126, 234, 0.2) !important;
            background: rgba(255, 255, 255, 0.95) !important;
            transform: translateY(-2px) !important;
        }
        
        .gradio-textbox input, .gradio-textbox textarea {
            color: #1e293b !important;
            font-size: 1rem !important;
            padding: 1rem !important;
            font-weight: 500 !important;
        }
        
        .gradio-label {
            color: #374151 !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            margin-bottom: 0.5rem !important;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
        }
        
        .analyze-button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%) !important;
            border: none !important;
            border-radius: 30px !important;
            padding: 1.2rem 2.5rem !important;
            font-size: 1.1rem !important;
            font-weight: 700 !important;
            color: white !important;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
            box-shadow: 
                0 15px 35px rgba(102, 126, 234, 0.4),
                0 0 0 1px rgba(255, 255, 255, 0.1) !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
            width: 100% !important;
            margin-top: 1rem !important;
            position: relative;
            overflow: hidden;
        }
        
        .analyze-button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            transition: left 0.5s ease;
        }
        
        .analyze-button:hover {
            transform: translateY(-3px) scale(1.02) !important;
            box-shadow: 
                0 25px 50px rgba(102, 126, 234, 0.5),
                0 0 0 1px rgba(255, 255, 255, 0.2) !important;
        }
        
        .analyze-button:hover::before {
            left: 100%;
        }
        
        .result-container {
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            border-radius: 25px;
            padding: 2.5rem;
            box-shadow: 
                0 20px 40px rgba(0, 0, 0, 0.1),
                0 0 0 1px rgba(255, 255, 255, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.3);
            position: relative;
            overflow: hidden;
        }
        
        .result-container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        }
        
        .result-title {
            font-size: 1.5rem;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 2rem;
            text-align: center;
            position: relative;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        .result-title::after {
            content: '';
            position: absolute;
            bottom: -10px;
            left: 50%;
            transform: translateX(-50%);
            width: 60px;
            height: 3px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            border-radius: 2px;
        }
        
        .status-indicator {
            background: linear-gradient(135deg, rgba(241, 245, 249, 0.9) 0%, rgba(226, 232, 240, 0.9) 100%);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            border-radius: 15px;
            padding: 1.5rem 2rem;
            margin-bottom: 2rem;
            text-align: center;
            font-weight: 600;
            color: #64748b;
            border: 1px solid rgba(226, 232, 240, 0.5);
            position: relative;
            overflow: hidden;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
        }
        
        .status-indicator::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 50%, rgba(240, 147, 251, 0.05) 100%);
            opacity: 0.5;
        }
        
        .gradio-markdown {
            background: rgba(248, 250, 252, 0.9);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            border-radius: 15px;
            padding: 2rem;
            border: 1px solid rgba(226, 232, 240, 0.5);
            line-height: 1.7;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
        }
        
        .gradio-markdown h1, .gradio-markdown h2, .gradio-markdown h3 {
            color: #1e293b !important;
            font-weight: 700 !important;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        .gradio-markdown h1 {
            font-size: 1.8rem !important;
            margin-bottom: 1.5rem !important;
        }
        
        .gradio-markdown h2 {
            font-size: 1.5rem !important;
            margin-bottom: 1.2rem !important;
        }
        
        .gradio-markdown h3 {
            font-size: 1.3rem !important;
            margin-bottom: 1rem !important;
        }
        
        .gradio-markdown strong {
            color: #667eea !important;
            font-weight: 700 !important;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
        }
        
        .gradio-markdown ul, .gradio-markdown ol {
            padding-left: 2rem !important;
        }
        
        .gradio-markdown li {
            margin-bottom: 0.8rem !important;
            color: #374151 !important;
            font-weight: 500 !important;
        }
        
        .api-status {
            background: linear-gradient(135deg, rgba(220, 252, 231, 0.9) 0%, rgba(187, 247, 208, 0.9) 100%);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            border: 2px solid #22c55e;
            border-radius: 15px;
            padding: 1.5rem 2rem;
            margin-bottom: 2rem;
            text-align: center;
            font-weight: 600;
            color: #166534;
            position: relative;
            overflow: hidden;
            box-shadow: 0 10px 25px rgba(34, 197, 94, 0.2);
        }
        
        .api-status::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, rgba(22, 163, 74, 0.1) 100%);
            opacity: 0.5;
        }
        
        .api-status.error {
            background: linear-gradient(135deg, rgba(254, 242, 242, 0.9) 0%, rgba(254, 202, 202, 0.9) 100%);
            border-color: #ef4444;
            color: #991b1b;
            box-shadow: 0 10px 25px rgba(239, 68, 68, 0.2);
        }
        
        .api-status.error::before {
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(220, 38, 38, 0.1) 100%);
        }
        
        .footer {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.95) 0%, rgba(51, 65, 85, 0.95) 100%);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-radius: 25px;
            padding: 3rem;
            color: white;
            margin-top: 3rem;
            position: relative;
            overflow: hidden;
            box-shadow: 
                0 25px 50px rgba(0, 0, 0, 0.2),
                0 0 0 1px rgba(255, 255, 255, 0.1);
        }
        
        .footer::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: 
                radial-gradient(circle at 20% 80%, rgba(102, 126, 234, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(240, 147, 251, 0.1) 0%, transparent 50%);
        }
        
        .footer h3 {
            color: white !important;
            text-align: center;
            margin-bottom: 2rem;
            font-size: 1.5rem;
            font-weight: 700;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
            position: relative;
            z-index: 2;
        }
        
        .footer-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2.5rem;
            position: relative;
            z-index: 2;
        }
        
        .footer-section h4 {
            color: #e2e8f0;
            margin-bottom: 1.5rem;
            font-size: 1.1rem;
            font-weight: 600;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
        }
        
        .footer-section ul, .footer-section ol {
            color: #cbd5e1;
            line-height: 1.8;
        }
        
        .footer-section a {
            color: #93c5fd;
            text-decoration: none;
            transition: all 0.3s ease;
            font-weight: 500;
        }
        
        .footer-section a:hover {
            color: #60a5fa;
            text-decoration: underline;
            text-shadow: 0 0 10px rgba(96, 165, 250, 0.5);
        }
        
        .gradio-file {
            border-radius: 15px !important;
            border: 2px solid rgba(226, 232, 240, 0.8) !important;
            background: rgba(248, 250, 252, 0.8) !important;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
        }
        
        /* Dark theme uyumluluğu */
        @media (prefers-color-scheme: dark) {
            .gradio-container {
                background: linear-gradient(135deg, #1e293b 0%, #334155 50%, #475569 100%) !important;
            }
            
            .main-content {
                background: rgba(30, 41, 59, 0.95);
                color: #f1f5f9;
            }
            
            .stat-card, .agent-card, .input-container, .result-container {
                background: rgba(30, 41, 59, 0.9);
                color: #f1f5f9;
            }
            
            .stat-number, .agent-title, .input-title, .result-title {
                color: #f1f5f9 !important;
            }
            
            .stat-label, .agent-description, .gradio-label {
                color: #cbd5e1 !important;
            }
            
            .gradio-textbox {
                background: rgba(51, 65, 85, 0.8) !important;
                border-color: rgba(71, 85, 105, 0.8) !important;
            }
            
            .gradio-textbox input, .gradio-textbox textarea {
                color: #f1f5f9 !important;
            }
            
            .gradio-markdown {
                background: rgba(51, 65, 85, 0.9);
                color: #f1f5f9;
            }
            
            .gradio-markdown h1, .gradio-markdown h2, .gradio-markdown h3 {
                color: #f1f5f9 !important;
            }
            
            .gradio-markdown li {
                color: #cbd5e1 !important;
            }
        }
        
        /* Light theme için beyaz yazılar */
        @media (prefers-color-scheme: light) {
            .gradio-markdown {
                color: #ffffff !important;
            }
            
            .gradio-markdown h1, .gradio-markdown h2, .gradio-markdown h3 {
                color: #ffffff !important;
            }
            
            .gradio-markdown li {
                color: #ffffff !important;
            }
            
            .gradio-markdown strong {
                color: #ffffff !important;
            }
            
            .gradio-markdown a {
                color: #93c5fd !important;
            }
            
            .gradio-markdown a:hover {
                color: #60a5fa !important;
            }
        }
        
        @media (max-width: 768px) {
            .dashboard-section {
                grid-template-columns: 1fr;
            }
            
            .stats-section {
                flex-direction: column;
            }
            
            .stat-card {
                min-width: auto;
            }
            
            .agent-grid {
                grid-template-columns: 1fr;
            }
            
            .hero-title {
                font-size: 2.5rem;
            }
            
            .hero-subtitle {
                font-size: 1.2rem;
            }
            
            .main-content {
                margin: 1rem;
                padding: 2rem;
            }
            
            .footer-grid {
                grid-template-columns: 1fr;
            }
        }
        """
    ) as interface:
        
        # Hero Section
        gr.Markdown("""
        <div class="hero-section">
            <div class="hero-title">🚀 Infera</div>
            <div class="hero-subtitle">Yapay Zeka Tabanlı SEO Analiz Platformu</div>
            <div class="hero-slogan">"Görünmeyeni görünür kılan zeka, Infera."</div>
            <div class="hero-description">
                Gelişmiş AI agent'ları ile kapsamlı SEO analizi yapın. 
                PageSpeed, SERP, anahtar kelime ve rapor kalitesi analizlerini tek platformda birleştirin.
            </div>
        </div>
        """)
        
        # Stats Section - Tek satırda
        gr.Markdown("""
        <div class="stats-section">
            <div class="stat-card">
                <span class="stat-icon">🤖</span>
                <div class="stat-number">4</div>
                <div class="stat-label">AI Agent</div>
            </div>
            <div class="stat-card">
                <span class="stat-icon">⚡</span>
                <div class="stat-number">100%</div>
                <div class="stat-label">Otomatik</div>
            </div>
            <div class="stat-card">
                <span class="stat-icon">📊</span>
                <div class="stat-number">50+</div>
                <div class="stat-label">Metrik</div>
            </div>
            <div class="stat-card">
                <span class="stat-icon">🎯</span>
                <div class="stat-number">24/7</div>
                <div class="stat-label">Aktif</div>
            </div>
        </div>
        """)
        
        # Agent Grid
        gr.Markdown("""
        <div class="agent-grid">
            <div class="agent-card">
                <span class="agent-icon">🤖</span>
                <div class="agent-title">Technical SEO Agent</div>
                <div class="agent-description">
                    PageSpeed Insights ve SERP API analizi ile teknik SEO performansınızı ölçün
                </div>
                <div class="agent-features">
                    <ul>
                        <li>PageSpeed Skorları</li>
                        <li>SERP Sıralama Analizi</li>
                        <li>Teknik SEO Kontrolleri</li>
                    </ul>
                </div>
            </div>
            <div class="agent-card">
                <span class="agent-icon">🔍</span>
                <div class="agent-title">Keyword Control Agent</div>
                <div class="agent-description">
                    Anahtar kelime analizi ve içerik okunabilirlik kontrolü yapın
                </div>
                <div class="agent-features">
                    <ul>
                        <li>Anahtar Kelime Yoğunluğu</li>
                        <li>Okunabilirlik Skorları</li>
                        <li>İçerik Analizi</li>
                    </ul>
                </div>
            </div>
            <div class="agent-card">
                <span class="agent-icon">📊</span>
                <div class="agent-title">Report Agent</div>
                <div class="agent-description">
                    Kapsamlı ve detaylı SEO raporları oluşturun
                </div>
                <div class="agent-features">
                    <ul>
                        <li>Detaylı Analiz Raporları</li>
                        <li>Görsel Grafikler</li>
                        <li>PDF/JSON Export</li>
                    </ul>
                </div>
            </div>
            <div class="agent-card">
                <span class="agent-icon">✅</span>
                <div class="agent-title">Report Quality Agent</div>
                <div class="agent-description">
                    Rapor kalitesini kontrol edin ve doğruluğunu garanti edin
                </div>
                <div class="agent-features">
                    <ul>
                        <li>Kalite Kontrolü</li>
                        <li>Doğruluk Doğrulaması</li>
                        <li>Format Standardizasyonu</li>
                    </ul>
                </div>
            </div>
        </div>
        """)
        
        # Dashboard Section
        gr.Markdown("""
        <div class="dashboard-section">
        """)
        
        # Input Container
        gr.Markdown("""
        <div class="input-container">
            <div class="input-title">📋 Analiz Parametreleri</div>
        </div>
        """)
        
        url_input = gr.Textbox(
            label="🌐 Web Sitesi URL'si",
            placeholder="https://example.com",
            info="Analiz edilecek web sitesinin tam URL'sini girin",
            lines=1
        )
        
        keyword_input = gr.Textbox(
            label="🔍 Anahtar Kelime",
            placeholder="seo analiz",
            info="SEO analizi yapılacak anahtar kelimeyi girin",
            lines=1
        )
        
        domain_input = gr.Textbox(
            label="🏠 Domain",
            placeholder="example.com",
            info="SERP sıralaması kontrol edilecek domain'i girin",
            lines=1
        )
        
        analyze_btn = gr.Button(
            "🚀 Analizi Başlat",
            variant="primary",
            size="lg",
            elem_classes=["analyze-button"]
        )
        
        # API durumu
        api_status = gr.Markdown()
                
        # Result Container
        gr.Markdown("""
        <div class="result-container">
            <div class="result-title">📊 Analiz Sonucu</div>
        </div>
        """)
            
        # Durum göstergesi
        status_indicator = gr.Markdown(
            value="<div class='status-indicator'>🎯 Analiz için hazır! Gerekli bilgileri girin ve analizi başlatın.</div>",
            label="Durum"
        )
        
        result_output = gr.Markdown(
            label="SEO Analiz Raporu",
            value="""# 📊 SEO Analiz Raporu

## 🎯 Analiz Bekleniyor

Analiz başlatmak için gerekli bilgileri girin ve **"🚀 Analizi Başlat"** butonuna tıklayın.

### 📋 Gerekli Bilgiler:
- **🌐 Web Sitesi URL'si**: Analiz edilecek sitenin tam URL'si
- **🔍 Anahtar Kelime**: SEO analizi yapılacak anahtar kelime
- **🏠 Domain**: SERP sıralaması kontrol edilecek domain

### ⚡ Analiz Süreci:
1. **PageSpeed Analizi**: Site performansı ölçülür
2. **SERP Analizi**: Arama sıralaması kontrol edilir
3. **Anahtar Kelime Analizi**: İçerik ve yoğunluk analizi
4. **AI Raporu**: Gemini ile kapsamlı analiz

### 📈 Beklenen Sonuçlar:
- **Performans Skorları**: PageSpeed metrikleri
- **SERP Sıralaması**: Arama sonuçlarındaki pozisyon
- **Anahtar Kelime Analizi**: Yoğunluk ve optimizasyon
- **Öneriler**: İyileştirme tavsiyeleri

---
*Analiz başlatmak için yukarıdaki formu doldurun ve butona tıklayın.*"""
        )
        
        download_output = gr.File(
            label="📄 JSON Raporu İndir",
            visible=False
        )
        
        gr.Markdown("</div>")
        
        # Footer
        gr.Markdown("""
        <div class="footer">
            <h3>📝 Kullanım Talimatları</h3>
            <div class="footer-grid">
                <div class="footer-section">
                    <h4>🔧 Gerekli API Anahtarları:</h4>
                    <ul>
                        <li><strong>Gemini API</strong>: <a href="https://makersuite.google.com/app/apikey" target="_blank">https://makersuite.google.com/app/apikey</a></li>
                        <li><strong>PageSpeed API</strong>: <a href="https://console.cloud.google.com/apis/credentials" target="_blank">https://console.cloud.google.com/apis/credentials</a></li>
                        <li><strong>SerpAPI</strong>: <a href="https://serpapi.com/" target="_blank">https://serpapi.com/</a></li>
                    </ul>
                </div>
                <div class="footer-section">
                    <h4>📋 Adım Adım Kullanım:</h4>
                    <ol>
                        <li><strong>API Anahtarları</strong>: .env dosyasında gerekli API anahtarlarınızı ayarlayın</li>
                        <li><strong>URL</strong>: Analiz edilecek web sitesinin tam URL'sini girin</li>
                        <li><strong>Anahtar Kelime</strong>: SEO analizi yapılacak anahtar kelimeyi girin</li>
                        <li><strong>Domain</strong>: SERP sıralaması kontrol edilecek domain'i girin</li>
                        <li><strong>Analizi Başlat</strong>: Butona tıklayarak analizi başlatın</li>
                    </ol>
                </div>
            </div>
        </div>
        """)
        
        # Event handlers
        def check_api_status():
            keys_ok, message = check_api_keys()
            if keys_ok:
                return f"<div class='api-status'>{message}</div>"
            else:
                return f"<div class='api-status error'>{message}</div>"
        
        # API durumunu kontrol et
        interface.load(check_api_status, outputs=api_status)
        
        # Analiz butonu event'i
        analyze_btn.click(
            fn=analyze_seo,
            inputs=[url_input, keyword_input, domain_input],
            outputs=[result_output, download_output, status_indicator]
        )
        
        # Enter tuşu ile analiz başlatma
        url_input.submit(
            fn=analyze_seo,
            inputs=[url_input, keyword_input, domain_input],
            outputs=[result_output, download_output, status_indicator]
        )
        
        keyword_input.submit(
            fn=analyze_seo,
            inputs=[url_input, keyword_input, domain_input],
            outputs=[result_output, download_output, status_indicator]
        )
        
        domain_input.submit(
            fn=analyze_seo,
            inputs=[url_input, keyword_input, domain_input],
            outputs=[result_output, download_output, status_indicator]
        )
    
    return interface

# Ana fonksiyon
if __name__ == "__main__":
    # API anahtarlarını kontrol et
    keys_ok, message = check_api_keys()
    if not keys_ok:
        print(f"⚠️ Uyarı: {message}")
        print("📝 .env dosyasını oluşturun ve API anahtarlarınızı ekleyin.")
    
    # Arayüzü oluştur ve başlat
    interface = create_interface()
    interface.launch(
        server_name="0.0.0.0",
        server_port=7880,
        share=False,
        show_error=True
    ) 