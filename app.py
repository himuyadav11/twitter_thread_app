import streamlit as st
from groq import Groq
import os
client = Groq(api_key=os.environ["GROQ_API_KEY"])

st.set_page_config(page_title="Twitter/X Thread Ghostwriter", layout="centered")

st.markdown("""
<style>
body {
    background-color: #f5f8fa;
}

.twitter-card {
    background-color: white;
    padding: 16px;
    border-radius: 12px;
    border: 1px solid #e1e8ed;
    margin-bottom: 12px;
    font-family: Arial, sans-serif;
}

.tweet {
    border-bottom: 1px solid #e1e8ed;
    padding: 12px 0;
}

.tweet:last-child {
    border-bottom: none;
}

.tweet-header {
    font-weight: bold;
    font-size: 14px;
}

.tweet-handle {
    color: #657786;
    font-weight: normal;
    margin-left: 6px;
}

.tweet-text {
    font-size: 15px;
    margin-top: 6px;
}

.tweet-actions {
    color: #657786;
    font-size: 13px;
    margin-top: 8px;
}
</style>
""", unsafe_allow_html=True)

def render_twitter_thread(thread_text):
    tweets = [t.strip() for t in thread_text.split("\n") if t.strip().startswith(tuple("123456789"))]

    html = '<div class="twitter-card">'
    html += '<div class="tweet-header">ThreadGhost ✨ <span class="tweet-handle">@threadghost</span>

    for tweet in tweets:
        html += f'''
        <div class="tweet">
            <div class="tweet-text">{tweet}</div>
            <div class="tweet-actions">💬  🔁  ❤️  📤</div>
        </div>
        '''

    html += '</div>'
    return html


st.title("🧵 Twitter/X Thread Ghostwriter")
st.write("Generate a Twitter/X thread using GenAI.")

topic = st.text_input("Enter topic for the thread")
audience = st.selectbox(
    "Target audience",
    ["General public", "Students", "Professionals", "Founders"]
)
n_tweets = st.slider("Number of tweets", 3, 7, 5)
style = st.selectbox(
    "Select writing style",
    ["Viral", "Educational", "Professional"]
)

generate = st.button("Generate Thread")

SYSTEM_PROMPT = """
You are a professional Twitter/X thread ghostwriter.

Your task is to write high-quality Twitter threads that are:
- Clear, engaging, and coherent
- Structured as a numbered thread
- Each tweet must be under 280 characters
- Written in natural, human-like language
- Free from emojis unless explicitly requested
- Avoid hashtags unless explicitly requested

General rules:
- Tweet 1 must be a strong hook
- Middle tweets must logically develop the idea
- Final tweet must summarize or provide a takeaway
- Do NOT mention that you are an AI
"""

STYLE_PROMPTS = {
    "Viral": """
Write in a viral, attention-grabbing style.
- Use curiosity gaps and bold statements
- Short, punchy sentences
- Emotional but not misleading
""",
    "Educational": """
Write in an educational, explanatory style.
- Neutral and informative tone
- Explain concepts step-by-step
- Focus on clarity over virality
""",
    "Professional": """
Write in a professional, thought-leadership style.
- Calm, credible, and reflective
- Avoid hype or clickbait
- Emphasize insight and nuance
"""
}

if generate:

    if topic.strip() == "":
        st.warning("Please enter a topic.")

    else:
        prompt = f"""
Writing style:
{STYLE_PROMPTS[style]}
Topic: {topic}
Target audience: {audience}
Thread length: {n_tweets} tweets
Instructions:
- Number each tweet clearly (1/{n_tweets}, 2/{n_tweets}, etc.)
- Keep tone consistent throughout

Write the Twitter thread now:
"""

        with st.spinner("Generating thread..."):
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=700
            )

            output = completion.choices[0].message.content

            st.subheader("Generated Thread (Preview)")
            st.markdown(render_twitter_thread(output), unsafe_allow_html=True)



st.caption("Preview only. This does not post to Twitter/X.")



