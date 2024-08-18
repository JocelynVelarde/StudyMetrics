import streamlit as st
import base64
from algorithms.pptx_genai import generate_slide_titles, generate_slide_content, create_presentation
from algorithms.simple_text import ask_chat, generate_ics_file
from PyPDF2 import PdfReader
import openai as oclient

st.set_page_config(
        page_title="StudyMonitor",
        page_icon="📚",
)

submit = False
submit_photo = False

st.title('Generate, Check and Schedule your classes 📚')

st.divider()

st.subheader('Fill out the fields to start generating')

with st.form("Study Plan Form"):
   select_course = st.selectbox(
       "Select course", ["Math", "Science", "English"])
   select_course_level = st.selectbox(
       "Select course level", ["Elementary", "High School", "College"])
   select_duration_course = st.selectbox("Select duration of course", [
                                         "1 month", "2 months", "3 months"])
   select_hours_per_day = st.selectbox(
       "Select time per class", ["40 minutes", "1 hour", "2 hours", "3 hours"])
   start_date = st.date_input("Start Date")
    

   
   submitted = st.form_submit_button("Generate")

   if submitted:
      submit = True
      st.warning("Generating study plan...")
      lesson_plan = ask_chat(select_course, select_course_level, select_duration_course, select_hours_per_day, start_date)
      st.write(lesson_plan)
      ics_file = generate_ics_file(lesson_plan, start_date)
      with open(ics_file, 'rb') as f:
       st.download_button(label="Download .ics file", data=f, file_name='lesson_plan.ics')


st.divider()

st.subheader('Upload a document to review it and receive feedback')
client = oclient.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file is not None:
    pdf_reader = PdfReader(uploaded_file)
    content = ""
    for page in pdf_reader.pages:
        content += page.extract_text()
    
    st.write("Document content:")
    st.write(content[:500]) 

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant that reviews assessments."},
            {"role": "user", "content": f"Review the following assessment and provide feedback on which questions might be wrong, an overview, and some feedback:\n\n{content}"}
        ],
        max_tokens=500
    )

    feedback = response.choices[0].message['content'].strip()

    st.subheader("Feedback on Assessment")
    st.write(feedback)

def get_ppt_download_link(ppt_filename):
    with open(ppt_filename, "rb") as file:
        ppt_contents = file.read()
    b64_ppt = base64.b64encode(ppt_contents).decode()
    return f'<a href="data:application/vnd.openxmlformats-officedocument.presentationml.presentation;base64,{b64_ppt}" download="{ppt_filename}">Download the PowerPoint Presentation</a>'

st.divider()
st.subheader('Type a content topic to start generating a PPT')

with st.form("Study Plan Text Form"):
    topic = st.text_input("Enter the topic for your presentation:")
    generate_button = st.form_submit_button("Generate Presentation")

    if generate_button and topic:
        with st.spinner("Generating presentation... Please wait."):
            slide_titles = generate_slide_titles(topic)
            slide_contents = [generate_slide_content(title) for title in slide_titles]
            ppt_filename = create_presentation(topic, slide_titles, slide_contents)

        st.success("Presentation generated successfully!")

        st.markdown(get_ppt_download_link(ppt_filename), unsafe_allow_html=True)