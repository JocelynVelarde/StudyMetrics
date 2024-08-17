import streamlit as st

st.set_page_config(
        page_title="StudyMonitor",
        page_icon="📚",
)

st.title('Welcome to StudyMonitor 📚')

st.write('We are your best tool to monitor your students on online and in-person classes. We give you the best insights to improve your teaching experience and the ability to generate and check class content.')

st.subheader('Our Features ⭐️')

col1, col2 = st.columns(2)
col1.subheader("In Person Metrics")
col1.divider()
col1.write("- By placing a video camera on the classroom, we can monitor the students' behavior and engagement in real time.")
col1.write("- We generate live time metrics on graphics to provide insights and recommendations on what to improve.")
col1.write("- Video data is not stored anywhere to protect the students' privacy.")

col2.subheader("Generate Content")
col2.divider()
col2.write("- Generate power point presentations ready to download with a single propmt.")
col2.write("- Generate lesson plans and study guides for your classes and export them into your Google or Outlook calendar.")
col2.write("- Upload student's assesments and get insights on what might be wrong or what needs improvement.")



st.subheader("Virtual Metrics")
st.divider()
st.write("- Upload your zoom, teams or google meet recordings to get insights on your students' behavior and engagement.")
st.write("- Select the session you want to analyze and get graphics and reports.")
st.write("- You can also visualize your recorded video online while observing the metrics.")


st.divider()
st.subheader("Get Started")
st.page_link("pages/instructions.py", label="See Instructions 🚀")

st.divider()

st.markdown("<span style='margin-left: 250px; font-weight: 20px; font-size: 15px'>Thanks for using StudyMonitor 📚</span>", unsafe_allow_html=True)

