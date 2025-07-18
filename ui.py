import streamlit as st
import requests

#  Page setup
st.set_page_config(
    page_title="Bangla ➜ English Translation Ranker",
    layout="centered"
)

st.title("🇧🇩 Bangla ➜ English Translation Ranker")
st.write("""
Enter your **Bengali sentence** and a **reference English translation**.  
Your backend will generate **5 diverse LLM-style paraphrases**, score them with **COMET**, rank them, and store everything locally in SQLite.
""")

#  User inputs
source_bn = st.text_area("Bengali Sentence:", height=100)
reference_en = st.text_area("Reference English:", height=80)

#  On submit
if st.button("Translate & Rank"):
    if not source_bn.strip() or not reference_en.strip():
        st.warning("Please fill in both inputs.")
        st.stop()

    with st.spinner("Translating, paraphrasing with LLM, scoring with COMET, and ranking..."):
        response = requests.post(
            "http://127.0.0.1:8000/translate_and_rank",
            json={"source_bn": source_bn, "reference_en": reference_en}
        )

    if response.status_code != 200:
        st.error(f"Error {response.status_code}: {response.text}")
        st.stop()

    data = response.json()

    #  Display Input Summary
    st.subheader("Input Summary")
    st.markdown(f"**Bengali Sentence:**\n\n```bn\n{data['source_bn']}\n```")
    st.markdown(f"**Reference English:**\n\n```en\n{data['reference_en']}\n```")

    #  Display Candidate Translations
    st.subheader("Ranked Translations")

    seen = set()
    unique_translations = []

    for item in data["translations_ranked"]:
        t = item["translation"].strip()
        if t not in seen:
            unique_translations.append(item)
            seen.add(t)

    while len(unique_translations) < 5:
        unique_translations.append({
            "translation": "[No unique translation generated]",
            "score": 0.0,
            "rank": len(unique_translations) + 1
        })

    for item in unique_translations:
        st.markdown(f"""
**Rank {item['rank']}**

> `{item['translation']}`

**COMET Score:** `{item['score']:.4f}`
""")

    st.success("Stored in your local `translations.db` database.")
    st.caption("Powered by MarianMT + LLM Paraphraser + COMET. All local, no OpenAI tokens needed.")

