import streamlit as st

st.set_page_config(
        page_title="StudyMonitor",
        page_icon="📚",
)

st.title('Welcome to StudyMonitor 📚')

st.write('Some random content in here')

st.subheader('We have three main infrastructure features:')

col1, col2 = st.columns(2)
col1.subheader("In Person Metrics")
col1.divider()
col1.write("- ADD CONTENT HERE")

col2.subheader("Generate Content")
col2.divider()
col2.write("- ADD CONTENT HERE")

col3, col4 = st.columns(2)
col3.subheader("Virtual Metrics")
col3.divider()
col3.write("- ADD CONTENT HERE")

col4.image("assets/images/study.png", use_column_width=True)

st.divider()
st.subheader("We combine the use of several tools to make your teaching experience easier")


st.divider()
st.subheader("Get Started")
st.page_link("pages/instructions.py", label="See Instructions 🚀")

st.divider()

st.markdown("<span style='margin-left: 250px; font-weight: 20px; font-size: 15px'>Thanks for using StudyMonitor 📚</span>", unsafe_allow_html=True)

