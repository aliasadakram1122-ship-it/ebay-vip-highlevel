import streamlit as st
import google.generativeai as genai
import re
import urllib.parse

# ہائی لیول پیج کنفیگریشن
st.set_page_config(page_title="Asad Official - VIP eBay Generator", page_icon="👑", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stButton>button {
        background: linear-gradient(90deg, #1e3a8a, #0284c7);
        color: white; font-weight: bold; border-radius: 12px;
        padding: 12px 28px; border: none; transition: all 0.3s;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(2, 132, 199, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

st.header("👑 Asad Official | Enterprise eBay Listing Generator")
st.caption("ایک پروفیشنل اور ہائی اینڈ پلیٹ فارم جو بغیر کسی رکاوٹ کے پریمیم HTML کوڈ تیار کرتا ہے۔")

# سیکیور طریقے سے API Key مانگنا (سب سے بہترین اور ایرر فری طریقہ)
api_key = st.text_input("🔑 Enter your Google AI Studio API Key:", type="password", help="اپنی نئی API Key یہاں پیسٹ کریں")

# کیٹیگری تھیم سلیکشن
theme_option = st.selectbox("🎯 Select Premium Category Theme:", [
    "Automotive / Hardware", "Art & Craft / Tools", "Skin Care / Beauty", 
    "Medical / Pharmacy", "Pet Care", "Garden / Organic", "Hygiene / Household"
])

theme_colors = {
    "Automotive / Hardware": {"brand": "#1e40af", "accent": "#94a3b8", "black": "#0f172a", "soft": "#f8fafc"},
    "Art & Craft / Tools": {"brand": "#7c2d12", "accent": "#f59e0b", "black": "#0f172a", "soft": "#fffbeb"},
    "Skin Care / Beauty": {"brand": "#9f1239", "accent": "#fcd34d", "black": "#4c0519", "soft": "#fff1f2"},
    "Medical / Pharmacy": {"brand": "#991b1b", "accent": "#fbbf24", "black": "#450a0a", "soft": "#fef2f2"},
    "Pet Care": {"brand": "#4c1d95", "accent": "#f59e0b", "black": "#2e1065", "soft": "#f5f3ff"},
    "Garden / Organic": {"brand": "#166534", "accent": "#84cc16", "black": "#052e16", "soft": "#f7fee7"},
    "Hygiene / Household": {"brand": "#14532d", "accent": "#4ade80", "black": "#052e16", "soft": "#f0fdf4"}
}
selected_colors = theme_colors[theme_option]

product_url = st.text_input("🔗 Paste Amazon Product URL here (Smart Extractor):")
product_data_to_process = ""

if product_url:
    match = re.search(r'amazon\.[a-z\.]+/(.*?)/dp/', product_url)
    if match:
        extracted_name = urllib.parse.unquote(match.group(1).replace('-', ' '))
        st.success(f"✅ Product Identified via URL: **{extracted_name}**")
        product_data_to_process = extracted_name
    else:
        st.warning("⚠️ لنک ریڈ نہیں ہو سکا۔ پروڈکٹ کا نام نیچے خود ٹائپ کریں:")

product_manual = st.text_input("📝 Or Type Product Name / Details Manually:")
if product_manual:
    product_data_to_process = product_manual

if st.button("✨ Generate Enterprise Listing Code"):
    if not api_key:
        st.error("❌ برائے مہربانی اپنی API Key باکس میں درج کریں۔")
    elif not product_data_to_process:
        st.error("❌ برائے مہربانی ایمیزون لنک یا پروڈکٹ کی تفصیلات فراہم کریں۔")
    else:
        with st.spinner("💎 ہائی لیول ڈیٹا پروسیسنگ اور ٹیمپلیٹ رینڈرنگ جاری ہے..."):
            try:
                genai.configure(api_key=api_key)
                
                # آٹو ماڈل سلیکشن - جو بھی گوگل کا ایکٹو ماڈل ہوگا، یہ خود اٹھا لے گا
                models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                if not models:
                    raise Exception("کوئی بھی سپورٹڈ AI ماڈل دستیاب نہیں ہے۔")
                
                # جدید ترین ماڈل کا استعمال
                chosen_model = [m for m in models if '1.5' in m] or models
                model = genai.GenerativeModel(chosen_model[0] if isinstance(chosen_model, list) else chosen_model)
                
                prompt = f"""
                You are a premium enterprise product copywriter for eBay. 
                Product/Details: "{product_data_to_process}".
                Generate a conversion-optimized eBay listing description using exactly this HTML structure (.hero-section, .product-intro, .grid-layout, .info-terminal, .usage-box, .trust-bar) and these CSS variables:
                --brand-color: {selected_colors['brand']};
                --accent-glow: {selected_colors['accent']};
                --premium-black: {selected_colors['black']};
                --soft-bg: {selected_colors['soft']};
                Return ONLY pure HTML code without markdown tags.
                """
                
                response = model.generate_content(prompt)
                clean_html = re.sub(r'^```html\s*|```$', '', response.text, flags=re.MULTILINE).strip()
                
                st.success("🎉 آپ کی پروفیشنل لسٹنگ کامیابی سے تیار ہو گئی ہے!")
                
                tab1, tab2 = st.tabs(["👀 Live Preview", "💻 Raw HTML Code"])
                with tab1:
                    st.components.v1.html(clean_html, height=1200, scrolling=True)
                with tab2:
                    st.text_area("کاپی کریں کوڈ یہاں سے:", value=clean_html, height=500)
                    st.download_button("📥 Download Enterprise HTML", data=clean_html, file_name="enterprise_listing.html", mime="text/html")

            except Exception as e:
                st.error(f"❌ سسٹم ایرر: {str(e)}")
