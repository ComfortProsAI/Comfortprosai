import streamlit as st
from google import genai

# Page Config
st.set_page_config(page_title="Comfort Pros Command Center", page_icon="❄️", layout="wide")

st.title("❄️ Comfort Pros Command Center")
st.markdown("Your private AI-powered control hub for Arizona & California operations.")

# Load API key from Streamlit secrets or sidebar fallback
api_key = st.secrets.get("GEMINI_API_KEY", "")
if not api_key:
    api_key = st.sidebar.text_input("Gemini API Key", type="password")

# Main Interface Tabs
tab1, tab2, tab3 = st.tabs(["💬 Marketing & Operations AI", "📊 Location Data", "🛠️ Quick Actions"])

with tab1:
    st.subheader("Comfort Pros Executive Assistant")
    st.write("Tell Gemini what you want to execute (e.g., *'Write a Google post for a 15% off spring tune-up in Gilbert'* or *'Draft a response to a 5-star review'*).")
    
    prompt = st.text_area("What do you want to build, write, or solve today?", height=100)
    
    if st.button("Execute with Gemini", type="primary"):
        if not api_key:
            st.error("Please configure your Gemini API key!")
        elif not prompt:
            st.warning("Please type a request first.")
        else:
            with st.spinner("Comfort Pros AI is working..."):
                try:
                    client = genai.Client(api_key=api_key)
                    # System instruction forces Gemini to act specifically as your business partner
                    response = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=f"You are the internal operations and marketing AI for Comfort Pros, an HVAC contractor operating in Arizona (Gilbert/Phoenix metro) and California. Keep answers practical, direct, and focused on growing and running an HVAC business. Here is the request: {prompt}",
                    )
                    st.success("Done!")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")

with tab2:
    st.subheader("Business Locations & Analytics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Arizona Office (Gilbert)", value="Active", delta="ROC #364742")
    with col2:
        st.metric(label="California Operations", value="Active", delta="Ready")

with tab3:
    st.subheader("Action Center")
    st.write("Trigger tools, copy local listing guidelines, or generate structured schema.")
    if st.button("Generate Local Schema Markup"):
        st.code("""
{
  "@context": "https://schema.org",
  "@type": "HVACBusiness",
  "name": "Comfort Pros",
  "telephone": "+1-XXXXXXXXXX",
  "url": "https://comfortprosaz.com",
  "areaServed": ["Gilbert", "Phoenix", "Mesa", "Chandler", "Scottsdale"]
}
        """, language="json")
