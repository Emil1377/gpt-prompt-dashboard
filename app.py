import re
import random

try:
    import streamlit as st
    streamlit_available = True
except ModuleNotFoundError:
    streamlit_available = False
    print("[Warning] 'streamlit' is not available. Streamlit UI components will not render.")

try:
    from textblob import TextBlob
    textblob_available = True
except ModuleNotFoundError:
    textblob_available = False
    print("[Warning] 'textblob' is not available. Some scoring features will be limited.")

def score_prompt(prompt):
    if textblob_available:
        clarity_score = min(10, max(1, int(TextBlob(prompt).sentiment.polarity * 10)))
    else:
        clarity_score = 5  # default fallback
    format_score = 8 if prompt.strip().endswith('?') else 6
    intent_score = 9 if 'generate' in prompt.lower() or 'create' in prompt.lower() else 5
    total_score = (clarity_score + format_score + intent_score) / 3
    return round(total_score, 2)

def categorize_prompt(prompt):
    categories = {
        'SaaS': ['app', 'software', 'startup', 'SaaS'],
        'Education': ['learn', 'teach', 'course', 'education'],
        'Lifestyle': ['habit', 'travel', 'health', 'life']
    }
    for cat, keywords in categories.items():
        if any(kw.lower() in prompt.lower() for kw in keywords):
            return cat
    return 'Other'

if streamlit_available:
    st.set_page_config(page_title="Prompt Evaluator Dashboard", layout="centered")
    st.title("🧠 GPT Prompt Evaluator Dashboard")

    prompt_input = st.text_area("Enter your GPT prompt:", height=200)

    if prompt_input:
        with st.expander("📊 Prompt Evaluation Results"):
            st.markdown("---")
            word_count = len(re.findall(r'\w+', prompt_input))
            quality = score_prompt(prompt_input)
            category = categorize_prompt(prompt_input)

            st.metric("Quality Score", f"{quality}/10")
            st.metric("Word Count", word_count)
            st.metric("Prompt Category", category)

            st.markdown("---")
            st.write("🔍 **Feedback Summary:**")
            if textblob_available:
                st.write(f"- **Clarity:** {TextBlob(prompt_input).sentiment.polarity:.2f}")
            else:
                st.write("- **Clarity:** Unavailable (TextBlob not installed)")
            st.write(f"- **Ends with question mark:** {'Yes' if prompt_input.strip().endswith('?') else 'No'}")
            st.write(f"- **Intent keyword detected:** {'Yes' if 'generate' in prompt_input.lower() or 'create' in prompt_input.lower() else 'No'}")
    else:
        st.info("Please enter a prompt above to evaluate.")
else:
    print("[Info] Running in non-UI mode. Only helper functions can be used.")
    test_prompt = "Create a SaaS app to track health habits."
    print("Prompt:", test_prompt)
    print("Score:", score_prompt(test_prompt))
    print("Category:", categorize_prompt(test_prompt))
