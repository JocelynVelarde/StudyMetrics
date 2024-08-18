
from openai import OpenAI 
import streamlit as st
from ics import Calendar, Event
from datetime import datetime, timedelta

def ask_chat(select_course, select_course_level, select_duration_course, select_hours_per_day, start_date):
  MODEL="gpt-4o"
  client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

  completion = client.chat.completions.create(
    model=MODEL,
    messages=[
      {"role": "system", "content": "Your role is to generate a detailed plan study for the professor, including proposed activities, topics, quizzes, exams, and homework"}, 
      {"role": "user", "content": "Help me to create a lesson plan for " + select_course + " class" + " at " + select_course_level + " level" + " for " + select_duration_course + " with " + select_hours_per_day + " per day" + " starting on " + start_date.strftime("%Y-%m-%d")}  
    ]
  )



  return completion.choices[0].message.content


def generate_ics_file(lesson_plan, start_date):
    calendar = Calendar()
    current_date = start_date

    for day, activities in enumerate(lesson_plan.split('\n')):
        event = Event()
        event.name = f"Lesson Plan Day {day + 1}"
        event.begin = current_date
        event.duration = timedelta(hours=1)  
        event.description = activities
        calendar.events.add(event)
        current_date += timedelta(days=1)

    with open('lesson_plan.ics', 'w') as f:
        f.writelines(calendar)

    return 'lesson_plan.ics'