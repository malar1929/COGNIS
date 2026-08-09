"""
COGNIS - Job Description Matcher
Matches resumes against job descriptions with advanced scoring
"""

import re
from collections import Counter
from datetime import datetime


class JDMather:
    """Match resumes against job descriptions"""

    def __init__(self):
        """Initialize the JD matcher"""
        self.importance_weights = {
            'skills': 0.35,
            'experience': 0.25,
            'education': 0.15,
            'achievements': 0.15,
            'certifications': 0.10
        }

    def extract_skills(self, jd_content):
        """Extract required skills from job description"""
        skills = []

        skill_keywords = [
            'python', 'java', 'javascript', 'c', 'c++', 'html', 'css',
            'flask', 'django', 'react', 'node', 'sql', 'mysql',
            'mongodb', 'git', 'github', 'aws', 'docker',
            'kubernetes', 'pycharm', 'vs code', 'google colab'
        ]

        content_lower = jd_content.lower()

        for keyword in skill_keywords:
            if keyword in content_lower:
                skills.append(keyword)

        return list(set(skills))

    # Remove duplicates

    def extract_experience_requirements(self, jd_content):
        """Extract experience requirements from job description"""
        experience_years = 0

        # Look for experience patterns
        patterns = [
            r'(\d+)[\s-]+(\d+)\s+years\s+of\s+experience',
            r'(\d+)\s+years\s+(?:of\s+)?experience',
            r'experience\s+of\s+(\d+)\s+years'
        ]

        for pattern in patterns:
            matches = re.findall(pattern, jd_content, re.IGNORECASE)
            if matches:
                for match in matches:
                    if isinstance(match, tuple):
                        # Range like "5-8 years"
                        try:
                            experience_years = sum(map(int, match)) / len(match)
                        except:
                            continue
                    else:
                        try:
                            experience_years = int(match)
                        except:
                            continue
                    break
                if experience_years > 0:
                    break

        return experience_years

    def extract_education_requirements(self, jd_content):
        """Extract education requirements from job description"""
        education_levels = {
            'phd': 5,
            'doctorate': 5,
            'master': 4,
            'm.s': 4,
            'm.sc': 4,
            'mba': 4,
            'bachelor': 3,
            'b.s': 3,
            'b.sc': 3,
            'associate': 2,
            'certification': 1
        }

        max_level = 0
        content_lower = jd_content.lower()

        for level, value in education_levels.items():
            if level in content_lower:
                max_level = max(max_level, value)

        return max_level

    def calculate_match_score(self, resume_data, jd_skills):
        """
        Calculate overall match score between resume and job description
        Returns score as percentage
        """
        scores = {}

        # 1. Skills match
        candidate_skills = resume_data.get('skills', [])
        if jd_skills and candidate_skills:
            skill_coverage = self._calculate_skill_match(candidate_skills, jd_skills)
            scores['skills'] = skill_coverage
        else:
            scores['skills'] = 0
        # 2. Experience match
        experience_years = resume_data.get('experience_years', 0)

        if experience_years == 0:
            experience_score = 100
        else:
            experience_score = min(100, (experience_years / 5) * 100)

        scores['experience'] = experience_score

        # 3. Education match
        education = resume_data.get('education', [])
        education_score = self._calculate_education_score(education)
        scores['education'] = education_score

        # 4. Achievement quality
        achievements = resume_data.get('achievements', [])
        achievement_score = self._calculate_achievement_score(achievements)
        scores['achievements'] = achievement_score

        # 5. Certification relevance
        certifications = resume_data.get('certifications', [])
        certification_score = self._calculate_certification_score(certifications, jd_skills)
        scores['certifications'] = certification_score

        # Calculate weighted total
        total_score = sum(scores[key] * self.importance_weights[key]
                          for key in self.importance_weights)

        return round(total_score, 2)

    def _calculate_skill_match(self, candidate_skills, required_skills):
        """Calculate skill match percentage"""
        if not required_skills:
            return 0.0

        candidate_skills_lower = [s.lower() for s in candidate_skills]
        required_skills_lower = [s.lower() for s in required_skills]

        matched = 0
        for req_skill in required_skills_lower:
            # Direct match
            if req_skill in candidate_skills_lower:
                matched += 1
            else:
                # Partial match
                for cand_skill in candidate_skills_lower:
                    if req_skill in cand_skill or cand_skill in req_skill:
                        matched += 0.5
                        break

        return (matched / len(required_skills)) * 100

    def _calculate_education_score(self, education):
        """Calculate education score"""
        if not education:
            return 0.0

        # Score based on highest degree
        degree_weights = {
            'phd': 100,
            'doctorate': 100,
            'master': 85,
            'm.s': 85,
            'm.sc': 85,
            'mba': 85,
            'bachelor': 70,
            'b.s': 70,
            'b.sc': 70,
            'associate': 50
        }

        highest_score = 0
        for edu in education:
            degree = edu.get('degree', '').lower()
            for key, weight in degree_weights.items():
                if key in degree:
                    highest_score = max(highest_score, weight)
                    break

        return highest_score

    def _calculate_achievement_score(self, achievements):
        """Calculate achievement quality score"""
        if not achievements:
            return 0.0

        score = 0
        for achievement in achievements:
            # Check for quantifiable metrics
            if re.search(r'\d+%|\$\d+|\d+\s*(?:million|k|thousand)', achievement):
                score += 20
            # Check for impact words
            impact_words = ['increased', 'improved', 'reduced', 'saved', 'generated', 'delivered']
            for word in impact_words:
                if word in achievement.lower():
                    score += 10
                    break
            # Check for leadership
            if 'led' in achievement.lower() or 'managed' in achievement.lower():
                score += 15

        return min(100, score)

    def _calculate_certification_score(self, certifications, jd_skills):
        """Calculate certification relevance score"""
        if not certifications or not jd_skills:
            return 0.0

        score = 0
        for cert in certifications:
            cert_lower = cert.lower()
            for skill in jd_skills:
                if skill.lower() in cert_lower:
                    score += 20
                    break

        return min(100, score)