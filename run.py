#!/usr/bin/env python3
"""
COGNIS - Application Launcher
Run this script to start the application
"""

import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def check_requirements():
    """Check if all required modules are available"""
    required_modules = [
        'tkinter',
        'matplotlib',
        'numpy',
        're',
        'os',
        'sys',
        'json',
        'datetime'
    ]

    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)

    if missing_modules:
        print("Missing required modules:")
        for module in missing_modules:
            print(f"  - {module}")
        print("\nPlease install missing modules using pip:")
        print(f"pip install {' '.join(missing_modules)}")
        return False

    return True


def setup_directories():
    """Create required directories"""
    directories = [
        'resumes',
        'jd',
        'results',
        'reports'
    ]

    for directory in directories:
        Path(directory).mkdir(exist_ok=True)

    print("✓ Required directories created")


def create_sample_files():
    """Create sample files if they don't exist"""
    sample_dir = Path('resumes')
    if not any(sample_dir.glob('*.txt')):
        print("Creating sample resume files...")

        # Sample resumes
        resumes = [
            ('sample_resume_1.txt', """
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
"""),
            ('sample_resume_2.txt', """
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
"""),
            ('sample_resume_3.txt', """
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
        ]

        for filename, content in resumes:
            filepath = sample_dir / filename
            with open(filepath, 'w') as f:
                f.write(content)

        print("✓ Sample resumes created")

    # Sample job description
    jd_dir = Path('jd')
    if not any(jd_dir.glob('*.txt')):
        print("Creating sample job description...")

        with open(jd_dir / 'sample_jd.txt', 'w') as f:
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

        print("✓ Sample job description created")


def main():
    """Main launcher function"""
    print("=" * 60)
    print("COGNIS - Human Potential Compiler")
    print("Version 1.0.0")
    print("=" * 60)
    print()

    # Check requirements
    print("Checking requirements...")
    if not check_requirements():
        return 1

    print("✓ All requirements satisfied")
    print()

    # Setup environment
    print("Setting up environment...")
    setup_directories()
    create_sample_files()
    print()

    # Launch application
    print("Launching COGNIS...")
    print()

    try:
        from gui import CognisGUI
        app = CognisGUI()
        app.run()
    except ImportError as e:
        print(f"Error: Could not import GUI module: {e}")
        print("Make sure all files are in the correct directory.")
        return 1
    except Exception as e:
        print(f"Error launching application: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())