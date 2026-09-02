# 🤖 AI Resume Analyzer

<p align="center">
  <a href="https://airesumeanalyzer-jeqbg9qli7k5wj4ndps3fs.streamlit.app/">
    <img src="https://img.shields.io/badge/🚀_Live_Demo-Streamlit-red?style=for-the-badge&logo=streamlit" alt="Live Demo">
  </a>
  <a href="https://github.com/pankajkumar952/AI-Resume-Analyzer">
    <img src="https://img.shields.io/badge/GitHub-Repository-black?style=for-the-badge&logo=github" alt="GitHub">
  </a>
</p>

<h1 align="center">AI Resume Analyzer</h1>

<h3 align="center">
  AI-Powered Resume Analysis & Career Assistant
</h3>

<p align="center">
  Analyze your resume, identify skills, understand your profile, and get AI-powered career insights.
</p>

<p align="center">
  <a href="https://airesumeanalyzer-jeqbg9qli7k5wj4ndps3fs.streamlit.app/">
    🚀 <strong>Try the Live Application</strong>
  </a>
</p>

---

## 🚀 Live Demo

<p align="center">

<a href="https://airesumeanalyzer-jeqbg9qli7k5wj4ndps3fs.streamlit.app/">
<img src="https://img.shields.io/badge/OPEN_AI_RESUME_ANALYZER-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Open AI Resume Analyzer">
</a>

</p>

### 🔗 Live Application

