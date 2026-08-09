"""
COGNIS - Hidden Potential Score
Analyzes growth potential and future capability indicators
"""

import re
from datetime import datetime


class PotentialScoreAnalyzer:
    """Analyze hidden potential and growth indicators"""

    def __init__(self):
        """Initialize potential score analyzer"""
        self.growth_indicators = {
            'learning_agility': 0,
            'adaptability': 0,
            'curiosity': 0,
            'resilience': 0,
            'ambition': 0,
            'innovation': 0,
            'leadership': 0,
            'communication': 0
        }

        self.innovation_patterns = [
            r'created',
            r'developed',
            r'invented',
            r'patent',
            r'published',
            r'designed',
            r'architected',
            r'novel'
        ]

    def calculate_potential_score(self, resume_data):
        """
        Calculate hidden potential score (0-100)
        """
        content = resume_data.get('raw_content', '')
        achievements = resume_data.get('achievements', [])
        skills = resume_data.get('skills', [])
        experience_years = resume_data.get('experience_years', 0)

        # Analyze different potential dimensions
        learning_agility = self._analyze_learning_agility(content, skills)
        adaptability = self._analyze_adaptability(content)
        curiosity = self._analyze_curiosity(content)
        resilience = self._analyze_resilience(content)
        ambition = self._analyze_ambition(content, achievements)
        innovation = self._analyze_innovation(content, achievements)
        leadership = self._analyze_leadership(content, achievements)
        communication = self._analyze_communication(content)

        # Apply experience multiplier (new grads have more growth potential)
        experience_multiplier = max(1, 2 - (experience_years / 10))

        # Calculate weighted score
        scores = {
            'learning_agility': learning_agility * 1.2,
            'adaptability': adaptability * 1.1,
            'curiosity': curiosity * 1.0,
            'resilience': resilience * 1.1,
            'ambition': ambition * 1.3,
            'innovation': innovation * 1.0,
            'leadership': leadership * 1.1,
            'communication': communication * 0.9
        }

        total_score = sum(scores.values()) / len(scores)
        total_score *= experience_multiplier
        total_score = min(100, total_score * 1.2)  # Scale to 100

        return round(total_score, 2)

    def _analyze_learning_agility(self, content, skills):
        """Analyze learning agility indicators"""
        score = 50  # Baseline

        # Check for multiple skill categories
        skill_categories = ['programming', 'design', 'analytics', 'management', 'communication']
        category_count = len(set(skill_categories) & set(skills))
        score += category_count * 5

        # Check for learning-related keywords
        learning_keywords = ['learned', 'training', 'course', 'certification', 'workshop', 'seminar']
        for keyword in learning_keywords:
            if keyword in content.lower():
                score += 5

        # Check for diverse experience
        if len(skills) > 10:
            score += 10

        return min(100, score)

    def _analyze_adaptability(self, content):
        """Analyze adaptability indicators"""
        score = 50

        # Check for experience in different industries
        industries = ['tech', 'finance', 'healthcare', 'education', 'retail']
        industry_count = sum(1 for i in industries if i in content.lower())
        score += industry_count * 5

        # Check for multiple roles
        roles = ['developer', 'designer', 'manager', 'analyst', 'architect']
        role_count = sum(1 for r in roles if r in content.lower())
        score += role_count * 5

        # Check for remote work experience
        if 'remote' in content.lower():
            score += 10

        return min(100, score)

    def _analyze_curiosity(self, content):
        """Analyze curiosity indicators"""
        score = 50

        # Check for exploration
        exploration_terms = ['explored', 'investigated', 'researched', 'studied', 'analyzed']
        for term in exploration_terms:
            if term in content.lower():
                score += 8

        # Check for side projects
        if 'project' in content.lower():
            score += 10
        if 'github' in content.lower():
            score += 10

        # Check for continuous learning
        if 'certification' in content.lower():
            score += 10
        if 'course' in content.lower():
            score += 5

        return min(100, score)

    def _analyze_resilience(self, content):
        """Analyze resilience indicators"""
        score = 50

        # Check for overcoming challenges
        challenge_keywords = ['challenge', 'difficult', 'overcame', 'solved', 'crisis']
        for keyword in challenge_keywords:
            if keyword in content.lower():
                score += 10

        # Check for long tenure at difficult roles
        if 'challenging' in content.lower():
            score += 8

        # Check for recovery from failures
        if 'failed' in content.lower() or 'learned' in content.lower():
            score += 10

        return min(100, score)

    def _analyze_ambition(self, content, achievements):
        """Analyze ambition indicators"""
        score = 50

        # Check for career progression
        if any(level in content.lower() for level in ['senior', 'lead', 'manager', 'director']):
            score += 15

        # Check for promotions
        if 'promoted' in content.lower():
            score += 15

        # Check for impact
        if achievements:
            impact_score = sum(1 for a in achievements if any(word in a.lower()
                                                              for word in
                                                              ['increased', 'improved', 'generated', 'saved']))
            score += impact_score * 3

        # Check for awards
        if 'award' in content.lower() or 'recognized' in content.lower():
            score += 15

        return min(100, score)

    def _analyze_innovation(self, content, achievements):
        """Analyze innovation indicators"""
        score = 50

        # Check for innovation keywords
        for pattern in self.innovation_patterns:
            if pattern in content.lower():
                score += 8

        # Check for patents
        if 'patent' in content.lower():
            score += 20

        # Check for novel solutions
        if 'novel' in content.lower() or 'new' in content.lower():
            score += 10

        # Check for process improvements
        if any(pattern in content.lower() for pattern in ['streamlined', 'optimized', 'automated']):
            score += 10

        return min(100, score)

    def _analyze_leadership(self, content, achievements):
        """Analyze leadership indicators"""
        score = 30

        # Check for leadership keywords
        leadership_terms = ['led', 'managed', 'supervised', 'mentored', 'directed', 'guided', 'coached']
        for term in leadership_terms:
            if term in content.lower():
                score += 8

        # Check for team mentions
        if 'team' in content.lower():
            score += 10

        # Check for responsibility
        if 'responsible' in content.lower():
            score += 5

        # Check for mentorship
        if 'mentor' in content.lower():
            score += 15

        return min(100, score)

    def _analyze_communication(self, content):
        """Analyze communication skills"""
        score = 50

        # Check for writing quality
        sentences = re.findall(r'[^.!?]+[.!?]', content)
        if sentences:
            # Average sentence length
            avg_length = sum(len(s.split()) for s in sentences) / len(sentences)
            if 10 <= avg_length <= 20:  # Good sentence length
                score += 20
            elif avg_length > 30:  # Too long sentences
                score -= 10

        # Check for clear structure
        sections = re.findall(r'^[A-Z][A-Z\s]+:', content, re.MULTILINE)
        if len(sections) >= 3:  # Multiple sections (good structure)
            score += 15

        # Check for presentation skills
        if any(term in content.lower() for term in ['presented', 'presentation', 'speaker', 'conference']):
            score += 15

        return min(100, score)