import streamlit as st
from openai import OpenAI
from datetime import date

# ১. পেজ সেটআপ ও ব্র্যান্ডিং
st.set_page_config(
    page_title="CodeForge AI - Elite Coding Engine",
    page_icon="⚡",
    layout="wide"
)

# প্রিমিয়াম ডার্ক থিম সিএসএস
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    .limit-badge {
        background: #161b22;
        border: 1px solid #30363d;
        padding: 12px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ২. সিক্রেট থেকে API Key লোড করা
API_KEY = st.secrets.get("GROQ_API_KEY", "")

# ৩. প্রম্পট লিমিট ট্র্যাকিং (প্রতিদিন ১৫টি ফ্রি)
DAILY_FREE_LIMIT = 15
today = str(date.today())

if "last_date" not in st.session_state or st.session_state.last_date != today:
    st.session_state.last_date = today
    st.session_state.usage_count = 0

if "is_pro" not in st.session_state:
    st.session_state.is_pro = False

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ৪. সাইডবার (বিজনেস ও পেমেন্ট সেকশন)
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=60)
    st.title("⚡ CodeForge AI")
    st.caption("Next-Gen Software Engineering Partner")
    st.markdown("---")
    
    remaining = DAILY_FREE_LIMIT - st.session_state.usage_count
    if not st.session_state.is_pro:
        st.markdown(f"""
        <div class="limit-badge">
            <span style="color:#58a6ff; font-weight:bold;">🎁 ডেইলি ফ্রি কোটা:</span><br>
            <h2 style="margin:5px 0; color:#fff;">{remaining} / {DAILY_FREE_LIMIT}</h2>
            <small style="color:#8b949e;">প্রতিদিন রাত ১২টায় রিসেট হবে</small>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.success("🌟 আপনি একজন VIP PRO মেম্বার! আনলিমিটেড পাওয়ার সক্রিয়।")

    st.markdown("### 👑 Get CodeForge PRO")
    st.markdown("""
    - 🚀 **আনলিমিটেড** কোড জেনারেশন
    - 🧠 **High-Logic Pro** ফুলস্ট্যাক মোড
    - 🐞 ইনস্ট্যান্ট বাগ সলভার ও প্রজেক্ট ক্রিয়েটর
    """)
    st.info("💳 মাত্র ২৯৯ টাকা / মাস")
    
    with st.expander("📲 বিকাশ / নগদ দিয়ে অ্যাক্টিভ করুন"):
        st.write("**bKash / Nagad:** `01XXXXXXXXX` (Personal)")
        st.caption("Send Money করে TrxID নিচে দিন:")
        trx = st.text_input("Transaction ID (TrxID)")
        if st.button("ভেরিফাই ও আনলক"):
            if len(trx.strip()) >= 6:
                st.session_state.is_pro = True
                st.success("অভিনন্দন! আপনার PRO মেম্বারশিপ সক্রিয় হয়েছে! 🎉")
                st.rerun()
            else:
                st.error("সঠিক TrxID প্রদান করুন!")

# ৫. মূল চ্যাট স্ক্রিন
st.title("💻 CodeForge AI: The World-Class Coding Assistant")
st.write("যে কোনো জটিল কোড, অ্যালগরিদম, বাগ ফিক্স বা প্রজেক্ট তৈরি করতে নির্দেশ দিন।")

# চ্যাট হিস্ট্রি প্রদর্শন
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ইনপুট হ্যান্ডলার
if user_input := st.chat_input("কোড লিখতে বলুন বা আপনার সমস্যাটি জানান..."):
    if not st.session_state.is_pro and st.session_state.usage_count >= DAILY_FREE_LIMIT:
        st.error("⚠️ আপনার আজকের ১৫টি ফ্রি রিকোয়েস্ট শেষ! আনলিমিটেড ব্যবহার করতে সাইডবার থেকে PRO তে আপগ্রেড করুন।")
    else:
        st.session_state.usage_count += 1
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Groq Client
        client = OpenAI(
            api_key=API_KEY, 
            base_url="https://api.groq.com/openai/v1"
        )
        
        system_prompt = (
            "You are CodeForge AI, an expert software developer and technical assistant. "
            "Write high quality, bug-free, clean code with explanations. "
            "Help with all programming tasks accurately. Speak Bangla or English."
        )

        with st.chat_message("assistant"):
            with st.spinner("⚡ CodeForge কোড তৈরি করছে..."):
                # ১০০% কাজ করবে এমন স্ট্যাবল মডেল
                try:
                    response = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            *[{"role": m["role"], "content": m["content"]} for m in st.session_state.chat_history]
                        ],
                        temperature=0.3
                    )
                    reply = response.choices[0].message.content
                    st.markdown(reply)
                    st.session_state.chat_history.append({"role": "assistant", "content": reply})
                except Exception as e:
                    st.error(f"সার্ভার কানেকশন ত্রুটি: {e}")
