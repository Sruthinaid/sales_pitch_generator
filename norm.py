import streamlit as st
import requests
import google.generativeai as genai

# Configure API Key
GEMINI_API_KEY = "AIzaSyACCSRB3GW4BdLqBT9yPjdcTDkE-idPqJA"
genai.configure(api_key=GEMINI_API_KEY)

@st.cache_data
def load_products():
    url = "https://dummyjson.com/products"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()["products"]

products = load_products()

# Centered and larger header with icons
st.markdown(
    """
    <h1 style="text-align:center; font-size: 2.5em;">
             💼 Sales Pitch Generator 💡
    </h1>
    """,
    unsafe_allow_html=True
)

product_titles = [p["title"] for p in products]
selected_product = st.selectbox("🛍 Select a product:", product_titles)
company = st.text_input("🏢 Enter company name:")
audience = st.text_input("🎯 Enter target audience:")
tone = st.selectbox("🎨 Select pitch tone:", ["Professional", "Friendly", "Funny", "Luxury", "Bold", "Inspirational"])

if st.button("✨ Generate Pitch"):
    if not company or not audience:
        st.warning("⚠️ Please fill in all fields.")
    else:
        product = next(p for p in products if p["title"] == selected_product)
        
        prompt = f"""
        Write a short, catchy sales pitch in a {tone.lower()} tone for this product.
        Company: {company}
        Product: {product['title']}
        Target Audience: {audience}
        Description: {product['description']}
        Make it persuasive and under 50 words.
        """
        
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        st.write(response.text) 
