"""
COGNIS - Human Potential Compiler
Main Application Entry Point
Author: Senior Software Architect
Version: 1.0.0
"""

import sys
import os
from pathlib import Path
from gui import CognisGUI


def setup_environment():
    """Setup application environment and required directories"""
    directories = ['resumes', 'jd', 'results', 'reports']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)

    # Initialize sample files if they don't exist
    sample_dir = Path('resumes')
    if not any(sample_dir.glob('*.txt')):
        create_sample_files()


def create_sample_files():
    """Create sample resume and job description files"""
    # Sample Resume 1 - Software Engineer
    with open('resumes/sample_resume_1.txt', 'w') as f:
        f.write("""
CANDIDATE: Sarah Johnson
EMAIL: sarah.j@email.com
PHONE: +1-555-0123

EXPERIENCE:
Senior Software Engineer | TechCorp Inc. | 2020-2024
- Led development of microservices architecture handling 1M+ daily requests
- Improved system performance by 45% through optimization
- Mentored 5 junior developers and conducted code reviews
- Implemented CI/CD pipeline reducing deployment time by 60%

Software Developer | DataFlow Systems | 2018-2020
- Built RESTful APIs using Python and Django
- Reduced database query time by 30% through indexing
- Collaborated with cross-functional teams on 15+ projects

EDUCATION:
M.S. Computer Science | Stanford University | 2018
B.S. Software Engineering | MIT | 2016

SKILLS:
Python, Java, Docker, Kubernetes, AWS, PostgreSQL, MongoDB, Redis, CI/CD, Microservices, API Design, System Architecture, Leadership, Agile, Scrum

CERTIFICATIONS:
AWS Certified Solutions Architect
Kubernetes Administrator Certification

ACHIEVEMENTS:
- Employee of the Year 2022
- Published 3 technical papers on distributed systems
- Speaker at TechConf 2023
""")

    # Sample Resume 2 - Data Scientist
    with open('resumes/sample_resume_2.txt', 'w') as f:
        f.write("""
CANDIDATE: Michael Chen
EMAIL: michael.c@email.com
PHONE: +1-555-0456

EXPERIENCE:
Lead Data Scientist | AI Innovations Inc. | 2021-2024
- Developed predictive models improving accuracy by 35%
- Managed team of 8 data scientists and engineers
- Implemented MLOps pipeline reducing model deployment time by 70%
- Increased revenue by $2.5M through customer churn prediction

Data Scientist | DataViz Analytics | 2019-2021
- Created dashboards for 500+ enterprise clients
- Reduced data processing time by 50% using Spark
- Built recommendation engine serving 10K+ users daily

EDUCATION:
Ph.D. Data Science | UC Berkeley | 2021
M.S. Statistics | Stanford University | 2019

SKILLS:
Python, R, SQL, Tableau, Spark, Hadoop, TensorFlow, PyTorch, Machine Learning, Deep Learning, Statistics, Data Visualization, Big Data

CERTIFICATIONS:
Certified Data Scientist (CDS)
Google Professional Machine Learning Engineer

ACHIEVEMENTS:
- Best Research Paper Award 2022
- 5 patents in machine learning
""")

    # Sample Resume 3 - Product Manager
    with open('resumes/sample_resume_3.txt', 'w') as f:
        f.write("""
CANDIDATE: Emily Rodriguez
EMAIL: emily.r@email.com
PHONE: +1-555-0789

EXPERIENCE:
Senior Product Manager | CloudSolutions Inc. | 2022-2024
- Launched 3 successful SaaS products generating $10M+ revenue
- Defined product strategy and roadmap for enterprise suite
- Led cross-functional team of 25+ engineers and designers
- Increased user engagement by 200% through feature innovation

Product Manager | TechStartup Ventures | 2020-2022
- Managed product lifecycle from ideation to launch
- Conducted 200+ customer interviews for product validation
- Increased customer retention by 40%

EDUCATION:
MBA | Harvard Business School | 2020
B.S. Information Systems | UC Berkeley | 2016

SKILLS:
Product Strategy, Roadmapping, Agile, Scrum, User Research, Market Analysis, JIRA, Confluence, Figma, SQL, Python, Business Analytics

CERTIFICATIONS:
Certified Scrum Product Owner (CSPO)
Product Management Certification

ACHIEVEMENTS:
- Product of the Year Award 2023
- Grew user base from 10K to 150K in 18 months
""")

    # Sample Job Description
    with open('jd/sample_jd.txt', 'w') as f:
        f.write("""
JOB TITLE: Senior Software Engineer
DEPARTMENT: Engineering
COMPANY: TechCorp Inc.

JOB DESCRIPTION:
We are seeking an experienced Senior Software Engineer to join our growing engineering team. The ideal candidate will have strong backend development experience with expertise in microservices architecture and cloud technologies.

KEY RESPONSIBILITIES:
- Design and develop scalable microservices architecture
- Build and maintain RESTful APIs
- Optimize system performance and reliability
- Mentor and guide junior developers
- Implement CI/CD pipelines
- Collaborate with cross-functional teams on product development

REQUIRED SKILLS:
- Python (5+ years)
- Java (3+ years)
- Microservices Architecture
- Docker and Kubernetes
- AWS or Azure Cloud
- PostgreSQL or MongoDB
- CI/CD Practices
- System Design and Architecture
- Leadership and Mentoring
- Agile Methodologies

PREFERRED SKILLS:
- Redis
- API Design
- Distributed Systems
- Machine Learning

EDUCATION REQUIREMENTS:
- Bachelor's Degree in Computer Science or related field
- Master's Degree preferred

EXPERIENCE:
- 5-8 years of software engineering experience
- 2+ years in leadership/mentoring role
""")


def main():
    """Main application entry point"""
    try:
        # Setup environment
        setup_environment()

        # Launch GUI
        app = CognisGUI()
        app.run()

    except Exception as e:
        print(f"Error launching application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()