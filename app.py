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

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your Comfort Pros AI assistant. Ready to manage reviews, local SEO, or marketing."}
    ]

# Main Interface Tabs
tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat & Marketing AI", "⭐ Review & GBP Manager", "📊 Location Data", "🛠️ Quick Actions"])

with tab1:
    st.subheader("Comfort Pros Executive Assistant")
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask Gemini anything about marketing, operations, or reviews..."):
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
                        system_instruction = "You are the internal operations and marketing AI for Comfort Pros, an HVAC contractor operating in Arizona (Gilbert/Phoenix metro) and California. Keep answers practical, direct, and focused on growing and running an HVAC business."
                        full_prompt = f"{system_instruction}\n\nUser Request: {prompt}"
                        
                        response = client.models.generate_content(
                            model="gemini-3.6-flash",
                            contents=full_prompt,
                        )
                        answer = response.text
                        st.markdown(answer)
                        st.session_state.messages.append({"role": "assistant", "content": answer})
                    except Exception as e:
                        st.error(f"Error: {e}")

with tab2:
    st.subheader("Google Business Profile & Review Manager")
    st.write("Use Gemini to instantly draft review replies, write dispute appeals for fake reviews, or optimize your listing text.")
    
    manager_mode = st.radio("Select Action:", ["Draft Review Reply", "Dispute / Appeal Fake Review", "Optimize GBP Post / Description"])
    
    if manager_mode == "Draft Review Reply":
        rating = st.selectbox("Star Rating", ["5 Stars", "4 Stars", "3 Stars", "2 Stars", "1 Star"])
        review_text = st.text_area("Paste Customer Review Here:")
        if st.button("Generate Professional Reply"):
            if not api_key or not review_text:
                st.warning("Please provide your API key and the review text.")
            else:
                client = genai.Client(api_key=api_key)
                res = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=f"You are the owner of Comfort Pros HVAC. Write a professional, polite, and SEO-friendly response to this {rating} review. Mention our commitment to quality service in the Phoenix/East Valley area. Review: {review_text}"
                )
                st.markdown("### Suggested Reply:")
                st.write(res.text)

    elif manager_mode == "Dispute / Appeal Fake Review":
        fake_review_text = st.text_area("Paste the spam/unfair review text:")
        violation_reason = st.text_selectbox if hasattr(st, 'text_selectbox') else st.selectbox(
            "Primary Violation Type", 
            ["Not a genuine customer / Conflict of interest", "Spam / Advertising", "Harassment / Profanity", "Off-topic content"]
        )
        if st.button("Generate Google Support Dispute Justification"):
            if not api_key or not fake_review_text:
                st.warning("Please provide your API key and the review text.")
            else:
                client = genai.Client(api_key=api_key)
                res = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=f"Write a concise, strict dispute justification for Google Business Profile support to remove a fake review. Ground the appeal strictly in Google's terms of service regarding '{violation_reason}'. Review text: {fake_review_text}"
                )
                st.markdown("### Dispute Appeal Argument for Google Support:")
                st.write(res.text)

    elif manager_mode == "Optimize GBP Post / Description":
        post_topic = st.text_input("Enter Post Topic / Offer (e.g., Spring AC Tune-Up Special in Gilbert):")
        if st.button("Generate Google Post"):
            if not api_key or not post_topic:
                st.warning("Please enter a post topic.")
            else:
                client = genai.Client(api_key=api_key)
                res = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=f"Write an engaging Google Business Profile post for Comfort Pros HVAC about: {post_topic}. Keep it punchy, compliant with guidelines (no keyword stuffing, no markdown issues), and include a clear call-to-action."
                )
                st.markdown("### Generated Post:")
                st.write(res.text)

with tab3:
    st.subheader("Business Locations & Analytics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Arizona Office (Gilbert)", value="Active", delta="ROC #364742")
    with col2:
        st.metric(label="California Operations", value="Active", delta="Ready")

with tab4:
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
