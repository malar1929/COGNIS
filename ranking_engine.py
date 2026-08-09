"""
COGNIS - Candidate Ranking Engine
Ranks candidates based on multi-dimensional scoring
"""

import math
from collections import OrderedDict


class RankingEngine:
    """Rank candidates based on various metrics"""

    def __init__(self):
        """Initialize ranking engine"""
        self.ranking_weights = {
            'match_score': 0.25,
            'trust_score': 0.20,
            'potential_score': 0.25,
            'consistency_score': 0.15,
            'future_score': 0.15
        }

        self.ranking_boosts = {
            'innovation': 1.05,
            'leadership': 1.03,
            'growth': 1.08,
            'stability': 1.02
        }

    def rank_candidates(self, candidates):
        """
        Rank candidates based on all metrics
        Returns sorted list of candidates with rankings
        """
        if not candidates:
            return []

        # Normalize all scores
        normalized_candidates = self._normalize_scores(candidates)

        # Calculate weighted scores
        for candidate in normalized_candidates:
            candidate['weighted_score'] = self._calculate_weighted_score(candidate)
            candidate['final_score'] = self._apply_boosts(candidate)

        # Sort by final score
        sorted_candidates = sorted(normalized_candidates,
                                   key=lambda x: x['final_score'],
                                   reverse=True)

        # Add rank
        for rank, candidate in enumerate(sorted_candidates, 1):
            candidate['rank'] = rank

        return sorted_candidates

    def _normalize_scores(self, candidates):
        """Normalize scores to 0-100 range"""
        normalized = []

        for candidate in candidates:
            normalized_candidate = candidate.copy()

            # Ensure all scores exist and are in range
            for score_name in ['match_score', 'trust_score', 'potential_score',
                               'consistency_score', 'future_score']:
                if score_name not in normalized_candidate:
                    normalized_candidate[score_name] = 0
                else:
                    # Clamp to 0-100
                    normalized_candidate[score_name] = max(0, min(100,
                                                                  normalized_candidate[score_name]))

            normalized.append(normalized_candidate)

        return normalized

    def _calculate_weighted_score(self, candidate):
        """Calculate weighted overall score"""
        total = 0

        for weight_name, weight in self.ranking_weights.items():
            if weight_name in candidate:
                score = candidate[weight_name]
                total += score * weight

        return total

    def _apply_boosts(self, candidate):
        """Apply performance boosts based on special factors"""
        base_score = candidate['weighted_score']

        # Check for innovation boost
        if candidate.get('innovation_score', 0) > 70:
            base_score *= self.ranking_boosts['innovation']

        # Check for leadership boost
        if candidate.get('leadership_score', 0) > 70:
            base_score *= self.ranking_boosts['leadership']

        # Check for growth potential boost
        if candidate.get('potential_score', 0) > 80:
            base_score *= self.ranking_boosts['growth']

        # Check for consistency boost
        if candidate.get('consistency_score', 0) > 80:
            base_score *= self.ranking_boosts['stability']

        return min(100, base_score)  # Cap at 100

    def generate_ranking_report(self, ranked_candidates):
        """Generate detailed ranking report"""
        report = []
        report.append("=" * 60)
        report.append("COGNIS - CANDIDATE RANKING REPORT")
        report.append("=" * 60)
        report.append("")

        if not ranked_candidates:
            report.append("No candidates to rank.")
            return "\n".join(report)

        report.append(f"Total Candidates: {len(ranked_candidates)}")
        report.append("")
        report.append("RANK | NAME | OVERALL | MATCH | TRUST | POTENTIAL")
        report.append("-" * 60)

        for candidate in ranked_candidates:
            report.append(f"#{candidate['rank']:2d}  | {candidate['name'][:20]:20s} | "
                          f"{candidate['final_score']:5.1f}  | "
                          f"{candidate['match_score']:5.1f}  | "
                          f"{candidate['trust_score']:5.1f}  | "
                          f"{candidate['potential_score']:5.1f}")

        report.append("")
        report.append("=" * 60)
        report.append("TOP 3 CANDIDATES DETAILS")
        report.append("=" * 60)

        for i, candidate in enumerate(ranked_candidates[:3], 1):
            report.append("")
            report.append(f"#{i} - {candidate['name']}")
            report.append("-" * 40)
            report.append(f"Overall Score:     {candidate['final_score']:.1f}%")
            report.append(f"Match Score:       {candidate['match_score']:.1f}%")
            report.append(f"Trust Score:       {candidate['trust_score']:.1f}%")
            report.append(f"Potential Score:   {candidate['potential_score']:.1f}%")
            report.append(f"Consistency Score: {candidate.get('consistency_score', 0):.1f}%")
            report.append(f"Future Score:      {candidate.get('future_score', 0):.1f}%")

            # Add strengths and weaknesses
            strengths = self._identify_strengths(candidate)
            weaknesses = self._identify_weaknesses(candidate)

            if strengths:
                report.append("")
                report.append("Strengths:")
                for strength in strengths[:3]:
                    report.append(f"  • {strength}")

            if weaknesses:
                report.append("")
                report.append("Areas for Development:")
                for weakness in weaknesses[:2]:
                    report.append(f"  • {weakness}")

        report.append("")
        report.append("=" * 60)
        report.append("End of Report")
        report.append("=" * 60)

        return "\n".join(report)

    def _identify_strengths(self, candidate):
        """Identify candidate's key strengths"""
        strengths = []

        if candidate.get('match_score', 0) >= 80:
            strengths.append("Excellent skill match with job requirements")

        if candidate.get('trust_score', 0) >= 80:
            strengths.append("High credibility and verifiable achievements")

        if candidate.get('potential_score', 0) >= 80:
            strengths.append("Exceptional growth potential and learning agility")

        if candidate.get('consistency_score', 0) >= 80:
            strengths.append("Consistent career progression and skill development")

        if candidate.get('future_score', 0) >= 80:
            strengths.append("Strong future success indicators")

        if not strengths:
            strengths.append("Balanced performance across all metrics")

        return strengths

    def _identify_weaknesses(self, candidate):
        """Identify areas for improvement"""
        weaknesses = []

        if candidate.get('match_score', 0) < 60:
            weaknesses.append("Gap in required skills for this role")

        if candidate.get('trust_score', 0) < 60:
            weaknesses.append("Limited verifiable achievements or references")

        if candidate.get('potential_score', 0) < 60:
            weaknesses.append("Limited indicators of growth potential")

        if candidate.get('consistency_score', 0) < 60:
            weaknesses.append("Inconsistent career progression pattern")

        return weaknesses

    def get_top_candidates(self, ranked_candidates, n=3):
        """Get top N candidates"""
        return ranked_candidates[:n]

    def calculate_percentile(self, candidates, candidate_name):
        """Calculate candidate's percentile rank"""
        if not candidates:
            return 0

        # Find the candidate
        target_candidate = None
        for c in candidates:
            if c.get('name') == candidate_name:
                target_candidate = c
                break

        if not target_candidate:
            return 0

        # Calculate percentile
        target_score = target_candidate.get('final_score', 0)
        below_count = sum(1 for c in candidates if c.get('final_score', 0) < target_score)

        percentile = (below_count / len(candidates)) * 100
        return round(percentile, 1)

    def generate_comparison_matrix(self, ranked_candidates):
        """Generate comparison matrix for top candidates"""
        if not ranked_candidates:
            return ""

        top_n = min(5, len(ranked_candidates))

        matrix = []
        matrix.append("=" * 80)
        matrix.append("CANDIDATE COMPARISON MATRIX")
        matrix.append("=" * 80)
        matrix.append("")

        # Header
        header = "| Name".ljust(20) + "| Match".ljust(10) + "| Trust".ljust(10) + "| Potential".ljust(
            12) + "| Consistency".ljust(14) + "| Future".ljust(10) + "| Overall".ljust(10) + "|"
        matrix.append(header)
        matrix.append("-" * len(header))

        # Data rows
        for candidate in ranked_candidates[:top_n]:
            row = (f"| {candidate['name'][:18]}".ljust(20) +
                   f"| {candidate['match_score']:5.1f}%".ljust(10) +
                   f"| {candidate['trust_score']:5.1f}%".ljust(10) +
                   f"| {candidate['potential_score']:5.1f}%".ljust(12) +
                   f"| {candidate.get('consistency_score', 0):5.1f}%".ljust(14) +
                   f"| {candidate.get('future_score', 0):5.1f}%".ljust(10) +
                   f"| {candidate['final_score']:5.1f}%".ljust(10) + "|")
            matrix.append(row)

        matrix.append("=" * len(header))
        matrix.append("")
        matrix.append("* Higher scores indicate better performance")
        matrix.append("** All scores are normalized to 0-100 scale")

        return "\n".join(matrix)