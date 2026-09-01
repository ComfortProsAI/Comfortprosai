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

# Initialize chat history in session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your Comfort Pros AI assistant. What would you like to build, write, or manage today?"}
    ]

# Main Interface Tabs
tab1, tab2, tab3 = st.tabs(["💬 Chat & Marketing AI", "📊 Location Data", "🛠️ Quick Actions"])

with tab1:
    st.subheader("Comfort Pros Executive Assistant")
    
    # Display historical chat messages in bubbles
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input box pinned at the bottom of the tab/screen
    if prompt := st.chat_input("Ask Gemini anything about marketing, operations, or reviews..."):
        if not api_key:
            st.error("Please configure your Gemini API key in Streamlit Secrets or the sidebar!")
        else:
            # Append user message to history and display it
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Generate Gemini response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        client = genai.Client(api_key=api_key)
                        
                        # Format history for Gemini or pass prompt with system context
                        system_instruction = "You are the internal operations and marketing AI for Comfort Pros, an HVAC contractor operating in Arizona (Gilbert/Phoenix metro) and California. Keep answers practical, direct, and focused on growing and running an HVAC business."
                        
                        full_prompt = f"{system_instruction}\n\nUser Request: {prompt}"
                        
                        response = client.models.generate_content(
                            model="gemini-3.6-flash",
                            contents=full_prompt,
                        )
                        answer = response.text
                        st.markdown(answer)
                        
                        # Append assistant response to history
                        st.session_state.messages.append({"role": "assistant", "content": answer})
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
