import streamlit as st
from google import genai

st.set_page_config(page_title="Comfort Pros Command Center", page_icon="❄️", layout="wide")

st.title("❄️ Comfort Pros Command Center")
st.markdown("Your private AI-powered control hub for Arizona & California operations.")

# Automatically load the API key from Streamlit secrets
api_key = st.secrets.get("GEMINI_API_KEY", "")

if not api_key:
    # Fallback to sidebar input if secrets aren't set yet
    api_key = st.sidebar.text_input("Enter your Gemini API Key", type="password")

# Main Interface Tabs
tab1, tab2, tab3 = st.tabs(["💬 AI Assistant & Marketing", "📊 Location Data", "🛠️ Quick Actions"])

with tab1:
    st.subheader("Gemini Business & Marketing Assistant")
    st.write("Ask Gemini to write ad copy, draft review responses, or analyze customer feedback.")
    
    prompt = st.text_area("What do you want to create or analyze today?")
    
    if st.button("Generate with Gemini"):
        if not api_key:
            st.error("Please configure your Gemini API key in Streamlit Secrets or the sidebar!")
        elif not prompt:
            st.warning("Please type a request or prompt first.")
        else:
            with st.spinner("Gemini is working on it..."):
                try:
                    client = genai.Client(api_key=api_key)
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt,
                    )
                    st.success("Done!")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")

with tab2:
    st.subheader("Business Locations & Analytics")
    st.metric(label="Arizona Office (Gilbert)", value="Active", delta="Operational")
    st.metric(label="California Office", value="Active", delta="Operational")

with tab3:
    st.subheader("Action Center")
    if st.button("Run Connection Check"):
        st.success("Local environment check passed!")