**[🚀 Open AI Resume Analyzer](https://airesumeanalyzer-jeqbg9qli7k5wj4ndps3fs.streamlit.app/)**

> Upload your resume and use the AI-powered application to analyze your profile and receive career-focused insights.

---

## 📌 About The Project

**AI Resume Analyzer** is an AI-powered web application built to help job seekers understand and improve their resumes.

The application provides an interactive interface for uploading a resume and analyzing important information such as skills, profile details, and career-related insights.

The project demonstrates how **Python, Streamlit, Artificial Intelligence, Natural Language Processing, and modern web application development** can be combined to create a practical career-focused application.

---

## ✨ Features

- 📄 Resume Upload
- 🤖 AI-powered resume analysis
- 🔍 Resume content analysis
- 🧠 Skill identification
- 📊 Profile analysis
- 💼 Career-focused insights
- 🎯 Job-oriented recommendations
- 🖥️ Interactive Streamlit interface
- ⚡ Fast and simple workflow
- ☁️ Cloud deployment
- 🔄 GitHub-based deployment workflow

---

## 🛠️ Technology Stack

### Programming Language

- Python

### Framework

- Streamlit

### AI / Machine Learning

- Generative AI
- Natural Language Processing
- Machine Learning
- Resume Analysis
- AI-powered Recommendations

### Development Tools

- Git
- GitHub
- VS Code
- Streamlit Community Cloud

---

## 🏗️ Application Workflow

<p align="center">

<b>User</b>
<br>
⬇
<br>
<b>Resume Upload</b>
<br>
⬇
<br>
<b>Resume Processing</b>
<br>
⬇
<br>
<b>AI / Resume Analysis</b>
<br>
⬇
<br>
<b>Skill & Profile Analysis</b>
<br>
⬇
<br>
<b>Career Insights & Recommendations</b>

</p>

---

## 📂 Project Structure

```text
AI-Resume-Analyzer/
│
├── app.py
├── requirements.txt
├── README.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── DEPLOYMENT.md
├── AI_MODELS.md
├── Dockerfile
├── .gitignore
│
├── assets/
│   └── ...
│
├── config/
│   └── ...
│
├── src/
│   └── ...
│
└── .devcontainer/
    └── devcontainer.json
```

> The exact project structure may vary depending on the current implementation.

---

## ⚙️ Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/pankajkumar952/AI-Resume-Analyzer.git
```

### 2. Open the Project

```bash
cd AI-Resume-Analyzer
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

#### macOS / Linux

```bash
source venv/bin/activate
```

### 5. Upgrade pip

```bash
python -m pip install --upgrade pip
```

### 6. Install Dependencies

```bash
pip install -r requirements.txt
```

### 7. Install the spaCy English Model

If required by the resume analysis module:

```bash
python -m spacy download en_core_web_sm
```

### 8. Start the Streamlit Application

```bash
streamlit run app.py
```

The application will normally be available at:

```text
http://localhost:8501
```

---

## ☁️ Deployment

The application is deployed using **Streamlit Community Cloud**.

### 🌐 Production Application

**[🚀 AI Resume Analyzer — Live Application](https://airesumeanalyzer-jeqbg9qli7k5wj4ndps3fs.streamlit.app/)**

### Deployment Architecture

```text
Local Development
       │
       ▼
   Git Changes
       │
       ▼
     GitHub
       │
       ▼
Streamlit Community Cloud
       │
       ▼
  Live Web Application
```

---

## 🔄 Continuous Deployment

The project uses GitHub as the source repository for the deployed Streamlit application.

The development workflow is:

```text
Make Code Changes
       │
       ▼
   git add .
       │
       ▼
  git commit
       │
       ▼
   git push
       │
       ▼
     GitHub
       │
       ▼
Streamlit Deployment
       │
       ▼
  Updated App
```

### Basic Git Workflow

```bash
git add .
git commit -m "Update AI Resume Analyzer"
git push
```

Changes pushed to the configured GitHub repository can then be deployed through Streamlit Community Cloud.

---

## 🐳 Docker

The project also includes a Docker configuration for containerized deployment.

### Build the Docker Image

```bash
docker build -t ai-resume-analyzer .
```

### Run the Container

```bash
docker run -p 8501:8501 ai-resume-analyzer
```

Open:

```text
http://localhost:8501
```

---

## 🎯 Project Objectives

The main objectives of this project are:

- Help candidates understand their resumes
- Identify important technical skills
- Analyze resume information
- Provide AI-powered career insights
- Improve resume quality
- Support job seekers during their career journey
- Demonstrate practical AI application development
- Build and deploy a real-world Python application

---

## 🧠 Key Concepts Demonstrated

This project demonstrates practical knowledge of:

- Python Programming
- Streamlit Application Development
- Artificial Intelligence
- Machine Learning
- Natural Language Processing
- Resume Parsing
- Text Processing
- Generative AI
- Prompt Engineering
- Web Application Development
- Git & GitHub
- Cloud Deployment
- Application Deployment
- Continuous Deployment

---

# 🚀 Other Projects

## 1. CognitiveFraud — Real-Time AI Fraud Detection Platform

A real-time fraud detection and risk analytics platform designed to analyze transactions and identify suspicious activities.

### Technologies

- Python
- FastAPI
- Apache Kafka
- PostgreSQL
- Redis
- XGBoost
- Docker
- AWS
- React
- TypeScript

### Key Features

- Real-time transaction processing
- Fraud risk scoring
- Rule-based fraud detection
- Velocity monitoring
- JWT authentication
- Role-Based Access Control
- Kafka event processing
- WebSocket notifications

---

## 2. JobPulse AI — Intelligent Job & Recruitment Platform

An AI-powered recruitment platform designed to connect job seekers and recruiters.

### Key Features

- Job discovery
- Resume parsing
- Candidate matching
- AI interview preparation
- Recruiter job posting
- Candidate ranking
- Event-driven architecture

---

## 3. AI-Powered Code Debugger Assistant

An AI-powered application designed to analyze source code and provide debugging recommendations.

### Technologies

- Python
- Streamlit
- AI
- Source Code Analysis

### Key Features

- Code analysis
- Error detection
- Debugging recommendations
- AI-assisted troubleshooting

---

# 💼 Technical Skills

## Languages

- Java
- Python
- JavaScript

## Backend

- Spring Boot
- Spring MVC
- Spring Security
- FastAPI
- Hibernate
- REST APIs
- Microservices

## Frontend

- React.js
- Angular
- HTML5
- CSS3

## Databases

- MySQL
- PostgreSQL
- MongoDB

## Cloud & DevOps

- AWS
- Docker
- Jenkins
- CI/CD
- Maven

## Messaging & Testing

- Apache Kafka
- JUnit
- REST Assured
- Postman

## AI / Machine Learning

- Scikit-learn
- TensorFlow
- PyTorch
- NLP
- Generative AI
- Computer Vision
- Recommendation Systems
- Fraud Detection Models

## Tools & Concepts

- Git
- GitHub
- Linux
- JIRA
- VS Code
- OOP
- DSA
- SDLC
- Agile Scrum
- Debugging

---

# 📜 Certifications

- Oracle Cloud Infrastructure 2025 Certified AI Foundations Associate
- Oracle Autonomous Database Cloud 2025 Certified Professional
- Oracle Cloud Infrastructure 2025 Certified Data Science Professional
- Oracle Cloud Infrastructure 2025 Certified Generative AI Professional
- Data Analytics Job Simulation — Deloitte Forage
- Data Science Job Simulation — BCGX Forage
- Software Engineering Job Simulation — JPMorgan Chase & Co. Forage
- Java Programming Quiz — CodeAlpha
- eLitmus pH Test — 99.57 Percentile

---

# 🎓 Education

## Bachelor of Technology — Computer Science Engineering

**Invertis University, Bareilly**

**2019 – 2023**

**CGPA:** 7.36 / 10

---

# 👨‍💻 About Me

Hi, I'm **Pankaj Kumar**, a Software Developer based in Hyderabad, India.

I am interested in building scalable software applications, backend systems, full-stack applications, and AI-powered solutions.

### Areas of Interest

- Java Development
- Spring Boot
- Python
- REST APIs
- Microservices
- React.js
- SQL
- Apache Kafka
- Docker
- AWS
- AI / ML
- Generative AI

---

# 📊 GitHub

<p align="center">

<a href="https://github.com/pankajkumar952">
<img src="https://github-readme-stats.vercel.app/api?username=pankajkumar952&show_icons=true&hide_border=true" alt="Pankaj Kumar GitHub Stats">
</a>

</p>

<p align="center">

<a href="https://github.com/pankajkumar952">
<img src="https://github-readme-stats.vercel.app/api/top-langs/?username=pankajkumar952&layout=compact&hide_border=true" alt="Top Languages">
</a>

</p>

---

# 🔗 Connect With Me

### GitHub

https://github.com/pankajkumar952

### LinkedIn

https://www.linkedin.com/in/pankaj-kumar-0b82a8238/

### Portfolio

https://pankajkumar952.github.io/Portfolio/

### Learning Platform

https://pankajkumar952.github.io/Website_Learning_Platform_For_Engineer/

### AI Resume Analyzer — Live

https://airesumeanalyzer-jeqbg9qli7k5wj4ndps3fs.streamlit.app/

---

# ⭐ Support

If you find this project useful, please consider giving the repository a ⭐ on GitHub.

Your support helps improve and maintain the project.

---

<p align="center">

<strong>Built with ❤️ using Python, Streamlit & AI</strong>

</p>
