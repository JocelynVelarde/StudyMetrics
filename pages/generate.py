import streamlit as st
import base64
from algorithms.pptx_genai import generate_slide_titles, generate_slide_content, create_presentation
from algorithms.simple_text import ask_chat

st.set_page_config(
        page_title="StudyMonitor",
        page_icon="📚",
)

submit = False
submit_photo = False

st.title('Create a Study Plan with EduVision')

st.divider()

st.subheader(':green[Fill out the fields to start generating]')

with st.form("Study Plan Form"):
   select_course = st.selectbox(
       "Select course", ["Math", "Science", "English"])
   select_course_level = st.selectbox(
       "Select course level", ["Elementary", "High School", "College"])
   select_duration_course = st.selectbox("Select duration of course", [
                                         "1 month", "2 months", "3 months"])
   select_hours_per_day = st.selectbox(
       "Select time per class", ["40 minutes", "1 hour", "2 hours", "3 hours"])
    

   
   submitted = st.form_submit_button("Generate")

   if submitted:
      submit = True
      st.warning("Generating study plan...")
      st.write(ask_chat(select_course, select_course_level, select_duration_course, select_hours_per_day))


st.divider()

def get_ppt_download_link(ppt_filename):
    with open(ppt_filename, "rb") as file:
        ppt_contents = file.read()
    b64_ppt = base64.b64encode(ppt_contents).decode()
    return f'<a href="data:application/vnd.openxmlformats-officedocument.presentationml.presentation;base64,{b64_ppt}" download="{ppt_filename}">Download the PowerPoint Presentation</a>'

st.divider()
st.subheader(':orange[Type a content topic to start generating a PPT]')

with st.form("Study Plan Text Form"):
    topic = st.text_input("Enter the topic for your presentation:")
    generate_button = st.form_submit_button("Generate Presentation")

    if generate_button and topic:
        with st.spinner("Generating presentation... Please wait."):
            slide_titles = generate_slide_titles(topic)
            slide_contents = [generate_slide_content(title) for title in slide_titles]
            ppt_filename = create_presentation(topic, slide_titles, slide_contents)

        st.success("Presentation generated successfully!")

        # Provide a download link for the generated PowerPoint presentation
        st.markdown(get_ppt_download_link(ppt_filename), unsafe_allow_html=True)