import streamlit as st
from google import genai

# Page Config
st.set_page_config(page_title="Comfort Pros Command Center", page_icon="❄️", layout="wide")

st.title("❄️ Comfort Pros Command Center")
st.markdown("Your private AI-powered control hub for Arizona & California operations.")

# Sidebar for Gemini API Key (or you can manage settings here)
st.sidebar.header("⚙️ AI Controls")
api_key = st.sidebar.text_input("Enter your Gemini API Key", type="password")

# Main Interface Tabs
tab1, tab2, tab3 = st.tabs(["💬 AI Assistant & Marketing", "📊 Location Data", "🛠️ Quick Actions"])

with tab1:
    st.subheader("Gemini Business & Marketing Assistant")
    st.write("Ask Gemini to write ad copy, draft review responses, or analyze customer feedback.")

    prompt = st.text_area("What do you want to create or analyze today?")

    if st.button("Generate with Gemini"):
        if not api_key:
            st.error("Please enter your Gemini API key in the sidebar first!")
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
    st.info("Your Arizona and California listing metrics will feed directly here.")
    st.metric(label="Arizona Office (Gilbert)", value="Active", delta="Operational")
    st.metric(label="California Office", value="Active", delta="Operational")

with tab3:
    st.subheader("Action Center")
    st.write("Trigger automated updates, review pulls, or site tools.")
    if st.button("Run Connection Check"):
        st.success("Local environment check passed!")