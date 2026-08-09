"""
COGNIS - Consistency Fingerprint Engine
Analyzes behavioral and career consistency patterns

This module evaluates candidate consistency across multiple dimensions:
- Career trajectory consistency
- Skill continuity and development
- Job stability patterns
- Achievement patterns
- Role progression
- Industry focus
- Work rhythm and patterns
"""

import re
import math
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from collections import Counter, defaultdict


class ConsistencyEngine:
    """
    Analyzes consistency in candidate's career and behavioral patterns.

    The engine evaluates 7 key consistency factors:
    1. Career Trajectory - Logical progression in roles
    2. Skill Continuity - Consistent skill development
    3. Job Stability - Tenure and employment patterns
    4. Achievement Pattern - Consistent achievement delivery
    5. Role Progression - Upward career movement
    6. Industry Focus - Consistent industry alignment
    7. Work Rhythm - Predictable work patterns
    """

    def __init__(self):
        """Initialize the consistency engine with pattern definitions."""
        # Weight factors for each consistency dimension
        self.consistency_weights = {
            'career_trajectory': 1.1,
            'skill_continuity': 0.9,
            'job_stability': 1.2,
            'achievement_pattern': 0.8,
            'role_progression': 1.1,
            'industry_focus': 0.9,
            'work_rhythm': 1.0
        }

        # Seniority levels for role progression analysis
        self.seniority_levels = {
            'intern': 1,
            'junior': 2,
            'associate': 3,
            'engineer': 3,
            'developer': 3,
            'analyst': 3,
            'senior': 4,
            'lead': 5,
            'principal': 6,
            'staff': 5,
            'manager': 5,
            'senior manager': 6,
            'director': 7,
            'vp': 8,
            'vice president': 8,
            'c-level': 9,
            'chief': 9,
            'cto': 9,
            'cfo': 9,
            'ceo': 9,
            'founder': 8,
            'co-founder': 8
        }

        # Skill clusters for continuity analysis
        self.skill_clusters = {
            'frontend': ['react', 'angular', 'vue', 'html', 'css', 'javascript',
                         'typescript', 'next.js', 'nuxt', 'svelte', 'bootstrap'],
            'backend': ['python', 'java', 'node', 'django', 'flask', 'spring',
                        'express', 'php', 'ruby', 'rails', 'c#', 'asp.net', 'go'],
            'data': ['sql', 'mongodb', 'postgresql', 'redis', 'elasticsearch',
                     'cassandra', 'dynamodb', 'mysql', 'oracle', 'hadoop', 'spark'],
            'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins',
                      'terraform', 'cloudformation', 'ansible', 'puppet', 'chef'],
            'devops': ['jenkins', 'docker', 'kubernetes', 'aws', 'azure', 'git',
                       'ci/cd', 'terraform', 'ansible', 'prometheus', 'grafana'],
            'ai_ml': ['tensorflow', 'pytorch', 'scikit-learn', 'keras', 'numpy',
                      'pandas', 'opencv', 'nlp', 'deep learning', 'machine learning'],
            'mobile': ['swift', 'kotlin', 'react native', 'flutter', 'android',
                       'ios', 'xcode', 'android studio'],
            'ux_design': ['figma', 'sketch', 'adobe xd', 'photoshop', 'illustrator',
                          'ui/ux', 'prototype', 'wireframe', 'user research'],
            'management': ['agile', 'scrum', 'project management', 'product management',
                           'leadership', 'mentoring', 'coaching', 'strategic planning']
        }

        # Industry categories for focus analysis
        self.industries = {
            'tech_software': ['software', 'saas', 'cloud', 'ai', 'tech', 'it', 'digital'],
            'finance': ['finance', 'banking', 'investment', 'insurance', 'financial'],
            'healthcare': ['health', 'medical', 'biotech', 'pharma', 'healthcare'],
            'education': ['education', 'university', 'school', 'academic', 'teaching'],
            'retail': ['retail', 'ecommerce', 'consumer', 'shopping', 'commerce'],
            'manufacturing': ['manufacturing', 'industrial', 'automotive', 'engineering'],
            'consulting': ['consulting', 'advisory', 'strategy', 'professional services'],
            'media': ['media', 'publishing', 'entertainment', 'broadcasting', 'content']
        }

        # Achievement style patterns
        self.achievement_styles = {
            'quantitative': r'\d+%|\$\d+|\d+\s*(?:million|k|thousand|billion)',
            'leadership': r'\b(?:led|managed|mentored|supervised|guided|coached|directed|oversaw)\b',
            'innovation': r'\b(?:created|developed|designed|innovated|patent|invented|pioneered)\b',
            'improvement': r'\b(?:improved|enhanced|optimized|streamlined|reduced|increased|boosted)\b',
            'collaboration': r'\b(?:collaborated|partnered|team|together|cross-functional)\b'
        }

        # Career progression keywords
        self.progression_keywords = [
            'intern', 'junior', 'associate', 'senior', 'lead',
            'manager', 'director', 'vp', 'vice president', 'chief', 'cto', 'ceo'
        ]

        # Red flags for inconsistency
        self.inconsistency_indicators = {
            'frequent_jobs': r'\b(\d+)\s*(?:months|month|years?)\s*at\s+[A-Z]',
            'gaps': r'gap|break|sabbatical|leave of absence',
            'regression': r'\b(?:demoted|downgraded|step down)\b',
            'unclear_progression': r'\b(?:various|multiple|diverse)\s+roles\b'
        }

    def calculate_consistency(self, resume_content: str) -> float:
        """
        Calculate overall consistency score (0-100).

        Args:
            resume_content: Raw resume text

        Returns:
            Overall consistency score
        """
        # Extract structured information
        years = self._extract_years(resume_content)
        skills = self._extract_skills_list(resume_content)
        roles = self._extract_roles(resume_content)
        achievements = self._extract_achievement_patterns(resume_content)
        companies = self._extract_companies(resume_content)

        # Calculate individual consistency scores
        scores = {
            'career_trajectory': self._analyze_career_trajectory(roles, years),
            'skill_continuity': self._analyze_skill_continuity(skills),
            'job_stability': self._analyze_job_stability(years, companies),
            'achievement_pattern': self._analyze_achievement_pattern(achievements),
            'role_progression': self._analyze_role_progression(roles),
            'industry_focus': self._analyze_industry_focus(companies, skills),
            'work_rhythm': self._analyze_work_rhythm(years)
        }

        # Apply weights
        weighted_score = 0
        total_weight = 0

        for factor, score in scores.items():
            weight = self.consistency_weights.get(factor, 1.0)
            weighted_score += score * weight
            total_weight += weight

        # Calculate weighted average
        final_score = weighted_score / total_weight if total_weight > 0 else 0

        # Apply penalties for inconsistency indicators
        penalty = self._calculate_inconsistency_penalty(resume_content)
        final_score = max(0, min(100, final_score - penalty))

        return round(final_score, 2)

    def _extract_years(self, content: str) -> List[int]:
        """
        Extract all years mentioned in the resume.

        Args:
            content: Resume text

        Returns:
            List of years
        """
        year_pattern = r'\b(19|20)\d{2}\b'
        years = re.findall(year_pattern, content)
        years = [int(year) for year in years if 1980 <= int(year) <= datetime.now().year + 1]
        return sorted(list(set(years)))

    def _extract_skills_list(self, content: str) -> List[str]:
        """
        Extract skills from resume content.
        """

        skills = []
        content_lower = content.lower()

        # Extract from skill clusters
        for cluster, skill_list in self.skill_clusters.items():
            for skill in skill_list:
                if skill.lower() in content_lower:
                    skills.append(skill)

        return sorted(list(set(skills)))

    def _extract_roles(self, content: str) -> List[str]:
        """
        Extract job roles from resume.

        Args:
            content: Resume text

        Returns:
            List of roles
        """
        roles = []

        # Look for role patterns
        role_patterns = [
            r'(?:Senior|Lead|Principal|Junior|Associate|Staff|Principal)?\s*([A-Z][a-zA-Z\s]+?)\s+(?:at|with|for|\||,)',
            r'([A-Z][a-zA-Z\s]+?)\s+(?:Engineer|Developer|Manager|Architect|Analyst|Consultant|Designer|Scientist)'
        ]

        for pattern in role_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                role = match.strip()
                if role and len(role) > 2:
                    roles.append(role)

        # Look for roles in experience entries
        experience_section = self._find_section(content, ['experience', 'work experience', 'employment'])
        if experience_section:
            lines = experience_section.split('\n')
            for line in lines:
                # Look for title patterns
                if '|' in line or ',' in line or 'at' in line:
                    parts = re.split(r'[|,]', line)
                    if parts:
                        first_part = parts[0].strip()
                        if first_part and len(first_part) > 2:
                            roles.append(first_part)

        # Remove duplicates and limit
        return list(dict.fromkeys(roles))[:10]

    def _extract_achievement_patterns(self, content: str) -> List[str]:
        """
        Extract achievement patterns from resume.

        Args:
            content: Resume text

        Returns:
            List of achievement statements
        """
        achievements = []

        # Look for bullet points with action words
        bullet_pattern = r'[•\-*]\s*([^.!?]*(?:increased|improved|reduced|saved|generated|delivered|led|built|designed|created|developed|implemented|managed|mentored|optimized)[^.!?]*[.!?]?)'
        matches = re.findall(bullet_pattern, content, re.IGNORECASE)
        achievements.extend([m.strip() for m in matches if len(m.strip()) > 15])

        # Look for quantified achievements
        quantified_pattern = r'\b(?:increased|improved|reduced|saved|generated|boosted)\s+[^.!?]*?(?:\d+%|\$\d+|\d+\s*(?:million|k|thousand))[^.!?]*?[.!?]'
        matches = re.findall(quantified_pattern, content, re.IGNORECASE)
        achievements.extend([m.strip() for m in matches if len(m.strip()) > 15])

        # Look for leadership achievements
        leadership_pattern = r'\b(?:led|managed|mentored|supervised|guided|directed)\s+[^.!?]*?[.!?]'
        matches = re.findall(leadership_pattern, content, re.IGNORECASE)
        achievements.extend([m.strip() for m in matches if len(m.strip()) > 15])

        # Remove duplicates
        return list(dict.fromkeys(achievements))[:15]

    def _extract_companies(self, content: str) -> List[str]:
        """
        Extract company names from resume.

        Args:
            content: Resume text

        Returns:
            List of company names
        """
        companies = []

        # Look for company patterns
        company_patterns = [
            r'(?:at|with|for)\s+([A-Z][a-zA-Z\s]+(?:Inc|Corp|LLC|Company|Corporation|Technologies|Systems|Solutions|Labs|Ventures|Group|Holdings))',
            r'(?:at|with|for)\s+([A-Z][a-zA-Z\s]+(?:University|College|Institute|School)?)',
            r'([A-Z][a-zA-Z\s]+(?:Inc|Corp|LLC|Company|Corporation|Technologies|Systems|Solutions))'
        ]

        for pattern in company_patterns:
            matches = re.findall(pattern, content)
            companies.extend([m.strip() for m in matches if m.strip()])

        # Look for companies in experience section
        exp_section = self._find_section(content, ['experience', 'work experience'])
        if exp_section:
            lines = exp_section.split('\n')
            for line in lines:
                # Look for "at Company" pattern
                if 'at ' in line:
                    parts = line.split('at ')
                    if len(parts) > 1:
                        company = parts[1].split('|')[0].split(',')[0].strip()
                        if company and len(company) > 2:
                            companies.append(company)

        return list(dict.fromkeys(companies))[:10]

    def _find_section(self, content: str, headers: List[str]) -> Optional[str]:
        """
        Find a specific section in the resume.

        Args:
            content: Resume text
            headers: List of section header variations

        Returns:
            Section text or None
        """
        content_lower = content.lower()

        for header in headers:
            pattern = r'^' + re.escape(header) + r'[:\s]'
            match = re.search(pattern, content_lower, re.MULTILINE)
            if match:
                start_pos = match.start()
                end_pos = self._find_next_section_start(content, start_pos + len(header))
                return content[start_pos:end_pos].strip()

        return None

    def _find_next_section_start(self, content: str, start_pos: int) -> int:
        """
        Find the start of the next section.

        Args:
            content: Resume text
            start_pos: Current position

        Returns:
            Position of next section or end of content
        """
        content_lower = content.lower()

        # Common section headers
        all_headers = []
        for headers in [
            ['experience', 'work experience', 'employment'],
            ['education', 'academic'],
            ['skills', 'technical skills'],
            ['certifications', 'certification'],
            ['projects', 'project experience'],
            ['achievements', 'awards']
        ]:
            for header in headers:
                pattern = r'^' + re.escape(header) + r'[:\s]'
                for match in re.finditer(pattern, content_lower, re.MULTILINE):
                    if match.start() > start_pos:
                        all_headers.append(match.start())

        return min(all_headers) if all_headers else len(content)

    def _analyze_career_trajectory(self, roles: List[str], years: List[int]) -> float:
        """
        Analyze career trajectory consistency.

        Args:
            roles: List of job roles
            years: List of years

        Returns:
            Trajectory score (0-100)
        """
        if not roles or len(roles) < 2:
            return 70  # Default for minimal data

        # Map roles to seniority levels
        seniority_scores = []
        for role in roles:
            role_lower = role.lower()
            level = 0
            for level_name, level_value in self.seniority_levels.items():
                if level_name in role_lower:
                    level = max(level, level_value)
            seniority_scores.append(level)

        # Check for logical progression
        progression_score = 50  # Base score
        valid_progressions = 0

        for i in range(1, len(seniority_scores)):
            if seniority_scores[i] >= seniority_scores[i - 1]:
                valid_progressions += 1
                # Bonus for significant jumps
                if seniority_scores[i] - seniority_scores[i - 1] >= 3:
                    progression_score += 5
                else:
                    progression_score += 3
            else:
                # Penalty for regression
                progression_score -= 10

        # Calculate progression ratio
        if len(seniority_scores) > 1:
            ratio = valid_progressions / (len(seniority_scores) - 1)
            progression_score = 30 + (ratio * 70)

        # Check for consistency with years
        if years and len(years) > 1:
            year_ranges = max(years) - min(years)
            if year_ranges > 0:
                # Check if role progression matches time span
                if len(roles) >= year_ranges / 2:  # At least one role every 2 years
                    progression_score += 10

        return max(0, min(100, progression_score))

    def _analyze_skill_continuity(self, skills: List[str]) -> float:
        """
        Analyze skill continuity and development consistency.

        Args:
            skills: List of skills

        Returns:
            Continuity score (0-100)
        """
        if not skills:
            return 50

        # Check cluster distribution
        cluster_counts = defaultdict(int)
        for skill in skills:
            skill_lower = skill.lower()
            for cluster, cluster_skills in self.skill_clusters.items():
                for cluster_skill in cluster_skills:
                    if cluster_skill in skill_lower or skill_lower in cluster_skill:
                        cluster_counts[cluster] += 1
                        break

        # Calculate focus score
        total_skills = len(skills)
        if total_skills == 0:
            return 50

        # Determine number of clusters with significant skill presence
        significant_clusters = sum(1 for count in cluster_counts.values() if count >= 2)

        if significant_clusters == 0:
            focus_score = 50
        elif significant_clusters == 1:
            focus_score = 90  # Very focused
        elif significant_clusters == 2:
            focus_score = 80  # Good balance
        elif significant_clusters == 3:
            focus_score = 70  # Moderate focus
        else:
            focus_score = 60  # Too scattered

        # Bonus for depth in primary cluster
        if cluster_counts:
            max_count = max(cluster_counts.values())
            depth_bonus = min(10, max_count * 2)
            focus_score += depth_bonus

        # Check for skill progression (from basic to advanced)
        progression_indicators = []
        for skill in skills:
            if any(prefix in skill.lower() for prefix in ['advanced', 'expert', 'professional']):
                progression_indicators.append(skill)

        if progression_indicators:
            focus_score += min(10, len(progression_indicators) * 3)

        return min(100, focus_score)

    def _analyze_job_stability(self, years: List[int], companies: List[str]) -> float:
        """
        Analyze job stability and tenure patterns.

        Args:
            years: List of years from resume
            companies: List of company names

        Returns:
            Stability score (0-100)
        """
        if not years or len(years) < 2:
            return 70  # Default for minimal data

        # Calculate average tenure
        sorted_years = sorted(years)
        tenures = []

        for i in range(1, len(sorted_years)):
            tenure = sorted_years[i] - sorted_years[i - 1]
            if 1 <= tenure <= 8:  # Reasonable tenure range
                tenures.append(tenure)

        if not tenures:
            return 50  # No clear tenure pattern

        avg_tenure = sum(tenures) / len(tenures)
        max_tenure = max(tenures) if tenures else 0

        # Score based on average tenure
        if avg_tenure >= 4:
            stability_score = 90  # Very stable (4+ years average)
        elif avg_tenure >= 3:
            stability_score = 80
        elif avg_tenure >= 2:
            stability_score = 65
        elif avg_tenure >= 1.5:
            stability_score = 50
        else:
            stability_score = 35  # Job hopper

        # Bonus for long tenure
        if max_tenure >= 5:
            stability_score = min(100, stability_score + 10)
        elif max_tenure >= 3:
            stability_score = min(100, stability_score + 5)

        # Check if multiple companies show consistency
        if companies and len(companies) > 1:
            # Penalty for too many short-term companies
            if len(companies) > len(years) / 2:
                stability_score = max(0, stability_score - 10)

        # Check for company variety
        if companies and len(companies) >= 3:
            # If all in same industry, bonus
            company_industries = [self._detect_industry(company) for company in companies]
            if len(set(company_industries)) == 1 and company_industries[0] is not None:
                stability_score = min(100, stability_score + 10)

        return max(0, min(100, stability_score))

    def _analyze_achievement_pattern(self, achievements: List[str]) -> float:
        """
        Analyze consistency in achievement patterns.

        Args:
            achievements: List of achievement statements

        Returns:
            Achievement pattern score (0-100)
        """
        if not achievements:
            return 50

        # Style distribution analysis
        style_counts = {style: 0 for style in self.achievement_styles}

        for achievement in achievements:
            achievement_lower = achievement.lower()
            for style, pattern in self.achievement_styles.items():
                if re.search(pattern, achievement_lower, re.IGNORECASE):
                    style_counts[style] += 1

        total_achievements = len(achievements)

        # Calculate style dominance
        max_style = max(style_counts.values()) if style_counts else 0
        active_styles = sum(1 for count in style_counts.values() if count > 0)

        if total_achievements == 0:
            return 50

        # Score based on style consistency
        if max_style / total_achievements >= 0.7:
            # One dominant style - very consistent
            score = 90
        elif max_style / total_achievements >= 0.5:
            # One primary style - moderately consistent
            score = 75
        elif active_styles >= 3:
            # Multiple styles - diverse but may lack focus
            score = 65
        else:
            score = 60

        # Bonus for quantified achievements (higher value)
        quantified_count = sum(1 for a in achievements if re.search(r'\d+%|\$\d+|\d+\s*(?:million|k)', a))
        if quantified_count / total_achievements >= 0.5:
            score = min(100, score + 10)

        # Bonus for variety in achievement types
        if active_styles >= 3:
            score = min(100, score + 5)

        return max(0, min(100, score))

    def _analyze_role_progression(self, roles: List[str]) -> float:
        """
        Analyze role progression consistency.

        Args:
            roles: List of job roles

        Returns:
            Role progression score (0-100)
        """
        if not roles or len(roles) < 2:
            return 70

        # Track progression patterns
        progression_levels = []
        for role in roles:
            role_lower = role.lower()
            level = 0
            for level_name, level_value in self.seniority_levels.items():
                if level_name in role_lower:
                    level = max(level, level_value)
            progression_levels.append(level)

        if not progression_levels:
            return 60

        # Calculate progression ratio
        valid_progressions = 0
        total_comparisons = 0

        for i in range(1, len(progression_levels)):
            total_comparisons += 1
            if progression_levels[i] >= progression_levels[i - 1]:
                valid_progressions += 1

        if total_comparisons == 0:
            return 70

        progression_ratio = valid_progressions / total_comparisons

        # Score based on progression ratio
        if progression_ratio >= 0.9:
            score = 95  # Excellent progression
        elif progression_ratio >= 0.7:
            score = 85
        elif progression_ratio >= 0.5:
            score = 70
        elif progression_ratio >= 0.3:
            score = 55
        else:
            score = 40  # Inconsistent regression

        # Check for clear career path
        senior_roles = sum(1 for level in progression_levels if level >= 4)
        if senior_roles >= 2:
            score = min(100, score + 10)

        # Check for role variety
        unique_roles = len(set(roles))
        if unique_roles >= 3 and unique_roles <= 5:
            # Good variety but not too scattered
            score = min(100, score + 5)
        elif unique_roles > 5:
            # Too many different roles
            score = max(0, score - 5)

        return max(0, min(100, score))

    def _analyze_industry_focus(self, companies: List[str], skills: List[str]) -> float:
        """
        Analyze industry focus consistency.

        Args:
            companies: List of company names
            skills: List of skills

        Returns:
            Industry focus score (0-100)
        """
        if not companies and not skills:
            return 60

        score = 50

        # Detect industries from companies
        company_industries = []
        for company in companies:
            industry = self._detect_industry(company)
            if industry:
                company_industries.append(industry)

        if company_industries:
            # Check industry concentration
            industry_counts = Counter(company_industries)
            most_common = industry_counts.most_common(1)[0] if industry_counts else (None, 0)

            if most_common[0]:
                concentration = most_common[1] / len(company_industries)
                if concentration >= 0.8:
                    score = 90  # High focus
                elif concentration >= 0.6:
                    score = 80
                elif concentration >= 0.4:
                    score = 70
                else:
                    score = 60  # Diverse

        # Check if skills align with detected industry
        if company_industries and skills:
            primary_industry = most_common[0] if company_industries else None
            if primary_industry:
                aligned_skills = 0
                for skill in skills:
                    skill_lower = skill.lower()
                    industry_keywords = self.industries.get(primary_industry, [])
                    if any(keyword in skill_lower for keyword in industry_keywords):
                        aligned_skills += 1

                if aligned_skills / len(skills) >= 0.5:
                    score = min(100, score + 10)

        return max(0, min(100, score))

    def _detect_industry(self, text: str) -> Optional[str]:
        """
        Detect industry from text.

        Args:
            text: Text to analyze

        Returns:
            Detected industry or None
        """
        text_lower = text.lower()

        for industry, keywords in self.industries.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return industry

        return None

    def _analyze_work_rhythm(self, years: List[int]) -> float:
        """
        Analyze work rhythm consistency.

        Args:
            years: List of years from resume

        Returns:
            Work rhythm score (0-100)
        """
        if not years or len(years) < 3:
            return 70

        sorted_years = sorted(years)

        # Calculate gaps between years
        gaps = []
        for i in range(1, len(sorted_years)):
            gap = sorted_years[i] - sorted_years[i - 1]
            gaps.append(gap)

        if not gaps:
            return 70

        # Analyze gap patterns
        avg_gap = sum(gaps) / len(gaps)
        max_gap = max(gaps)

        # Score based on gap consistency
        if avg_gap <= 1.5:
            score = 90  # Consistent employment (no gaps)
        elif avg_gap <= 2.5:
            score = 80
        elif avg_gap <= 3.5:
            score = 65
        else:
            score = 50  # Significant gaps

        # Penalty for large gaps
        if max_gap > 5:
            score = max(0, score - 15)
        elif max_gap > 3:
            score = max(0, score - 5)

        # Check for pattern in gaps
        gap_variance = sum((g - avg_gap) ** 2 for g in gaps) / len(gaps) if gaps else 0
        if gap_variance > 4:
            score = max(0, score - 10)  # Inconsistent rhythm

        # Bonus for regular pattern (no significant gaps)
        if all(g <= 2 for g in gaps):
            score = min(100, score + 10)

        return max(0, min(100, score))

    def _calculate_inconsistency_penalty(self, content: str) -> float:
        """
        Calculate penalty for inconsistency indicators.

        Args:
            content: Resume text

        Returns:
            Penalty score (0-30)
        """
        penalty = 0
        content_lower = content.lower()

        # Check for job hopping patterns
        frequent_jobs = re.findall(r'\b(\d+)\s*(?:months|month)\s+(?:at|with|for)', content_lower)
        if frequent_jobs:
            short_tenures = [int(m) for m in frequent_jobs if int(m) < 12]
            if len(short_tenures) >= 3:
                penalty += 10
            elif len(short_tenures) >= 2:
                penalty += 5

        # Check for unexplained gaps
        gap_patterns = ['gap', 'break', 'sabbatical', 'leave of absence', 'unemployed']
        gaps_found = sum(1 for pattern in gap_patterns if pattern in content_lower)
        if gaps_found >= 2:
            penalty += 5
        elif gaps_found >= 1:
            penalty += 3

        # Check for role regression
        if 'demoted' in content_lower or 'downgraded' in content_lower:
            penalty += 10

        # Check for unclear progression
        if 'various roles' in content_lower or 'multiple positions' in content_lower:
            penalty += 3

        # Check for company hopping without progression
        companies = self._extract_companies(content)
        if len(companies) >= 4:
            roles = self._extract_roles(content)
            if len(roles) < len(companies):
                penalty += 5

        # Cap penalty at 30
        return min(30, penalty)

    def generate_consistency_report(self, resume_content: str) -> Dict[str, Any]:
        """
        Generate comprehensive consistency report.

        Args:
            resume_content: Resume text

        Returns:
            Dictionary with consistency analysis results
        """
        # Calculate all scores
        years = self._extract_years(resume_content)
        skills = self._extract_skills_list(resume_content)
        roles = self._extract_roles(resume_content)
        achievements = self._extract_achievement_patterns(resume_content)
        companies = self._extract_companies(resume_content)

        scores = {
            'career_trajectory': self._analyze_career_trajectory(roles, years),
            'skill_continuity': self._analyze_skill_continuity(skills),
            'job_stability': self._analyze_job_stability(years, companies),
            'achievement_pattern': self._analyze_achievement_pattern(achievements),
            'role_progression': self._analyze_role_progression(roles),
            'industry_focus': self._analyze_industry_focus(companies, skills),
            'work_rhythm': self._analyze_work_rhythm(years)
        }

        overall_score = self.calculate_consistency(resume_content)

        # Generate detailed report
        report = {
            'overall_score': overall_score,
            'factor_scores': scores,
            'strengths': self._identify_consistency_strengths(scores),
            'weaknesses': self._identify_consistency_weaknesses(scores),
            'recommendations': self._generate_consistency_recommendations(scores),
            'raw_data': {
                'years_found': years,
                'skills_found': skills,
                'roles_found': roles,
                'achievements_found': achievements,
                'companies_found': companies
            }
        }

        return report

    def _identify_consistency_strengths(self, scores: Dict[str, float]) -> List[str]:
        """
        Identify consistency strengths.

        Args:
            scores: Dictionary of factor scores

        Returns:
            List of strength descriptions
        """
        strengths = []

        if scores.get('job_stability', 0) >= 80:
            strengths.append("Strong job stability with consistent tenure patterns")

        if scores.get('skill_continuity', 0) >= 80:
            strengths.append("Excellent skill continuity and focused expertise")

        if scores.get('career_trajectory', 0) >= 80:
            strengths.append("Clear and logical career progression trajectory")

        if scores.get('role_progression', 0) >= 80:
            strengths.append("Consistent upward role progression")

        if scores.get('achievement_pattern', 0) >= 80:
            strengths.append("Strong and consistent achievement delivery")

        if scores.get('industry_focus', 0) >= 80:
            strengths.append("Focused industry specialization")

        if scores.get('work_rhythm', 0) >= 80:
            strengths.append("Consistent and stable work rhythm")

        if not strengths:
            strengths.append("Adequate consistency across most factors")

        return strengths

    def _identify_consistency_weaknesses(self, scores: Dict[str, float]) -> List[str]:
        """
        Identify consistency weaknesses.

        Args:
            scores: Dictionary of factor scores

        Returns:
            List of weakness descriptions
        """
        weaknesses = []

        if scores.get('job_stability', 0) < 50:
            weaknesses.append("Potential job-hopping pattern detected")

        if scores.get('skill_continuity', 0) < 50:
            weaknesses.append("Skill set appears scattered or inconsistent")

        if scores.get('career_trajectory', 0) < 50:
            weaknesses.append("Career progression lacks clear direction")

        if scores.get('role_progression', 0) < 50:
            weaknesses.append("Role progression is unclear or inconsistent")

        if scores.get('achievement_pattern', 0) < 50:
            weaknesses.append("Inconsistent achievement patterns")

        if scores.get('industry_focus', 0) < 50:
            weaknesses.append("Limited industry focus or specialization")

        if scores.get('work_rhythm', 0) < 50:
            weaknesses.append("Irregular work pattern with gaps or volatility")

        if not weaknesses:
            weaknesses.append("No significant consistency issues identified")

        return weaknesses

    def _generate_consistency_recommendations(self, scores: Dict[str, float]) -> List[str]:
        """
        Generate recommendations based on consistency analysis.

        Args:
            scores: Dictionary of factor scores

        Returns:
            List of recommendations
        """
        recommendations = []

        if scores.get('job_stability', 0) < 60:
            recommendations.append("Consider longer tenure in future roles to demonstrate stability")

        if scores.get('skill_continuity', 0) < 60:
            recommendations.append("Focus on developing expertise in complementary skill areas")

        if scores.get('career_trajectory', 0) < 60:
            recommendations.append("Develop a clearer career narrative and progression path")

        if scores.get('role_progression', 0) < 60:
            recommendations.append("Aim for roles with clear advancement opportunities")

        if scores.get('achievement_pattern', 0) < 60:
            recommendations.append("Work on delivering more consistent, quantifiable achievements")

        if scores.get('industry_focus', 0) < 60:
            recommendations.append("Consider specializing in a specific industry vertical")

        if scores.get('work_rhythm', 0) < 60:
            recommendations.append("Maintain consistent employment with minimal gaps")

        if not recommendations:
            recommendations.append("Continue maintaining consistent career patterns")

        return recommendations[:5]  # Return top 5 recommendations

    def format_consistency_report(self, report: Dict[str, Any]) -> str:
        """
        Format consistency report as readable text.

        Args:
            report: Consistency report dictionary

        Returns:
            Formatted report string
        """
        output = []
        output.append("=" * 70)
        output.append("CONSISTENCY FINGERPRINT REPORT")
        output.append("=" * 70)
        output.append("")
        output.append(f"Overall Consistency Score: {report['overall_score']:.1f}%")
        output.append("")
        output.append("FACTOR SCORES:")
        output.append("-" * 40)

        for factor, score in report['factor_scores'].items():
            factor_label = factor.replace('_', ' ').title()
            output.append(f"{factor_label:20s}: {score:5.1f}%")

        output.append("")
        output.append("STRENGTHS:")
        output.append("-" * 40)
        for strength in report['strengths']:
            output.append(f"  ✓ {strength}")

        output.append("")
        output.append("AREAS FOR IMPROVEMENT:")
        output.append("-" * 40)
        for weakness in report['weaknesses']:
            output.append(f"  ○ {weakness}")

        output.append("")
        output.append("RECOMMENDATIONS:")
        output.append("-" * 40)
        for i, recommendation in enumerate(report['recommendations'], 1):
            output.append(f"  {i}. {recommendation}")

        output.append("")
        output.append("=" * 70)

        return "\n".join(output)