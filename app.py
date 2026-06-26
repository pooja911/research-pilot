import streamlit as st
from agent import research

# Page config
st.set_page_config(
    page_title="AI Research Copilot",
    page_icon="🔬",
    layout="wide"
)

# Header
st.title("🔬 AI Research Copilot")
st.markdown("Ask any question — I'll search the web, synthesize answers, and cite my sources.")

# Input
question = st.text_input(
    "Your question:",
    placeholder="e.g. What are the latest developments in quantum computing?"
)

search_button = st.button("🔍 Research", type="primary")

if search_button and question:
    with st.spinner("Searching the web and synthesizing answer..."):
        try:
            result = research(question)

            # Confidence score
            confidence = result["confidence"]
            if confidence >= 0.7:
                confidence_color = "🟢"
                confidence_label = "High"
            elif confidence >= 0.4:
                confidence_color = "🟡"
                confidence_label = "Medium"
            else:
                confidence_color = "🔴"
                confidence_label = "Low"

            # Display confidence
            st.markdown(f"### Confidence Score: {confidence_color} {confidence_label} ({confidence})")
            st.progress(confidence)

            # Display answer
            st.markdown("### 📋 Answer")
            st.markdown(result["answer"])

            # Display sources
            st.markdown("### 📚 Sources")
            for i, source in enumerate(result["sources"]):
                with st.expander(f"Source {i+1}: {source['title']}"):
                    st.markdown(f"**URL:** [{source['url']}]({source['url']})")
                    st.markdown(f"**Relevance Score:** {source['score']}")
                    st.markdown(f"**Content:**")
                    st.markdown(source['content'])

        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")

elif search_button and not question:
    st.warning("Please enter a question first!")