
# StudyMetrics 📚
We provide the ultimate tool for monitoring students in online and offline classes, giving insights that empower teachers to enhance the learning experience by refining content and boosting engagement

<img width="700" alt="Screenshot 2024-08-18 at 12 14 27 AM" src="https://github.com/user-attachments/assets/252fbb13-2bf7-4969-aba3-b5dfe1713a26">

## Authors

- [@JocelynVelarde](https://github.com/JocelynVelarde)
- [@DiegoRossi](https://github.com/)
- [@RobertoPriego](https://github.com/rpribau)
- [@OscarCardenas](https://github.com/oscar6647)

## Features
### Generate Content
- Generate power point presentations ready to download with a single propmt.
- Generate lesson plans and study guides for your classes and export them into your Google or Outlook calendar.
- Upload student's assesments and get insights on what might be wrong or what needs improvement.

### Virtual Metrics
- Upload your zoom, teams or google meet recordings to get insights on your students' behavior and engagement.
- Select the session you want to analyze and get graphics and reports.
- You can also visualize your recorded video online while observing the metrics.

## Structure
```bash
streamlit_app 
├─ home.py
├─ algorithms
│  └─ pptx_genai.py
│  └─ review_hw.py
│  └─ s3_download.py
│  └─ simple_text.py
├─ assets
├─ jetson
├─ pages
│  └─ generate.py
│  └─ instructions.py
│  └─ upload.py
│  └─ visualize_online.py
├─ .gitignore
└─ requirements.txt
```

## Tools

- boto3
- openai
- python-pptx
- ics
- PyPDF2

Deployed with: Streamlit Cloud

## Try it

[Try it here](https://study-metrics.streamlit.app/)

## Demo

https://youtu.be/NDn7WzKKP9s


## License

[MIT](https://choosealicense.com/licenses/mit/)





