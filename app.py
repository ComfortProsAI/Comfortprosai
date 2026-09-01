import streamlit as st
from google import genai
from authlib.integrations.requests_client import OAuth2Session

# Page Config
st.set_page_config(page_title="Comfort Pros Command Center", page_icon="❄️", layout="wide")

st.title("❄️ Comfort Pros Command Center")
st.markdown("Your live operational command hub for Arizona & California.")

# Load API keys from Streamlit secrets
api_key = st.secrets.get("GEMINI_API_KEY", "")
google_client_id = st.secrets.get("GOOGLE_CLIENT_ID", "")
google_client_secret = st.secrets.get("GOOGLE_CLIENT_SECRET", "")

if not api_key:
    api_key = st.sidebar.text_input("Gemini API Key", type="password")

# Main Interface Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "💬 Chat & Marketing AI", 
    "⭐ Review & GBP Manager", 
    "🔌 Live Google Sync", 
    "📊 Location Data", 
    "🛠️ Quick Actions"
])

with tab1:
    st.subheader("Comfort Pros Executive Assistant")
    
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm ready to help manage operations, marketing, and reviews."}
        ]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask Gemini anything..."):
        if not api_key:
            st.error("Please configure your Gemini API key!")
        else:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        client = genai.Client(api_key=api_key)
                        system_instruction = "You are the internal operations and marketing AI for Comfort Pros, an HVAC contractor operating in Arizona (Gilbert/Phoenix metro) and California."
                        response = client.models.generate_content(
                            model="gemini-3.6-flash",
                            contents=f"{system_instruction}\n\nUser Request: {prompt}",
                        )
                        answer = response.text
                        st.markdown(answer)
                        st.session_state.messages.append({"role": "assistant", "content": answer})
                    except Exception as e:
                        st.error(f"Error: {e}")

with tab2:
    st.subheader("AI Review & Content Generator")
    manager_mode = st.radio("Select Action:", ["Draft Review Reply", "Dispute / Appeal Fake Review", "Optimize GBP Post"])
    
    if manager_mode == "Draft Review Reply":
        rating = st.selectbox("Star Rating", ["5 Stars", "4 Stars", "3 Stars", "2 Stars", "1 Star"])
        review_text = st.text_area("Paste Customer Review:")
        if st.button("Generate Reply"):
            if api_key and review_text:
                client = genai.Client(api_key=api_key)
                res = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=f"Write a professional response to this {rating} review for Comfort Pros HVAC in Arizona. Review: {review_text}"
                )
                st.write(res.text)

    elif manager_mode == "Dispute / Appeal Fake Review":
        fake_review = st.text_area("Paste Spam/Fake Review Text:")
        if st.button("Generate Google Support Appeal"):
            if api_key and fake_review:
                client = genai.Client(api_key=api_key)
                res = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=f"Write a strict Google Business Profile support appeal justification to remove this fake/spam review: {fake_review}"
                )
                st.write(res.text)

    elif manager_mode == "Optimize GBP Post":
        topic = st.text_input("Post Topic (e.g., Summer AC Checkup Special):")
        if st.button("Generate Post"):
            if api_key and topic:
                client = genai.Client(api_key=api_key)
                res = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=f"Write an engaging Google Business Profile post for Comfort Pros about: {topic}"
                )
                st.write(res.text)

with tab3:
    st.subheader("🔌 Live Google Business Profile Connector")
    
    if not google_client_id or not google_client_secret:
        st.warning("Google OAuth credentials are missing from Streamlit Secrets.")
        st.markdown("""
        **To finish the live setup:**
        Ensure your `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` are added to your Streamlit Cloud **Secrets** panel.
        """)
    else:
        # OAuth configuration endpoints
        authorization_endpoint = "https://accounts.google.com/o/oauth2/v2/auth"
        token_endpoint = "https://oauth2.googleapis.com/token"
        
        # Detect app URL dynamically or use standard flow
        redirect_uri = "https://share.streamlit.io" # Automatically handled when deployed
        
        if "oauth_token" not in st.session_state:
            st.session_state.oauth_token = None

        if not st.session_state.oauth_token:
            st.write("Click below to authorize your command center to access Comfort Pros listing data:")
            
            # Construct Google OAuth login link
            scope = "https://www.googleapis.com/auth/business.manage"
            auth_url = (
                f"{authorization_endpoint}?response_type=code&client_id={google_client_id}"
                f"&redirect_uri={redirect_uri}&scope={scope}&access_type=offline&prompt=consent"
            )
            st.markdown(f'<a href="{auth_url}" target="_self"><button style="background-color:#4285F4; color:white; padding:10px 20px; border:none; border-radius:4px; cursor:pointer;">Sign In with Google Business Profile</button></a>', unsafe_allow_html=True)
        else:
            st.success("Successfully Connected to Google Business Profile API!")
            if st.button("Fetch Live Account Locations"):
                st.write("Querying Google Business Profile endpoints for Comfort Pros...")

with tab4:
    st.subheader("Business Locations & Analytics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Arizona Office (Gilbert)", value="Active", delta="ROC #364742")
    with col2:
        st.metric(label="California Operations", value="Active", delta="Ready")

with tab5:
    st.subheader("Action Center")
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
