"""
COGNIS - Future Success Simulator
Predicts future performance and success indicators

This module simulates a candidate's future success potential based on:
- Learning velocity and adaptability
- Growth mindset indicators
- Network effects and collaboration
- Risk tolerance and innovation
- Resilience and recovery patterns
- Career stage adjustments
"""

import re
import math
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict


class FutureSimulator:
    """
    Simulate future success potential based on current metrics and patterns.

    The simulator evaluates 6 key future success factors:
    1. Learning Velocity - How fast candidates acquire new skills
    2. Adaptability - Ability to handle change and new situations
    3. Growth Mindset - Belief in ability to develop and improve
    4. Network Effect - Collaboration and influence potential
    5. Risk Tolerance - Willingness to take calculated risks
    6. Resilience - Ability to recover from setbacks
    """

    def __init__(self):
        """Initialize the future simulator with weighting and configuration."""
        # Weight factors for future success components
        self.future_weights = {
            'learning_velocity': 0.25,
            'adaptability': 0.20,
            'growth_mindset': 0.20,
            'network_effect': 0.10,
            'risk_tolerance': 0.15,
            'resilience': 0.10
        }

        # Career stage definitions with multipliers
        self.career_stages = {
            'early': (0, 3, 1.3),  # (min_years, max_years, multiplier)
            'mid': (3, 8, 1.1),
            'senior': (8, 15, 1.0),
            'expert': (15, 30, 0.9)
        }

        # Role progression predictions
        self.role_predictions = {
            'early': {
                'technical': 'Senior Developer / Technical Lead',
                'management': 'Team Lead / Project Manager',
                'mixed': 'Technical Project Manager'
            },
            'mid': {
                'technical': 'Principal Engineer / Architect',
                'management': 'Engineering Manager / Director',
                'mixed': 'Technical Director'
            },
            'senior': {
                'technical': 'Distinguished Engineer / CTO',
                'management': 'VP of Engineering / CPO',
                'mixed': 'VP of Product & Engineering'
            },
            'expert': {
                'technical': 'Chief Scientist / Technology Fellow',
                'management': 'Chief Product Officer / CEO',
                'mixed': 'Chief Innovation Officer'
            }
        }

        # Keywords for identifying growth indicators
        self.growth_keywords = [
            'learned', 'trained', 'certified', 'studied', 'mastered',
            'grew', 'developed', 'expanded', 'improved', 'advanced',
            'evolved', 'transformed', 'innovated', 'pioneered', 'revolutionized'
        ]

        self.challenge_keywords = [
            'challenge', 'difficult', 'complex', 'hard', 'tough',
            'obstacle', 'hurdle', 'barrier', 'adversity', 'setback',
            'crisis', 'emergency', 'urgent', 'critical', 'pressure'
        ]

        self.collaboration_keywords = [
            'collaborated', 'team', 'together', 'cooperated', 'partnered',
            'cross-functional', 'multi-team', 'stakeholder', 'client', 'customer',
            'presented', 'communicated', 'facilitated', 'workshop', 'meeting'
        ]

        self.risk_keywords = [
            'startup', 'new', 'novel', 'innovated', 'pioneered',
            'ventured', 'challenged', 'disrupted', 'transformed',
            'entrepreneur', 'venture', 'launch', 'initiative', 'pilot'
        ]

        self.recovery_keywords = [
            'recovered', 'rebounded', 'overcame', 'persisted', 'persevered',
            'adapted', 'adjusted', 'pivoted', 'solution', 'resolved'
        ]

    def simulate_future(self, resume_data: Dict[str, Any], match_score: float) -> float:
        """
        Simulate future success potential.

        Args:
            resume_data: Parsed resume data dictionary
            match_score: Current match score with job description

        Returns:
            Future success score (0-100)
        """
        # Extract data
        skills = resume_data.get('skills', [])
        achievements = resume_data.get('achievements', [])
        experience_years = resume_data.get('experience_years', 0)
        content = resume_data.get('raw_content', '')
        education = resume_data.get('education', [])
        certifications = resume_data.get('certifications', [])
        projects = resume_data.get('projects', [])

        # Calculate individual future factors
        learning_velocity = self._calculate_learning_velocity(
            skills, achievements, certifications, education
        )
        adaptability = self._calculate_adaptability_score(
            content, projects, experience_years
        )
        growth_mindset = self._calculate_growth_mindset(
            content, achievements, education
        )
        network_effect = self._calculate_network_effect(
            content, achievements
        )
        risk_tolerance = self._calculate_risk_tolerance(
            content, projects, experience_years
        )
        resilience = self._calculate_resilience(
            content, achievements, experience_years
        )

        # Calculate weighted score
        weighted_score = 0
        total_weight = 0

        factor_scores = {
            'learning_velocity': learning_velocity,
            'adaptability': adaptability,
            'growth_mindset': growth_mindset,
            'network_effect': network_effect,
            'risk_tolerance': risk_tolerance,
            'resilience': resilience
        }

        for factor, score in factor_scores.items():
            weight = self.future_weights.get(factor, 1.0)
            weighted_score += score * weight
            total_weight += weight

        base_future_score = (weighted_score / total_weight) * 100 if total_weight > 0 else 0

        # Apply career stage multiplier
        stage_multiplier = self._get_stage_multiplier(experience_years)
        base_future_score *= stage_multiplier

        # Incorporate match score (if highly matched, future success more likely)
        if match_score > 70:
            base_future_score *= 1.1
        elif match_score > 50:
            base_future_score *= 1.0
        else:
            base_future_score *= 0.9

        # Add bonus for continuous learning indicators
        learning_bonus = self._calculate_learning_bonus(resume_data)
        base_future_score += learning_bonus

        # Ensure score is within bounds
        final_score = max(0, min(100, base_future_score))

        return round(final_score, 2)

    def _calculate_learning_velocity(
            self,
            skills: List[str],
            achievements: List[str],
            certifications: List[str],
            education: List[str]
    ) -> float:
        """
        Calculate learning velocity from skills and achievements.

        Args:
            skills: List of skills
            achievements: List of achievements
            certifications: List of certifications
            education: List of education entries

        Returns:
            Learning velocity score (0-100)
        """
        score = 30  # Base score

        # Skill diversity indicates learning across domains
        skill_diversity = len(set(skills))
        if skill_diversity >= 15:
            score += 30
        elif skill_diversity >= 10:
            score += 25
        elif skill_diversity >= 5:
            score += 15
        else:
            score += 5

        # Achievement quantity and quality indicate active learning
        if achievements:
            achievement_count = len(achievements)
            if achievement_count >= 10:
                score += 25
            elif achievement_count >= 5:
                score += 15
            else:
                score += 5

            # Bonus for varied achievements
            achievement_types = set()
            for achievement in achievements:
                if any(word in achievement.lower() for word in ['led', 'managed']):
                    achievement_types.add('leadership')
                if any(word in achievement.lower() for word in ['created', 'designed']):
                    achievement_types.add('creation')
                if any(word in achievement.lower() for word in ['improved', 'optimized']):
                    achievement_types.add('improvement')
                if re.search(r'\d+%|\$\d+', achievement):
                    achievement_types.add('quantified')

            if len(achievement_types) >= 3:
                score += 10
            elif len(achievement_types) >= 2:
                score += 5

        # Certifications indicate formal learning
        if certifications:
            cert_count = len(certifications)
            if cert_count >= 5:
                score += 15
            elif cert_count >= 3:
                score += 10
            else:
                score += 5

        # Education level indicates learning foundation
        if education:
            highest_degree = 0
            degree_levels = {
                'phd': 4,
                'doctorate': 4,
                'master': 3,
                'm.s': 3,
                'm.sc': 3,
                'mba': 3,
                'bachelor': 2,
                'b.s': 2,
                'b.sc': 2,
                'associate': 1
            }

            for edu in education:
                degree = edu.get('degree', '').lower()
                for level_name, level_value in degree_levels.items():
                    if level_name in degree:
                        highest_degree = max(highest_degree, level_value)

            score += highest_degree * 5

        return max(0, min(100, score))

    def _calculate_adaptability_score(
            self,
            content: str,
            projects: List[str],
            experience_years: float
    ) -> float:
        """
        Calculate adaptability based on experience variety.

        Args:
            content: Resume text
            projects: List of projects
            experience_years: Total years of experience

        Returns:
            Adaptability score (0-100)
        """
        score = 30  # Base score

        # Check for multiple industries
        industries = ['tech', 'finance', 'health', 'education', 'retail',
                      'manufacturing', 'consulting', 'media', 'energy', 'transportation']
        industry_count = sum(1 for industry in industries if industry in content.lower())
        score += min(25, industry_count * 5)

        # Check for multiple roles
        roles = ['developer', 'manager', 'analyst', 'architect', 'designer',
                 'consultant', 'lead', 'director', 'scientist', 'researcher']
        role_count = sum(1 for role in roles if role in content.lower())
        score += min(20, role_count * 4)

        # Cross-functional experience indicates adaptability
        cross_keywords = ['cross-functional', 'cross functional', 'multiple teams',
                          'stakeholder', 'client-facing', 'product']
        cross_count = sum(1 for keyword in cross_keywords if keyword in content.lower())
        score += min(20, cross_count * 4)

        # Projects indicate practical adaptability
        if projects:
            project_count = len(projects)
            if project_count >= 5:
                score += 15
            elif project_count >= 3:
                score += 10
            else:
                score += 5

            # Check for diverse projects
            project_keywords = ['web', 'mobile', 'data', 'ai', 'cloud', 'desktop']
            project_types = sum(1 for keyword in project_keywords if keyword in ' '.join(projects).lower())
            if project_types >= 3:
                score += 5

        # Adjust for experience (mid-career often more adaptable)
        if 3 <= experience_years <= 10:
            score += 10
        elif experience_years > 10:
            score += 5  # More experience, but potentially less adaptable

        return max(0, min(100, score))

    def _calculate_growth_mindset(
            self,
            content: str,
            achievements: List[str],
            education: List[str]
    ) -> float:
        """
        Calculate growth mindset indicators.

        Args:
            content: Resume text
            achievements: List of achievements
            education: List of education entries

        Returns:
            Growth mindset score (0-100)
        """
        score = 40  # Base score

        # Check for growth-related language
        growth_count = 0
        for keyword in self.growth_keywords:
            if keyword in content.lower():
                growth_count += 1
        score += min(30, growth_count * 4)

        # Check for continuous learning indicators
        learning_indicators = ['course', 'training', 'workshop', 'seminar', 'bootcamp']
        learning_count = sum(1 for indicator in learning_indicators if indicator in content.lower())
        score += min(15, learning_count * 3)

        # Achievement quality indicates growth
        if achievements:
            challenge_count = 0
            for achievement in achievements:
                if any(keyword in achievement.lower() for keyword in self.challenge_keywords):
                    challenge_count += 1
            if challenge_count / len(achievements) >= 0.3:
                score += 10

        # Education shows investment in growth
        if education:
            # Check for continuing education
            recent_edu = False
            current_year = datetime.now().year
            for edu in education:
                year = edu.get('year', '')
                if year:
                    try:
                        grad_year = int(year)
                        if current_year - grad_year <= 5:
                            recent_edu = True
                            break
                    except:
                        pass

            if recent_edu:
                score += 10

        # Look for self-improvement language
        improvement_patterns = ['improved', 'enhanced', 'optimized', 'upgraded']
        improvement_count = sum(1 for pattern in improvement_patterns if pattern in content.lower())
        score += min(10, improvement_count * 2)

        return max(0, min(100, score))

    def _calculate_network_effect(
            self,
            content: str,
            achievements: List[str]
    ) -> float:
        """
        Calculate network effect and collaboration potential.

        Args:
            content: Resume text
            achievements: List of achievements

        Returns:
            Network effect score (0-100)
        """
        score = 30  # Base score

        # Check for collaboration indicators
        collaboration_count = 0
        for keyword in self.collaboration_keywords:
            if keyword in content.lower():
                collaboration_count += 1
        score += min(30, collaboration_count * 4)

        # Check for leadership in network
        leadership_count = 0
        leadership_keywords = ['led', 'mentored', 'guided', 'directed', 'supervised', 'managed']
        for keyword in leadership_keywords:
            if keyword in content.lower():
                leadership_count += 1
        score += min(25, leadership_count * 5)

        # Check for communication skills
        communication_keywords = ['presented', 'communicated', 'presentation', 'speaker',
                                  'conference', 'workshop', 'facilitated', 'coordinated']
        comm_count = sum(1 for keyword in communication_keywords if keyword in content.lower())
        score += min(20, comm_count * 4)

        # Check achievements for collaboration indicators
        if achievements:
            collab_achievements = 0
            for achievement in achievements:
                if any(keyword in achievement.lower() for keyword in ['team', 'cross', 'stakeholder']):
                    collab_achievements += 1

            if collab_achievements / len(achievements) >= 0.5:
                score += 10

        return max(0, min(100, score))

    def _calculate_risk_tolerance(
            self,
            content: str,
            projects: List[str],
            experience_years: float
    ) -> float:
        """
        Calculate risk tolerance from resume.

        Args:
            content: Resume text
            projects: List of projects
            experience_years: Total years of experience

        Returns:
            Risk tolerance score (0-100)
        """
        score = 50  # Base score

        # Check for risk-taking indicators
        risk_count = 0
        for keyword in self.risk_keywords:
            if keyword in content.lower():
                risk_count += 1
        score += min(25, risk_count * 5)

        # Check for entrepreneurial signs
        if 'startup' in content.lower():
            score += 15
        if 'entrepreneur' in content.lower() or 'founder' in content.lower():
            score += 15

        # Check for innovation
        innovation_keywords = ['innovated', 'patent', 'pioneered', 'novel', 'disrupt']
        innovation_count = sum(1 for keyword in innovation_keywords if keyword in content.lower())
        score += min(20, innovation_count * 5)

        # Check for new initiatives
        initiative_keywords = ['launched', 'initiated', 'introduced', 'established']
        initiative_count = sum(1 for keyword in initiative_keywords if keyword in content.lower())
        score += min(15, initiative_count * 3)

        # Project diversity indicates risk tolerance
        if projects:
            # Check if projects are varied
            project_contexts = ['web', 'mobile', 'data', 'ai', 'cloud']
            project_types = sum(1 for context in project_contexts if any(context in p.lower() for p in projects))
            if project_types >= 3:
                score += 10

        # Adjust for experience (mid-career more willing to take risks)
        if 3 <= experience_years <= 10:
            score += 5

        return max(0, min(100, score))

    def _calculate_resilience(
            self,
            content: str,
            achievements: List[str],
            experience_years: float
    ) -> float:
        """
        Calculate resilience from career patterns.

        Args:
            content: Resume text
            achievements: List of achievements
            experience_years: Total years of experience

        Returns:
            Resilience score (0-100)
        """
        score = 40  # Base score

        # Check for overcoming challenges
        challenge_count = 0
        for keyword in self.challenge_keywords:
            if keyword in content.lower():
                challenge_count += 1
        score += min(25, challenge_count * 5)

        # Check for recovery language
        recovery_count = 0
        for keyword in self.recovery_keywords:
            if keyword in content.lower():
                recovery_count += 1
        score += min(20, recovery_count * 4)

        # Check achievements for challenge indicators
        if achievements:
            challenging_achievements = 0
            for achievement in achievements:
                if any(keyword in achievement.lower() for keyword in self.challenge_keywords):
                    challenging_achievements += 1

            if challenging_achievements / len(achievements) >= 0.4:
                score += 10

        # Check for persistence indicators
        persistence_keywords = ['consistently', 'continuously', 'persisted', 'ongoing']
        persistence_count = sum(1 for keyword in persistence_keywords if keyword in content.lower())
        score += min(15, persistence_count * 3)

        # Check career gaps and recovery
        years = self._extract_years(content)
        if years:
            sorted_years = sorted(years)
            gaps = []
            for i in range(1, len(sorted_years)):
                gap = sorted_years[i] - sorted_years[i - 1]
                if gap > 2:  # Gap larger than 2 years
                    gaps.append(gap)

            if gaps:
                # Having gaps but coming back shows resilience
                if len(gaps) <= 2 and max(gaps) <= 3:
                    score += 10
                elif len(gaps) <= 1:
                    score += 5

        return max(0, min(100, score))

    def _get_stage_multiplier(self, experience_years: float) -> float:
        """
        Get multiplier based on career stage.

        Args:
            experience_years: Total years of experience

        Returns:
            Stage multiplier
        """
        for stage, (min_years, max_years, multiplier) in self.career_stages.items():
            if min_years <= experience_years < max_years:
                return multiplier

        # Default multiplier for very experienced (>30 years)
        return 0.85

    def _calculate_learning_bonus(self, resume_data: Dict[str, Any]) -> float:
        """
        Calculate bonus for continuous learning indicators.

        Args:
            resume_data: Parsed resume data

        Returns:
            Learning bonus (0-10)
        """
        bonus = 0
        content = resume_data.get('raw_content', '')
        certifications = resume_data.get('certifications', [])

        # Recent certifications
        current_year = datetime.now().year
        for cert in certifications:
            # Check for year in certification
            years = re.findall(r'\b(19|20)\d{2}\b', cert)
            if years:
                try:
                    cert_year = int(years[0])
                    if current_year - cert_year <= 2:
                        bonus += 3
                    elif current_year - cert_year <= 5:
                        bonus += 1
                except:
                    pass

        # Online learning platforms
        learning_platforms = ['coursera', 'edx', 'udacity', 'pluralsight', 'linkedin learning']
        for platform in learning_platforms:
            if platform in content.lower():
                bonus += 2

        # Technical blog or writing
        if 'blog' in content.lower() or 'medium' in content.lower():
            bonus += 3

        # Open source contributions
        if 'open source' in content.lower() or 'github' in content.lower():
            bonus += 3

        return min(10, bonus)

    def _extract_years(self, content: str) -> List[int]:
        """
        Extract years from content.

        Args:
            content: Resume text

        Returns:
            List of years
        """
        year_pattern = r'\b(19|20)\d{2}\b'
        years = re.findall(year_pattern, content)
        years = [int(year) for year in years if 1980 <= int(year) <= datetime.now().year + 1]
        return sorted(list(set(years)))

    def predict_future_trajectory(
            self,
            resume_data: Dict[str, Any],
            years_ahead: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Predict career trajectory over the next N years.

        Args:
            resume_data: Parsed resume data
            years_ahead: Number of years to predict

        Returns:
            List of predicted career steps
        """
        experience_years = resume_data.get('experience_years', 0)
        skills = resume_data.get('skills', [])
        achievements = resume_data.get('achievements', [])

        # Determine current career stage
        current_stage = 'early'
        for stage, (min_years, max_years, _) in self.career_stages.items():
            if min_years <= experience_years < max_years:
                current_stage = stage
                break

        # Determine career path (technical, management, mixed)
        career_path = self._determine_career_path(resume_data)

        # Generate predictions
        predictions = []
        current_year = datetime.now().year

        for year in range(1, years_ahead + 1):
            projected_years = experience_years + year
            predicted_stage = self._determine_stage(projected_years)

            # Get predicted role
            predicted_role = self._predict_role(predicted_stage, career_path)

            # Calculate confidence (decreases over time)
            confidence = max(50, 100 - (year * 8))

            predictions.append({
                'year': year,
                'target_year': current_year + year,
                'experience_years': round(projected_years, 1),
                'career_stage': predicted_stage,
                'predicted_role': predicted_role,
                'confidence': confidence
            })

        return predictions

    def _determine_career_path(self, resume_data: Dict[str, Any]) -> str:
        """
        Determine career path based on resume data.

        Args:
            resume_data: Parsed resume data

        Returns:
            Career path ('technical', 'management', 'mixed')
        """
        content = resume_data.get('raw_content', '')
        achievements = resume_data.get('achievements', [])

        # Count technical indicators
        technical_keywords = ['python', 'java', 'javascript', 'sql', 'aws', 'docker',
                              'kubernetes', 'machine learning', 'data science']
        tech_count = sum(1 for keyword in technical_keywords if keyword in content.lower())

        # Count management indicators
        management_keywords = ['led', 'managed', 'directed', 'supervised', 'mentored',
                               'budget', 'strategy', 'planning', 'stakeholder']
        mgmt_count = sum(1 for keyword in management_keywords if keyword in content.lower())

        # Count achievements
        leadership_achievements = sum(1 for a in achievements if 'led' in a.lower() or 'managed' in a.lower())

        # Determine path
        if mgmt_count > tech_count * 0.5 or leadership_achievements >= 2:
            if tech_count > mgmt_count * 0.5:
                return 'mixed'
            else:
                return 'management'
        else:
            return 'technical'

    def _determine_stage(self, experience_years: float) -> str:
        """
        Determine career stage based on experience years.

        Args:
            experience_years: Total years of experience

        Returns:
            Career stage name
        """
        for stage, (min_years, max_years, _) in self.career_stages.items():
            if min_years <= experience_years < max_years:
                return stage
        return 'expert'

    def _predict_role(self, stage: str, career_path: str) -> str:
        """
        Predict role based on stage and career path.

        Args:
            stage: Career stage
            career_path: Career path

        Returns:
            Predicted role title
        """
        if stage in self.role_predictions:
            if career_path in self.role_predictions[stage]:
                return self.role_predictions[stage][career_path]
            else:
                # Default to mixed if path not found
                return self.role_predictions[stage]['mixed']
        else:
            # Default for unknown stages
            return 'Senior Professional'

    def generate_future_report(
            self,
            resume_data: Dict[str, Any],
            match_score: float
    ) -> str:
        """
        Generate comprehensive future success report.

        Args:
            resume_data: Parsed resume data
            match_score: Current match score

        Returns:
            Formatted report string
        """
        future_score = self.simulate_future(resume_data, match_score)
        trajectory = self.predict_future_trajectory(resume_data)

        report = []
        report.append("=" * 70)
        report.append("FUTURE SUCCESS SIMULATION REPORT")
        report.append("=" * 70)
        report.append(f"\nFuture Success Score: {future_score:.1f}%")

        # Confidence level
        if future_score >= 80:
            confidence = "Very High"
        elif future_score >= 65:
            confidence = "High"
        elif future_score >= 50:
            confidence = "Moderate"
        else:
            confidence = "Low"

        report.append(f"Confidence Level: {confidence}")

        # Growth indicators
        report.append("\nKEY GROWTH INDICATORS:")
        report.append("-" * 40)
        indicators = self._identify_growth_indicators(resume_data)
        for indicator in indicators:
            report.append(f"• {indicator}")

        # Career trajectory
        report.append("\nPREDICTED CAREER TRAJECTORY (Next 5 Years):")
        report.append("-" * 40)

        for step in trajectory:
            report.append(f"Year {step['year']} ({step['target_year']}):")
            report.append(f"  Role: {step['predicted_role']}")
            report.append(f"  Experience: {step['experience_years']:.0f} years")
            report.append(f"  Confidence: {step['confidence']}%")
            report.append("")

        # Recommendations
        report.append("\nRECOMMENDATIONS FOR FUTURE SUCCESS:")
        report.append("-" * 40)
        recommendations = self._generate_recommendations(
            resume_data, future_score, trajectory
        )
        for rec in recommendations:
            report.append(f"• {rec}")

        # Risk factors
        report.append("\nPOTENTIAL RISK FACTORS:")
        report.append("-" * 40)
        risks = self._identify_risks(resume_data)
        for risk in risks:
            report.append(f"• {risk}")

        report.append("\n" + "=" * 70)

        return "\n".join(report)

    def _identify_growth_indicators(self, resume_data: Dict[str, Any]) -> List[str]:
        """
        Identify key growth indicators from resume.

        Args:
            resume_data: Parsed resume data

        Returns:
            List of growth indicators
        """
        indicators = []
        skills = resume_data.get('skills', [])
        achievements = resume_data.get('achievements', [])
        certifications = resume_data.get('certifications', [])
        experience_years = resume_data.get('experience_years', 0)

        # Technical growth indicators
        if len(skills) >= 10:
            indicators.append("Wide technical skill set indicates continuous learning")

        if len(skills) >= 15:
            indicators.append("Exceptional technical breadth and depth")

        # Career growth indicators
        if experience_years >= 3 and len(achievements) >= 5:
            indicators.append("Consistent achievement pattern suggests steady growth")

        if len(achievements) >= 10:
            indicators.append("High achievement frequency indicates strong performance")

        # Leadership indicators
        if any('led' in str(achievement).lower() for achievement in achievements):
            indicators.append("Leadership experience indicates management potential")

        # Innovation indicators
        if any(any(kw in str(achievement).lower() for kw in ['created', 'designed', 'developed'])
               for achievement in achievements):
            indicators.append("Innovation and creation skills demonstrated")

        # Learning indicators
        if certifications:
            if len(certifications) >= 3:
                indicators.append("Strong commitment to continuous learning through certifications")
            else:
                indicators.append("Invests in professional certification")

        # Growth mindset language
        content = resume_data.get('raw_content', '')
        if any(kw in content.lower() for kw in self.growth_keywords):
            indicators.append("Demonstrates growth mindset in career language")

        return indicators[:5]  # Return top 5 indicators

    def _generate_recommendations(
            self,
            resume_data: Dict[str, Any],
            future_score: float,
            trajectory: List[Dict[str, Any]]
    ) -> List[str]:
        """
        Generate actionable recommendations for future success.

        Args:
            resume_data: Parsed resume data
            future_score: Future success score
            trajectory: Predicted career trajectory

        Returns:
            List of recommendations
        """
        recommendations = []
        skills = resume_data.get('skills', [])
        achievements = resume_data.get('achievements', [])
        content = resume_data.get('raw_content', '')

        # Based on skill gaps
        if len(skills) < 8:
            recommendations.append("Expand technical skill set with emerging technologies")

        # Based on achievement pattern
        if achievements and len(achievements) < 5:
            recommendations.append("Focus on documenting and quantifying achievements")

        # Based on future score
        if future_score < 60:
            recommendations.append("Seek challenging projects to accelerate growth")
            recommendations.append("Invest in continuous learning and certification")
        elif future_score < 80:
            recommendations.append("Maintain growth trajectory with strategic skill development")
            recommendations.append("Consider mentorship or leadership opportunities")
        else:
            recommendations.append("Continue high-growth trajectory")
            recommendations.append("Seek leadership and strategic roles")

        # Specific recommendations
        if 'python' in str(skills).lower():
            recommendations.append("Deepen expertise in Python ecosystem and frameworks")

        if any(skill in str(skills).lower() for skill in ['cloud', 'aws', 'azure']):
            recommendations.append("Advance cloud expertise with specialized certifications")

        if 'leadership' not in content.lower():
            recommendations.append("Develop leadership and team management skills")

        # Based on career trajectory
        if trajectory and len(trajectory) >= 3:
            next_role = trajectory[2].get('predicted_role', '')
            if 'lead' in next_role.lower() or 'manager' in next_role.lower():
                recommendations.append("Prepare for management transition with relevant courses")

        return recommendations[:5]  # Return top 5 recommendations

    def _identify_risks(self, resume_data: Dict[str, Any]) -> List[str]:
        """
        Identify potential risks for future success.

        Args:
            resume_data: Parsed resume data

        Returns:
            List of risk factors
        """
        risks = []
        content = resume_data.get('raw_content', '')
        experience_years = resume_data.get('experience_years', 0)

        # Check for outdated skills
        if 'legacy' in content.lower() or 'maintenance' in content.lower():
            risks.append("Potential skill obsolescence risk")

        # Check for lack of innovation
        if not any(kw in content.lower() for kw in ['created', 'designed', 'developed']):
            risks.append("Limited demonstration of innovation or creation skills")

        # Check for limited leadership experience
        if not any(kw in content.lower() for kw in ['led', 'managed', 'directed']):
            risks.append("Limited leadership and management exposure")

        # Check for industry narrowness
        industries = ['tech', 'finance', 'healthcare', 'education', 'retail']
        industry_count = sum(1 for industry in industries if industry in content.lower())
        if industry_count <= 2:
            risks.append("Limited industry diversity may reduce adaptability")

        # Check for career stagnation
        if experience_years > 8 and not any('senior' in role.lower() or 'lead' in role.lower()
                                            for role in resume_data.get('experience', [])):
            risks.append("Potential career stagnation without clear progression")

        return risks[:3]  # Return top 3 risks

    def generate_trajectory_visualization_data(
            self,
            resume_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate data for trajectory visualization.

        Args:
            resume_data: Parsed resume data

        Returns:
            Dictionary with visualization data
        """
        trajectory = self.predict_future_trajectory(resume_data)

        # Prepare data for plotting
        years = [step['year'] for step in trajectory]
        experience = [step['experience_years'] for step in trajectory]
        confidence = [step['confidence'] for step in trajectory]
        roles = [step['predicted_role'] for step in trajectory]

        return {
            'years': years,
            'experience': experience,
            'confidence': confidence,
            'roles': roles,
            'current_experience': resume_data.get('experience_years', 0),
            'current_role': resume_data.get('experience', [{}])[0].get('title', 'Unknown') if resume_data.get(
                'experience') else 'Unknown'
        }