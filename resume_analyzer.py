"""
COGNIS - Resume Analyzer Module
Extracts and structures information from resumes

This module handles all resume parsing and information extraction
using only Python built-in libraries and regex patterns.
"""

import re
import os
from collections import Counter
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any
from pathlib import Path

class ResumeAnalyzer:
    """
    Analyzes and extracts structured information from resume text files.

    Features:
    - Name extraction
    - Email and phone extraction
    - Work experience parsing
    - Education history extraction
    - Skill identification (technical, soft skills)
    - Achievement extraction
    - Certification detection
    - Experience years calculation
    - Word and sentence count
    - Language detection
    """

    def __init__(self):
        """
        Initialize the resume analyzer with skill patterns and keyword lists.
        """
        # Comprehensive skill patterns organized by category
        self.skill_patterns = {
            'programming_languages': [
                'python', 'java', 'javascript', 'c\\+\\+', 'c#', 'ruby', 'php',
                'swift', 'kotlin', 'go', 'rust', 'typescript', 'scala', 'perl',
                'r', 'matlab', 'shell', 'bash', 'c', 'objective-c', 'dart',
                'elixir', 'erlang', 'haskell', 'clojure', 'groovy', 'lua'
            ],
            'frameworks': [
                'django', 'flask', 'spring', 'react', 'angular', 'vue',
                'node', 'express', 'rails', 'laravel', 'asp.net', 'jquery',
                'bootstrap', 'tensorflow', 'pytorch', 'keras', 'scikit-learn',
                'pandas', 'numpy', 'matplotlib', 'seaborn', 'plotly', 'dash',
                'fastapi', 'gin', 'echo', 'beego', 'dropwizard',
                'symfony', 'codeigniter', 'cakephp', 'yii', 'zend'
            ],
            'databases': [
                'postgresql', 'mysql', 'mongodb', 'redis', 'elasticsearch',
                'oracle', 'sql server', 'sqlite', 'cassandra', 'dynamodb',
                'neo4j', 'graphql', 'firebase', 'realm', 'couchdb', 'mariadb',
                'hbase', 'couchbase', 'arangodb', 'influxdb', 'timescaledb'
            ],
            'cloud': [
                'aws', 'azure', 'gcp', 'google cloud', 'docker', 'kubernetes',
                'terraform', 'ansible', 'jenkins', 'gitlab', 'github actions',
                'cloudformation', 'chef', 'puppet', 'salt', 'vagrant',
                'rancher', 'openshift', 'mesos', 'nomad', 'consul', 'vault'
            ],
            'methodologies': [
                'agile', 'scrum', 'kanban', 'devops', 'ci/cd', 'tdd',
                'bdd', 'microservices', 'serverless', 'event-driven',
                'waterfall', 'lean', 'six sigma', 'cmmi', 'itil', 'cobit'
            ],
            'soft_skills': [
                'leadership', 'mentoring', 'coaching', 'communication',
                'presentation', 'negotiation', 'team building', 'collaboration',
                'problem solving', 'critical thinking', 'decision making',
                'strategic planning', 'project management', 'time management',
                'adaptability', 'creativity', 'emotional intelligence'
            ]
        }

        # Achievement keywords for detecting accomplishments
        self.achievement_keywords = [
            'increased', 'improved', 'reduced', 'saved', 'generated',
            'delivered', 'led', 'built', 'designed', 'implemented',
            'created', 'developed', 'launched', 'managed', 'mentored',
            'optimized', 'streamlined', 'accelerated', 'boosted',
            'achieved', 'attained', 'exceeded', 'pioneered', 'introduced',
            'established', 'founded', 'spearheaded', 'revitalized', 'transformed'
        ]

        # Education degree patterns
        self.education_patterns = {
            'phd': ['phd', 'doctorate', 'doctor of', 'd.phil'],
            'masters': ['master', 'm.s', 'm.sc', 'm.a', 'm.b.a', 'mba', 'msc', 'meng'],
            'bachelors': ['bachelor', 'b.s', 'b.sc', 'b.a', 'beng', 'btech', 'be', 'bs'],
            'associates': ['associate', 'a.s', 'a.a', 'a.sc'],
            'high_school': ['high school', 'secondary school', 'ged']
        }

        # Common resume section headers
        self.section_headers = {
            'experience': ['experience', 'work experience', 'employment', 'professional experience',
                           'career history', 'work history', 'employment history'],
            'education': ['education', 'academic', 'qualifications', 'academic background',
                          'educational background', 'schooling'],
            'skills': ['skills', 'technical skills', 'professional skills', 'core competencies',
                       'competencies', 'expertise', 'technologies'],
            'certifications': ['certifications', 'certification', 'licenses', 'license',
                               'professional certifications', 'certificates'],
            'projects': ['projects', 'project experience', 'key projects', 'personal projects'],
            'achievements': ['achievements', 'accomplishments', 'awards', 'recognition'],
            'publications': ['publications', 'papers', 'articles', 'research papers'],
            'interests': ['interests', 'hobbies', 'activities', 'extracurricular']
        }

    def analyze_resume(self, resume_content: str, filename: str = None) -> Dict[str, Any]:
        """
        Analyze resume and extract structured information.

        Args:
            resume_content: String containing the resume text

        Returns:
            Dictionary with parsed resume information
        """
        try:
            # Sanitize and prepare content
            content = self._preprocess_content(resume_content)

            # Extract basic information
            # Extract basic information
            name = self._extract_name(content)

            # Filename fallback
            if name is None and filename:
                from pathlib import Path
                name = Path(filename).stem.replace("_", " ").replace("-", " ").title()
            elif name is None:
                name = "Candidate"

            email = self._extract_email(content)
            phone = self._extract_phone(content)

            # Extract sections
            experience = self._extract_experience(content)
            education = self._extract_education(content)
            skills = self._extract_skills(content)
            achievements = self._extract_achievements(content)
            certifications = self._extract_certifications(content)
            projects = self._extract_projects(content)
            publications = self._extract_publications(content)

            # Calculate additional metrics
            experience_years = self._calculate_experience_years(experience, content)
            total_work_experience = self._extract_work_timeline(content)

            # Language analysis
            language_complexity = self._analyze_language_complexity(content)

            return {
                'name': name,
                'email': email,
                'phone': phone,
                'experience': experience,
                'experience_years': experience_years,
                'total_work_experience': total_work_experience,
                'education': education,
                'skills': skills,
                'achievements': achievements,
                'certifications': certifications,
                'projects': projects,
                'publications': publications,
                'raw_content': content,
                'word_count': len(content.split()),
                'sentence_count': len(re.findall(r'[.!?]+', content)),
                'language_complexity': language_complexity,
                'has_contact_info': bool(email != 'Unknown' or phone != 'Unknown'),
                'section_count': len(self._detect_sections(content))
            }

        except Exception as e:
            print(f"Error analyzing resume: {e}")
            return self._get_empty_result(resume_content)

    def _preprocess_content(self, content: str) -> str:
        """
        Preprocess resume content for better parsing.

        Args:
            content: Raw resume text

        Returns:
            Preprocessed text
        """
        # Remove excessive whitespace
        content = re.sub(r'\n\s*\n', '\n\n', content)

        # Remove carriage returns
        content = content.replace('\r', '')

        # Normalize bullet points
        content = re.sub(r'[•·●○▪▸►]', '•', content)

        # Normalize dashes
        content = re.sub(r'[–—]', '-', content)

        # Fix common OCR artifacts
        content = re.sub(r'[|]', 'I', content)

        return content

    def _get_empty_result(self, content: str) -> Dict[str, Any]:
        """
        Return empty result structure when analysis fails.

        Args:
            content: Original resume content

        Returns:
            Dictionary with default values
        """
        return {
            'name': 'Unknown',
            'email': 'Unknown',
            'phone': 'Unknown',
            'experience': [],
            'experience_years': 0,
            'total_work_experience': 0,
            'education': [],
            'skills': [],
            'achievements': [],
            'certifications': [],
            'projects': [],
            'publications': [],
            'raw_content': content,
            'word_count': len(content.split()),
            'sentence_count': len(re.findall(r'[.!?]+', content)),
            'language_complexity': {},
            'has_contact_info': False,
            'section_count': 0
        }

    def _detect_sections(self, content: str) -> List[str]:
        """
        Detect and return all sections present in the resume.

        Args:
            content: Resume text

        Returns:
            List of detected section names
        """
        detected_sections = []
        content_lower = content.lower()

        for section, headers in self.section_headers.items():
            for header in headers:
                # Look for header at the start of a line
                if re.search(r'^' + re.escape(header) + r'[:\s]', content_lower, re.MULTILINE):
                    detected_sections.append(section)
                    break

        return detected_sections

    def _extract_name(self, content: str) -> str:
        """
        Extract candidate name from resume.

        Args:
            content: Resume text

        Returns:
            Extracted name or 'Unknown'
        """
        # Look for name patterns at the beginning
        lines = content.split('\n')[:15]  # Check first 15 lines

        for line in lines:
            line = line.strip()

            # Skip empty lines and common headers
            if not line or len(line) < 2:
                continue

            skip_keywords = [
                'candidate', 'resume', 'curriculum', 'vitae', 'email',
                'phone', 'contact', 'address', 'summary', 'objective',
                'experience', 'education', 'skills', 'certification'
            ]

            if any(keyword in line.lower() for keyword in skip_keywords):
                continue

            # Check if line contains uppercase words (potential name)
            words = line.split()

            # Name should be 2-4 words
            if 2 <= len(words) <= 4:
                # Check if all words start with capital letters
                if all(w[0].isupper() for w in words if len(w) > 1):
                    # Ensure it doesn't look like a job title
                    if not any(w in ['of', 'and', 'for', 'with', 'the'] for w in words):
                        return line

        # Try alternative pattern - look for common name formats
        name_patterns = [
            r'([A-Z][a-z]+ [A-Z][a-z]+(?: [A-Z][a-z]+)?)',
            r'([A-Z][a-z]+\.? [A-Z][a-z]+)',
            r'([A-Z][A-Z]\.? [A-Z][a-z]+ [A-Z][a-z]+)'
        ]

        for pattern in name_patterns:
            matches = re.findall(pattern, content)
            if matches:
                # Filter out false positives
                for match in matches:
                    if not any(kw in match.lower() for kw in skip_keywords):
                        return match

        return "Candidate"

    def _extract_email(self, content: str) -> str:
        """
        Extract email address from resume.

        Args:
            content: Resume text

        Returns:
            Extracted email or 'Unknown'
        """
        # Standard email pattern
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        matches = re.findall(email_pattern, content)

        if matches:
            # Return first valid email
            return matches[0]

        return "Unknown"

    def _extract_phone(self, content: str) -> str:
        """
        Extract phone number from resume.

        Args:
            content: Resume text

        Returns:
            Extracted phone number or 'Unknown'
        """
        # Multiple phone number patterns
        phone_patterns = [
            r'(\+\d{1,3}[\s-]?)?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{4}',
            r'\+?\d{1,3}[\s.-]?\d{3}[\s.-]?\d{3}[\s.-]?\d{4}',
            r'\+?\d{1,3}[\s.-]?\d{3}[\s.-]?\d{4}[\s.-]?\d{4}?'
        ]

        for pattern in phone_patterns:
            matches = re.findall(pattern, content)
            if matches:
                # Clean and return first match
                phone = matches[0]
                # Remove spaces, dashes, parentheses
                phone = re.sub(r'[\s\-()]', '', phone)
                return phone

        return "Unknown"

    def _extract_experience(self, content: str) -> List[Dict[str, str]]:
        """
        Extract work experience entries from resume.

        Args:
            content: Resume text

        Returns:
            List of experience dictionaries
        """
        experience = []

        # Find experience section
        experience_section = self._find_section(content, self.section_headers['experience'])

        if not experience_section:
            # Try to find experience without section header
            experience_section = self._find_experience_without_section(content)

        if not experience_section:
            return experience

        # Split into individual experiences
        exp_entries = self._split_into_experiences(experience_section)

        for entry in exp_entries:
            if entry.strip():
                # Extract structured data from entry
                exp_data = self._parse_experience_entry(entry)
                if exp_data:
                    experience.append(exp_data)

        return experience

    def _find_section(self, content: str, headers: List[str]) -> Optional[str]:
        """
        Find a specific section in the resume.

        Args:
            content: Resume text
            headers: List of section header variations

        Returns:
            Section text or None if not found
        """
        content_lower = content.lower()

        # Find section header positions
        positions = []
        for header in headers:
            pattern = r'^' + re.escape(header) + r'[:\s]'
            for match in re.finditer(pattern, content_lower, re.MULTILINE):
                positions.append((match.start(), header))

        if not positions:
            return None

        # Sort by position and get first occurrence
        positions.sort()

        # Determine end of section (next section or end of file)
        start_pos = positions[0][0]

        # Find all section headers
        all_headers = []
        for section, section_headers in self.section_headers.items():
            for header in section_headers:
                pattern = r'^' + re.escape(header) + r'[:\s]'
                for match in re.finditer(pattern, content_lower, re.MULTILINE):
                    if match.start() > start_pos:
                        all_headers.append(match.start())

        if all_headers:
            end_pos = min(all_headers)
        else:
            end_pos = len(content)

        return content[start_pos:end_pos].strip()

    def _find_experience_without_section(self, content: str) -> Optional[str]:
        """
        Find experience entries when no explicit section header exists.

        Args:
            content: Resume text

        Returns:
            Experience text or None
        """
        # Look for common experience patterns
        patterns = [
            r'(\d{4}[\s-]*\d{4}|\d{4}[\s-]*Present)\s*[|,]\s*([^\n]+)',  # Date pattern
            r'([A-Z][a-z]+ [A-Z][a-z]+(?:\s+at\s+[A-Z][a-z]+)?)'  # Job title pattern
        ]

        for pattern in patterns:
            matches = re.findall(pattern, content)
            if len(matches) >= 2:  # At least 2 experiences
                # Return a portion of content containing experience
                start_idx = content.find(matches[0][0])
                if start_idx != -1:
                    end_idx = self._find_next_section_start(content, start_idx)
                    return content[start_idx:end_idx].strip()

        return None

    def _find_next_section_start(self, content: str, start_pos: int) -> int:
        """
        Find the start of the next section after a given position.

        Args:
            content: Resume text
            start_pos: Current position

        Returns:
            Position of next section or end of content
        """
        content_lower = content.lower()

        # Look for common section headers
        for headers in self.section_headers.values():
            for header in headers:
                pattern = r'^' + re.escape(header) + r'[:\s]'
                for match in re.finditer(pattern, content_lower, re.MULTILINE):
                    if match.start() > start_pos:
                        return match.start()

        return len(content)

    def _split_into_experiences(self, experience_section: str) -> List[str]:
        """
        Split experience section into individual entries.

        Args:
            experience_section: Section containing work experiences

        Returns:
            List of individual experience entries
        """
        # Try multiple splitting strategies
        entries = []

        # Strategy 1: Split by blank lines with date pattern
        blocks = re.split(r'\n\s*\n', experience_section)
        for block in blocks:
            if re.search(r'\d{4}[\s-]*\d{4}|\d{4}[\s-]*Present', block):
                entries.append(block)

        # Strategy 2: Split by company pattern
        if len(entries) < 2:
            entries = []
            lines = experience_section.split('\n')
            current_entry = []

            for line in lines:
                # Look for company name pattern
                if re.search(r'(?:at|with|for)\s+[A-Z][a-zA-Z\s]+(?:Inc|Corp|LLC|Company)', line):
                    if current_entry:
                        entries.append('\n'.join(current_entry))
                        current_entry = []
                current_entry.append(line)

            if current_entry:
                entries.append('\n'.join(current_entry))

        # Strategy 3: Split by date pattern
        if len(entries) < 2:
            entries = re.split(r'(?=\d{4}[\s-]*\d{4}|\d{4}[\s-]*Present)', experience_section)
            entries = [e for e in entries if e.strip()]

        return entries

    def _parse_experience_entry(self, entry: str) -> Optional[Dict[str, str]]:
        """
        Parse a single experience entry into structured data.

        Args:
            entry: Single experience entry

        Returns:
            Dictionary with title, company, period, and description
        """
        if not entry.strip():
            return None

        # Extract date period
        period_pattern = r'(\d{4}[\s-]*\d{4}|\d{4}[\s-]*Present)'
        period_match = re.search(period_pattern, entry)
        period = period_match.group(0) if period_match else ""

        # Remove period from entry for further parsing
        entry_without_period = re.sub(period_pattern, '', entry).strip()

        # Extract company name
        company_pattern = r'(?:at|with|for)\s+([A-Z][a-zA-Z\s]+(?:Inc|Corp|LLC|Company|Corporation|Technologies|Systems|Solutions)?)'
        company_match = re.search(company_pattern, entry_without_period)
        company = company_match.group(1).strip() if company_match else ""

        # Remove company from entry
        if company_match:
            entry_without_period = re.sub(company_pattern, '', entry_without_period).strip()

        # Extract title (first line or before comma/pipe)
        lines = entry_without_period.split('\n')
        title = ""

        if lines:
            first_line = lines[0].strip()
            # Title is before comma or pipe
            title_parts = re.split(r'[,|]', first_line)
            if title_parts:
                title = title_parts[0].strip()

        # If title empty, try to find in first line
        if not title and lines:
            title = lines[0].strip()

        # Description is everything after the first few lines
        description_lines = lines[1:] if len(lines) > 1 else []
        description = '\n'.join(description_lines).strip()

        return {
            'title': title,
            'company': company,
            'period': period,
            'description': description
        }

    def _extract_education(self, content: str) -> List[Dict[str, str]]:
        """
        Extract education entries from resume.

        Args:
            content: Resume text

        Returns:
            List of education dictionaries
        """
        education = []

        # Find education section
        education_section = self._find_section(content, self.section_headers['education'])

        if not education_section:
            return education

        # Split into individual education entries
        edu_entries = re.split(r'\n\s*\n', education_section)

        for entry in edu_entries:
            if not entry.strip():
                continue

            # Extract degree
            degree = ""
            for level, patterns in self.education_patterns.items():
                for pattern in patterns:
                    if pattern in entry.lower():
                        degree = level
                        break
                if degree:
                    break

            # Extract institution
            institution_pattern = r'(?:at|from|of)\s+([A-Z][a-zA-Z\s]+(?:University|College|Institute|School)?)'
            institution_match = re.search(institution_pattern, entry)
            institution = institution_match.group(1).strip() if institution_match else ""

            # Extract year
            year_pattern = r'\b(19|20)\d{2}\b'
            year_match = re.search(year_pattern, entry)
            year = year_match.group(0) if year_match else ""

            if degree or institution:
                education.append({
                    'degree': degree if degree else "Unknown",
                    'institution': institution if institution else "Unknown",
                    'year': year,
                    'details': entry.strip()
                })

        return education

    def _extract_skills(self, content: str) -> List[str]:
        skills = set()
        content_lower = content.lower()

        skills_section = self._find_section(content, self.section_headers['skills'])

        if skills_section:
            skill_items = re.split(r'[|,••\n;]', skills_section)
            for item in skill_items:
                item = item.strip().lower()

                for prefix in ['skills', 'technologies', 'expertise', 'competencies']:
                    item = item.replace(prefix, '').strip()

                if len(item) > 1 and item not in ['and', 'or', 'with', 'of', 'the']:
                    skills.add(item)

        if not skills:
            for category, skill_list in self.skill_patterns.items():
                for skill in skill_list:
                    if re.search(r'\b' + re.escape(skill.lower()) + r'\b', content_lower):
                        skills.add(skill)

        return sorted(list(skills))

    def _extract_achievements(self, content: str) -> List[str]:
        """
        Extract achievements and accomplishments from resume.

        Args:
            content: Resume text

        Returns:
            List of achievement statements
        """
        achievements = []

        # Check for achievements section
        achievements_section = self._find_section(content, self.section_headers['achievements'])

        if achievements_section:
            # Extract bullet points
            bullet_items = re.findall(r'[•\-*]\s*([^.!?]+[.!?]?)', achievements_section)
            for item in bullet_items:
                item = item.strip()
                if self._is_achievement(item):
                    achievements.append(item)

        # Scan for achievement patterns in entire content
        if len(achievements) < 5:
            lines = content.split('\n')
            for line in lines:
                line = line.strip()
                if self._is_achievement(line):
                    # Avoid duplicates
                    if line not in achievements:
                        achievements.append(line)

        # Look for quantified achievements
        quantified_pattern = r'(?:increased|improved|reduced|saved|generated|delivered|boosted)\s+[^.!?]*?(?:\d+%|\$\d+|\d+\s*(?:million|k|thousand))[^.!?]*?[.!?]'
        quantified_matches = re.findall(quantified_pattern, content, re.IGNORECASE)

        for match in quantified_matches:
            match = match.strip()
            if match not in achievements:
                achievements.append(match)

        # Sort by quality (quantified achievements first)
        achievements.sort(key=lambda x: 0 if re.search(r'\d+%|\$\d+', x) else 1)

        return achievements[:10]  # Limit to top 10

    def _is_achievement(self, text: str) -> bool:
        """
        Check if text is an achievement statement.

        Args:
            text: Text to check

        Returns:
            True if it appears to be an achievement
        """
        if not text or len(text) < 10:
            return False

        # Check for achievement keywords
        has_keyword = any(keyword in text.lower() for keyword in self.achievement_keywords)

        # Check for quantifiable results
        has_numbers = bool(re.search(r'\d+%|\$\d+|\d+\s*(?:million|k|thousand)', text))

        # Check for action-oriented language
        has_action = bool(re.search(r'\b(?:led|built|created|designed|implemented|developed)\b', text.lower()))

        return has_keyword or has_numbers or has_action

    def _extract_certifications(self, content: str) -> List[str]:
        """
        Extract certifications from resume.

        Args:
            content: Resume text

        Returns:
            List of certifications
        """
        certifications = []

        # Look for certification section
        cert_section = self._find_section(content, self.section_headers['certifications'])

        if cert_section:
            # Extract certification lines
            cert_lines = re.split(r'[|,•\n;]', cert_section)
            for cert in cert_lines:
                cert = cert.strip()
                if self._is_certification(cert):
                    certifications.append(cert)

        # If no certification section, scan for keywords
        if not certifications:
            cert_keywords = [
                'certified', 'certification', 'certificate',
                'course', 'training', 'workshop',
                'internship', 'intern',
                'nptel', 'coursera', 'udemy',
                'license', 'scrum master',
                'aws certified', 'azure certified',
                'google certified',
                'project management',
                'agile certified',
                'itil certified',
                'cissp', 'ccna', 'ccnp',
                'pmp', 'six sigma'
            ]

            for line in content.split('\n'):
                line = line.strip()

                if len(line) < 5:
                    continue

                line_lower = line.lower()

                for keyword in cert_keywords:
                    if keyword in line_lower:
                        if line not in certifications:
                            certifications.append(line)
                        break

        return certifications[:10]

    def _is_certification(self, text: str) -> bool:
        """
        Check if text is a certification.

        Args:
            text: Text to check

        Returns:
            True if it appears to be a certification
        """
        if not text or len(text) < 5:
            return False

        cert_indicators = [
            'certified', 'certification', 'license', 'accredited',
            'professional', 'expert', 'master', 'specialist'
        ]

        return any(indicator in text.lower() for indicator in cert_indicators)

    def _extract_projects(self, content: str) -> List[str]:
        """
        Extract project descriptions from resume.

        Args:
            content: Resume text

        Returns:
            List of project descriptions
        """
        projects = []

        # Look for projects section
        project_section = self._find_section(content, self.section_headers['projects'])

        if project_section:
            # Extract bullet points
            project_items = re.findall(r'[•\-*]\s*([^.!?]+[.!?]?)', project_section)
            for item in project_items:
                item = item.strip()
                if len(item) > 20:
                    projects.append(item)

        # If no projects section, look for project keywords
        if not projects:
            project_keywords = ['project', 'initiative', 'built', 'created', 'developed']
            for line in content.split('\n'):
                if any(keyword in line.lower() for keyword in project_keywords) and len(line) > 30:
                    if line.strip() not in projects:
                        projects.append(line.strip())

        return projects[:5]

    def _extract_publications(self, content: str) -> List[str]:
        """
        Extract publications from resume.

        Args:
            content: Resume text

        Returns:
            List of publications
        """
        publications = []

        # Look for publications section
        pub_section = self._find_section(content, self.section_headers['publications'])

        if pub_section:
            # Extract publication items
            pub_items = re.split(r'[|,•\n;]', pub_section)
            for pub in pub_items:
                pub = pub.strip()
                if len(pub) > 10:
                    publications.append(pub)

        # If no publications section, look for publication keywords
        if not publications:
            pub_keywords = ['published', 'publication', 'paper', 'article', 'conference', 'journal']
            for line in content.split('\n'):
                if any(keyword in line.lower() for keyword in pub_keywords) and len(line) > 20:
                    if line.strip() not in publications:
                        publications.append(line.strip())

        return publications[:5]

    def _calculate_experience_years(self, experience: List[Dict], content: str) -> float:
        """
        Calculate total years of experience.

        Args:
            experience: List of experience entries
            content: Resume text

        Returns:
            Total years of experience
        """
        total_years = 0
        current_year = datetime.now().year

        # Try to extract from structured experience
        for exp in experience:
            period = exp.get('period', '')
            if period:
                # Extract years from period
                years = re.findall(r'\b(19|20)\d{2}\b', period)
                if years:
                    try:
                        start_year = int(years[0])
                        end_year = int(years[1]) if len(years) > 1 else current_year
                        if end_year < start_year:
                            end_year = current_year
                        total_years += (end_year - start_year)
                    except (ValueError, IndexError):
                        continue

        # If no years found in structured data, scan content
        if total_years == 0:
            # Look for date patterns in content
            year_patterns = [
                r'(\d{4})\s*[-–—]\s*(\d{4})',
                r'(\d{4})\s*[-–—]\s*Present',
                r'(\d{4})\s*to\s*(\d{4})',
                r'(\d{4})\s*to\s*Present'
            ]

            for pattern in year_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                for match in matches:
                    try:
                        if len(match) == 2:
                            start_year = int(match[0])
                            end_year = int(match[1]) if match[1].isdigit() else current_year
                            years_diff = end_year - start_year
                            if 0 < years_diff < 50:  # Sanity check
                                total_years += years_diff
                        else:
                            start_year = int(match[0])
                            years_diff = current_year - start_year
                            if 0 < years_diff < 50:
                                total_years += years_diff
                    except:
                        continue

        # If no experience data, estimate from education
        if total_years == 0:
            # Look for graduation year
            grad_years = re.findall(r'(?:Graduated|Class of)\s*(\d{4})', content, re.IGNORECASE)
            if grad_years:
                try:
                    grad_year = int(grad_years[0])
                    total_years = current_year - grad_year - 1  # Subtract 1 year for education
                except:
                    pass

        # Cap at reasonable maximum
        total_years = min(total_years, 50)

        return round(total_years, 1)

    def _extract_work_timeline(self, content: str) -> List[Dict[str, Any]]:
        """
        Extract complete work timeline from resume.

        Args:
            content: Resume text

        Returns:
            List of timeline events
        """
        timeline = []

        # Find all date patterns
        year_pattern = r'\b(19|20)\d{2}\b'
        dates = re.findall(year_pattern, content)

        if dates:
            unique_dates = sorted(set(int(d) for d in dates))
            for date in unique_dates:
                if 1990 <= date <= datetime.now().year:
                    # Find context around date
                    context = self._get_date_context(content, str(date))
                    timeline.append({
                        'year': date,
                        'context': context
                    })

        return timeline

    def _get_date_context(self, content: str, date_str: str) -> str:
        """
        Get context around a specific date mention.

        Args:
            content: Resume text
            date_str: Date string to find

        Returns:
            Context text around the date
        """
        # Find position of date
        pos = content.find(date_str)
        if pos == -1:
            return ""

        # Get surrounding text (100 chars before and after)
        start = max(0, pos - 100)
        end = min(len(content), pos + 100)
        context = content[start:end]

        # Clean up context
        context = ' '.join(context.split())

        return context

    def _analyze_language_complexity(self, content: str) -> Dict[str, Any]:
        """
        Analyze language complexity of the resume.

        Args:
            content: Resume text

        Returns:
            Dictionary with language metrics
        """
        if not content:
            return {}

        words = content.split()
        sentences = re.findall(r'[^.!?]+[.!?]', content)

        # Calculate metrics
        total_words = len(words)
        total_sentences = len(sentences)
        unique_words = len(set(words))

        # Average metrics
        avg_word_length = sum(len(w) for w in words) / total_words if total_words > 0 else 0
        avg_sentence_length = total_words / total_sentences if total_sentences > 0 else 0

        # Vocabulary richness (type-token ratio)
        vocabulary_richness = unique_words / total_words if total_words > 0 else 0

        return {
            'total_words': total_words,
            'unique_words': unique_words,
            'total_sentences': total_sentences,
            'avg_word_length': round(avg_word_length, 2),
            'avg_sentence_length': round(avg_sentence_length, 2),
            'vocabulary_richness': round(vocabulary_richness, 3),
            'readability_score': self._calculate_readability(content)
        }

    def _calculate_readability(self, content: str) -> float:
        """
        Calculate readability score (simplified Flesch Reading Ease).

        Args:
            content: Resume text

        Returns:
            Readability score (0-100)
        """
        sentences = re.findall(r'[^.!?]+[.!?]', content)
        words = content.split()

        if not sentences or not words:
            return 0

        # Flesch Reading Ease formula (simplified)
        total_sentences = len(sentences)
        total_words = len(words)
        total_syllables = sum(self._count_syllables(word) for word in words)

        if total_sentences == 0:
            return 0

        # Formula: 206.835 - 1.015*(words/sentences) - 84.6*(syllables/words)
        score = 206.835 - 1.015 * (total_words / total_sentences) - 84.6 * (total_syllables / total_words)

        # Clamp to 0-100
        return max(0, min(100, score))

    def _count_syllables(self, word: str) -> int:
        """
        Count syllables in a word (approximate).

        Args:
            word: Word to count syllables for

        Returns:
            Approximate syllable count
        """
        word = word.lower()
        if len(word) <= 3:
            return 1

        # Count vowel groups
        vowels = 'aeiouy'
        count = 0
        prev_char = ''

        for char in word:
            if char in vowels and prev_char not in vowels:
                count += 1
            prev_char = char

        # Adjust for silent e
        if word.endswith('e'):
            count -= 1

        # Ensure at least 1 syllable
        return max(1, count)

    def get_skill_gaps(self, candidate_skills: List[str], required_skills: List[str]) -> Tuple[List[str], List[str]]:
        """
        Identify gaps between candidate skills and required skills.

        Args:
            candidate_skills: List of candidate's skills
            required_skills: List of required skills

        Returns:
            Tuple of (missing_skills, present_skills)
        """
        candidate_skills_lower = [s.lower() for s in candidate_skills]
        required_skills_lower = [s.lower() for s in required_skills]

        present_skills = []
        missing_skills = []

        for skill in required_skills:
            skill_lower = skill.lower()

            # Check for exact match
            if skill_lower in candidate_skills_lower:
                present_skills.append(skill)
                continue

            # Check for partial match
            found = False
            for cand_skill in candidate_skills_lower:
                if skill_lower in cand_skill or cand_skill in skill_lower:
                    present_skills.append(skill)
                    found = True
                    break

            if not found:
                missing_skills.append(skill)

        return missing_skills, present_skills

    def calculate_skill_coverage(self, candidate_skills: List[str], required_skills: List[str]) -> float:
        """
        Calculate percentage of required skills covered by candidate.

        Args:
            candidate_skills: List of candidate's skills
            required_skills: List of required skills

        Returns:
            Coverage percentage
        """
        if not required_skills:
            return 0.0

        missing, present = self.get_skill_gaps(candidate_skills, required_skills)
        coverage = (len(present) / len(required_skills)) * 100

        return round(coverage, 2)

    def get_skill_categories(self, skills: List[str]) -> Dict[str, int]:
        """
        Categorize skills into their respective categories.

        Args:
            skills: List of skills

        Returns:
            Dictionary with category counts
        """
        categories = {category: 0 for category in self.skill_patterns.keys()}

        for skill in skills:
            skill_lower = skill.lower()
            for category, skill_list in self.skill_patterns.items():
                for pattern in skill_list:
                    if pattern in skill_lower:
                        categories[category] += 1
                        break

        return categories

    def generate_skill_summary(self, skills: List[str]) -> str:
        """
        Generate a summary of skills.

        Args:
            skills: List of skills

        Returns:
            Formatted skill summary
        """
        if not skills:
            return "No skills identified"

        categories = self.get_skill_categories(skills)
        total_skills = len(skills)

        summary = f"Total Skills: {total_skills}\n"
        summary += "-" * 30 + "\n"

        for category, count in categories.items():
            if count > 0:
                category_name = category.replace('_', ' ').title()
                percentage = (count / total_skills) * 100
                summary += f"{category_name}: {count} ({percentage:.1f}%)\n"

        return summary