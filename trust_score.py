"""
COGNIS - Trust Score Analyzer
Evaluates candidate credibility and trustworthiness
"""

import re
from collections import Counter


class TrustScoreAnalyzer:
    """Analyze trustworthiness of resume content"""

    def __init__(self):
        """Initialize trust score analyzer"""
        self.trust_indicators = {
            'achievements': 20,  # Quantifiable achievements
            'specificity': 15,  # Specific details
            'consistency': 15,  # Consistent narrative
            'verifiability': 15,  # Verifiable claims
            'humility': 10,  # Appropriate self-promotion
            'professionalism': 10,  # Professional language
            'references': 5,  # Reference mentions
            'portfolio': 5,  # Portfolio/work samples
            'publications': 5  # Published work
        }

        self.red_flags = [
            'overpromise', 'unrealistic', 'exaggerated',
            'inconsistent', 'vague', 'unsupported',
            'superlative', 'guarantee', 'best', 'perfect'
        ]

    def calculate_trust_score(self, resume_content):
        """
        Calculate overall trust score (0-100)
        """
        scores = {}

        # 1. Achievement quality
        achievements = self._extract_achievements(resume_content)
        scores['achievements'] = self._score_achievements(achievements)

        # 2. Specificity of claims
        scores['specificity'] = self._score_specificity(resume_content)

        # 3. Narrative consistency
        scores['consistency'] = self._score_consistency(resume_content)

        # 4. Verifiability
        scores['verifiability'] = self._score_verifiability(resume_content)

        # 5. Humility (appropriate self-promotion)
        scores['humility'] = self._score_humility(resume_content)

        # 6. Professionalism
        scores['professionalism'] = self._score_professionalism(resume_content)

        # 7. References
        scores['references'] = self._score_references(resume_content)

        # 8. Portfolio presence
        scores['portfolio'] = self._score_portfolio(resume_content)

        # 9. Publications
        scores['publications'] = self._score_publications(resume_content)

        # Calculate weighted total
        total_score = sum(scores[key] * (self.trust_indicators.get(key, 10) / 100)
                          for key in scores)

        # Apply red flag penalties
        red_flag_penalty = self._calculate_red_flag_penalty(resume_content)
        total_score = max(0, total_score - red_flag_penalty)

        return round(total_score, 2)

    def _extract_achievements(self, content):
        """Extract achievement statements"""
        achievements = []

        # Look for achievement patterns
        patterns = [
            r'(?:increased|improved|reduced|saved|generated|delivered|led|built|designed|implemented|created|developed|launched|managed|mentored|optimized|streamlined|accelerated|boosted)\s+[^.!?]+[.!?]',
            r'[•\-*]\s*(?:increased|improved|reduced|saved|generated|delivered|led|built|designed|implemented|created|developed|launched|managed|mentored|optimized|streamlined|accelerated|boosted)\s+[^.!?]+[.!?]'
        ]

        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            achievements.extend(matches)

        return achievements

    def _score_achievements(self, achievements):
        """Score quality and quantity of achievements"""
        if not achievements:
            return 0.0

        score = 0
        for achievement in achievements:
            # Has quantifiable metrics (higher score)
            if re.search(r'\d+%|\$\d+|\d+\s*(?:million|k|thousand)', achievement):
                score += 15
            # Has impact indicators
            impact_words = ['increased', 'improved', 'reduced', 'saved', 'generated', 'delivered']
            if any(word in achievement.lower() for word in impact_words):
                score += 10
            # Has leadership indicators
            if 'led' in achievement.lower() or 'managed' in achievement.lower():
                score += 10

        return min(100, score / len(achievements) * 20)

    def _score_specificity(self, content):
        """Score how specific the claims are"""
        # Count specific details
        details = 0

        # Specific numbers
        numbers = re.findall(r'\d+', content)
        if numbers:
            details += len(numbers) * 0.5

        # Specific technologies/ tools
        tech_keywords = ['python', 'java', 'aws', 'docker', 'kubernetes', 'sql', 'react', 'angular']
        for keyword in tech_keywords:
            if keyword.lower() in content.lower():
                details += 2

        # Specific metrics
        metrics = ['%', '$', 'million', 'thousand', 'billion', 'increase', 'decrease', 'growth']
        for metric in metrics:
            if metric in content.lower():
                details += 3

        return min(100, details * 2)

    def _score_consistency(self, content):
        """Score narrative consistency"""
        # Check for contradictory statements
        contradictions = 0

        # Check for timeline inconsistencies
        years = re.findall(r'\b(19|20)\d{2}\b', content)
        if years:
            years = [int(y) for y in years]
            # Check for impossible sequences
            for i in range(1, len(years)):
                if years[i] < years[i - 1] and (years[i - 1] - years[i]) > 10:
                    contradictions += 5

        # Check for role progression
        roles = ['intern', 'junior', 'senior', 'lead', 'manager', 'director', 'vp']
        role_positions = []
        content_lower = content.lower()
        for role in roles:
            if role in content_lower:
                role_positions.append(roles.index(role))

        # Check if progression is logical
        if role_positions and len(role_positions) > 1:
            for i in range(1, len(role_positions)):
                if role_positions[i] < role_positions[i - 1]:
                    contradictions += 3

        return max(0, 100 - contradictions * 3)

    def _score_verifiability(self, content):
        """Score how verifiable the claims are"""
        verifiable_elements = 0

        # LinkedIn presence
        if 'linkedin' in content.lower():
            verifiable_elements += 20

        # GitHub/portfolio presence
        if 'github' in content.lower() or 'gitlab' in content.lower():
            verifiable_elements += 20

        # Company names
        companies = re.findall(
            r'\b([A-Z][a-zA-Z]+)\s+(?:Inc|Corp|LLC|Company|Corporation|Technologies|Systems|Solutions)\b', content)
        if companies:
            verifiable_elements += min(len(companies) * 5, 20)

        # Project names
        if 'project' in content.lower():
            verifiable_elements += 10

        # Publication mentions
        if 'published' in content.lower() or 'publication' in content.lower():
            verifiable_elements += 10

        # Conference mentions
        if 'conference' in content.lower() or 'speaker' in content.lower():
            verifiable_elements += 10

        return min(100, verifiable_elements)

    def _score_humility(self, content):
        """Score appropriate humility in self-presentation"""
        # Check for overuse of "I"
        i_count = len(re.findall(r'\bI\b', content))
        total_words = len(content.split())

        if total_words > 0:
            i_ratio = i_count / total_words
            # Optimal "I" usage is around 2-5%
            if 0.02 <= i_ratio <= 0.05:
                humility_score = 100
            else:
                humility_score = max(0, 100 - abs(i_ratio - 0.035) * 2000)
        else:
            humility_score = 50

        # Check for team language
        we_count = len(re.findall(r'\bwe\b', content.lower()))
        if we_count > 0:
            humility_score = min(100, humility_score + we_count * 2)

        return humility_score

    def _score_professionalism(self, content):
        """Score professionalism of language"""
        professionalism_score = 100

        # Check for unprofessional language
        unprofessional_words = ['awesome', 'cool', 'killer', 'rockstar', 'ninja', 'guru', 'god', 'legend']
        for word in unprofessional_words:
            if word in content.lower():
                professionalism_score -= 10

        # Check for proper capitalization
        sentences = re.findall(r'[.!?]\s+([a-z])', content)
        if sentences:
            lowercase_start = sum(1 for s in sentences if s.islower())
            if lowercase_start / len(sentences) > 0.3:
                professionalism_score -= 15

        # Check for complete sentences
        periods = len(re.findall(r'[.!?]', content))
        if periods < 10 and len(content.split()) > 100:
            professionalism_score -= 10

        return max(0, professionalism_score)

    def _score_references(self, content):
        """Score presence of references"""
        if 'reference' in content.lower() or 'available upon request' in content.lower():
            return 100
        elif 'referee' in content.lower():
            return 70
        else:
            return 30

    def _score_portfolio(self, content):
        """Score portfolio presence"""
        portfolio_score = 0

        if 'portfolio' in content.lower():
            portfolio_score += 40
        if 'github' in content.lower() or 'gitlab' in content.lower():
            portfolio_score += 30
        if 'website' in content.lower() or 'blog' in content.lower():
            portfolio_score += 30

        return min(100, portfolio_score)

    def _score_publications(self, content):
        """Score publication presence"""
        publication_score = 0

        if 'published' in content.lower():
            publication_score += 30
        if 'publication' in content.lower():
            publication_score += 20
        if 'paper' in content.lower():
            publication_score += 20
        if 'research' in content.lower():
            publication_score += 30

        return min(100, publication_score)

    def _calculate_red_flag_penalty(self, content):
        """Calculate penalty for red flags"""
        penalty = 0
        content_lower = content.lower()

        for flag in self.red_flags:
            if flag in content_lower:
                penalty += 5

        # Check for unrealistic claims
        if 'guarantee' in content_lower and '100%' in content_lower:
            penalty += 10

        # Check for too many superlatives
        superlatives = ['best', 'perfect', 'excellent', 'outstanding', 'exceptional', 'unmatched']
        superlative_count = sum(1 for s in superlatives if s in content_lower)
        if superlative_count > 3:
            penalty += (superlative_count - 3) * 5

        return min(50, penalty)  # Max 50% penalty