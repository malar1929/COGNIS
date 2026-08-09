"""
COGNIS - Report Generation System
Generates comprehensive reports in multiple formats
"""

import os
import json
from datetime import datetime
from pathlib import Path


class ReportGenerator:
    """Generate comprehensive reports from analysis results"""

    def __init__(self):
        """Initialize report generator"""
        self.report_dir = 'reports'
        if not os.path.exists(self.report_dir):
            os.makedirs(self.report_dir)

    def generate_report(self, analysis_results):
        """
        Generate comprehensive report for all candidates
        Returns path to generated report file
        """
        if not analysis_results:
            return None

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"cognis_report_{timestamp}.txt"
        report_path = os.path.join(self.report_dir, report_filename)

        with open(report_path, 'w', encoding='utf-8') as f:
            # Write report header
            f.write("=" * 80 + "\n")
            f.write("COGNIS - HUMAN POTENTIAL COMPILER\n")
            f.write("Comprehensive Candidate Analysis Report\n")
            f.write("=" * 80 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Candidates: {len(analysis_results)}\n")
            f.write("=" * 80 + "\n\n")

            # Executive Summary
            f.write("EXECUTIVE SUMMARY\n")
            f.write("-" * 80 + "\n")

            # Calculate averages
            avg_scores = {
                'match': 0,
                'trust': 0,
                'potential': 0,
                'consistency': 0,
                'future': 0,
                'overall': 0
            }

            for data in analysis_results.values():
                avg_scores['match'] += data.get('match_score', 0)
                avg_scores['trust'] += data.get('trust_score', 0)
                avg_scores['potential'] += data.get('potential_score', 0)
                avg_scores['consistency'] += data.get('consistency_score', 0)
                avg_scores['future'] += data.get('future_score', 0)
                avg_scores['overall'] += data.get('overall_score', 0)

            total = len(analysis_results)
            avg_scores = {k: v / total for k, v in avg_scores.items()}

            f.write(f"Average Match Score:     {avg_scores['match']:.1f}%\n")
            f.write(f"Average Trust Score:     {avg_scores['trust']:.1f}%\n")
            f.write(f"Average Potential Score: {avg_scores['potential']:.1f}%\n")
            f.write(f"Average Consistency:     {avg_scores['consistency']:.1f}%\n")
            f.write(f"Average Future Score:    {avg_scores['future']:.1f}%\n")
            f.write(f"Average Overall Score:   {avg_scores['overall']:.1f}%\n")
            f.write("\n")

            # Top candidates
            f.write("TOP 3 CANDIDATES\n")
            f.write("-" * 80 + "\n")

            sorted_candidates = sorted(analysis_results.items(),
                                       key=lambda x: x[1].get('overall_score', 0),
                                       reverse=True)

            for rank, (name, data) in enumerate(sorted_candidates[:3], 1):
                f.write(f"\n{rank}. {name}\n")
                f.write(f"   Overall Score: {data.get('overall_score', 0):.1f}%\n")
                f.write(f"   Match Score:   {data.get('match_score', 0):.1f}%\n")
                f.write(f"   Trust Score:   {data.get('trust_score', 0):.1f}%\n")
                f.write(f"   Potential:     {data.get('potential_score', 0):.1f}%\n")

            f.write("\n" + "=" * 80 + "\n\n")

            # Detailed candidate reports
            f.write("DETAILED CANDIDATE REPORTS\n")
            f.write("=" * 80 + "\n\n")

            for name, data in sorted_candidates:
                f.write(f"CANDIDATE: {name}\n")
                f.write("-" * 80 + "\n")

                # Parse resume content
                content = data.get('content', '')
                parsed = data.get('parsed', {})

                # Basic information
                f.write(f"Email: {parsed.get('email', 'Unknown')}\n")
                f.write(f"Phone: {parsed.get('phone', 'Unknown')}\n")
                f.write(f"Experience: {parsed.get('experience_years', 0):.1f} years\n")
                f.write("\n")

                # Scores
                f.write("SCORES:\n")
                f.write(f"  Match Score:     {data.get('match_score', 0):.1f}%\n")
                f.write(f"  Trust Score:     {data.get('trust_score', 0):.1f}%\n")
                f.write(f"  Potential Score: {data.get('potential_score', 0):.1f}%\n")
                f.write(f"  Consistency:     {data.get('consistency_score', 0):.1f}%\n")
                f.write(f"  Future Score:    {data.get('future_score', 0):.1f}%\n")
                f.write(f"  Overall Score:   {data.get('overall_score', 0):.1f}%\n")
                f.write("\n")

                # Skills
                skills = parsed.get('skills', [])
                if skills:
                    f.write("KEY SKILLS:\n")
                    for skill in skills[:15]:
                        f.write(f"  • {skill}\n")
                    f.write("\n")

                # Achievements
                achievements = parsed.get('achievements', [])
                if achievements:
                    f.write("TOP ACHIEVEMENTS:\n")
                    for achievement in achievements[:5]:
                        f.write(f"  • {achievement}\n")
                    f.write("\n")

                # Education
                education = parsed.get('education', [])
                if education:
                    f.write("EDUCATION:\n")
                    for edu in education:
                        f.write(
                            f"  • {edu.get('degree', '')} from {edu.get('institution', '')} ({edu.get('year', '')})\n")
                    f.write("\n")

                # Certifications
                certifications = parsed.get('certifications', [])
                if certifications:
                    f.write("CERTIFICATIONS:\n")
                    for cert in certifications[:5]:
                        f.write(f"  • {cert}\n")
                    f.write("\n")

                # Future simulation
                f.write("FUTURE SUCCESS SIMULATION:\n")
                future_score = data.get('future_score', 0)
                if future_score >= 80:
                    f.write("  Prediction: High growth potential\n")
                elif future_score >= 60:
                    f.write("  Prediction: Moderate growth potential\n")
                else:
                    f.write("  Prediction: Focus on skill development needed\n")
                f.write("\n")

                # Strengths and weaknesses
                f.write("STRENGTHS:\n")
                strengths = []
                if data.get('match_score', 0) >= 70:
                    strengths.append("Strong skill match with requirements")
                if data.get('trust_score', 0) >= 70:
                    strengths.append("High credibility and verifiable achievements")
                if data.get('potential_score', 0) >= 70:
                    strengths.append("Excellent growth potential")
                if data.get('consistency_score', 0) >= 70:
                    strengths.append("Consistent career progression")
                if not strengths:
                    strengths.append("Balanced performance across metrics")
                for strength in strengths:
                    f.write(f"  ✓ {strength}\n")

                f.write("\nAREAS FOR IMPROVEMENT:\n")
                weaknesses = []
                if data.get('match_score', 0) < 60:
                    weaknesses.append("Skill gaps for this role")
                if data.get('trust_score', 0) < 60:
                    weaknesses.append("Limited verifiable achievements")
                if data.get('potential_score', 0) < 60:
                    weaknesses.append("Growth indicators need enhancement")
                if data.get('consistency_score', 0) < 60:
                    weaknesses.append("Career progression pattern inconsistent")
                if not weaknesses:
                    weaknesses.append("Well-rounded profile")
                for weakness in weaknesses:
                    f.write(f"  ○ {weakness}\n")

                f.write("\n" + "=" * 80 + "\n\n")

            # Recommendations
            f.write("OVERALL RECOMMENDATIONS\n")
            f.write("-" * 80 + "\n")

            # Generate overall recommendations
            if avg_scores['overall'] >= 70:
                f.write("• High-quality candidate pool - focus on soft skills and cultural fit\n")
            elif avg_scores['overall'] >= 50:
                f.write("• Moderate quality candidates - consider additional screening\n")
            else:
                f.write("• Consider expanding recruitment channels for better candidates\n")

            if avg_scores['match'] < avg_scores['potential']:
                f.write("• Candidates show high potential but skill gaps - invest in training\n")
            elif avg_scores['match'] > avg_scores['potential']:
                f.write("• Strong skills but limited growth indicators - consider motivation\n")

            f.write("• Schedule interviews with top 3 candidates for deeper evaluation\n")
            f.write("• Validate top candidates' achievements during interviews\n")

            f.write("\n" + "=" * 80 + "\n")
            f.write("End of Report\n")
            f.write("=" * 80 + "\n")

        return report_path

    def generate_json_report(self, analysis_results):
        """
        Generate JSON format report for data export
        """
        if not analysis_results:
            return None

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_filename = f"cognis_data_{timestamp}.json"
        json_path = os.path.join(self.report_dir, json_filename)

        # Prepare data for JSON export
        export_data = {
            'generated': datetime.now().isoformat(),
            'total_candidates': len(analysis_results),
            'candidates': []
        }

        for name, data in analysis_results.items():
            candidate_data = {
                'name': name,
                'scores': {
                    'match': data.get('match_score', 0),
                    'trust': data.get('trust_score', 0),
                    'potential': data.get('potential_score', 0),
                    'consistency': data.get('consistency_score', 0),
                    'future': data.get('future_score', 0),
                    'overall': data.get('overall_score', 0)
                }
            }

            # Add parsed data if available
            parsed = data.get('parsed', {})
            if parsed:
                candidate_data['experience_years'] = parsed.get('experience_years', 0)
                candidate_data['skills'] = parsed.get('skills', [])
                candidate_data['achievements'] = parsed.get('achievements', [])
                candidate_data['education'] = parsed.get('education', [])
                candidate_data['certifications'] = parsed.get('certifications', [])

            export_data['candidates'].append(candidate_data)

        # Write JSON file
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)

        return json_path

    def generate_summary_report(self, analysis_results):
        """
        Generate quick summary report for recruiters
        """
        if not analysis_results:
            return None

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        summary_filename = f"cognis_summary_{timestamp}.txt"
        summary_path = os.path.join(self.report_dir, summary_filename)

        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write("COGNIS - QUICK SUMMARY\n")
            f.write("=" * 60 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Candidates: {len(analysis_results)}\n")
            f.write("-" * 60 + "\n\n")

            # Sort by overall score
            sorted_candidates = sorted(analysis_results.items(),
                                       key=lambda x: x[1].get('overall_score', 0),
                                       reverse=True)

            f.write("RANK | NAME | OVERALL | MATCH | TRUST | POTENTIAL\n")
            f.write("-" * 60 + "\n")

            for rank, (name, data) in enumerate(sorted_candidates, 1):
                f.write(f"{rank:4d} | {name[:20]:20s} | "
                        f"{data.get('overall_score', 0):5.1f}  | "
                        f"{data.get('match_score', 0):5.1f}  | "
                        f"{data.get('trust_score', 0):5.1f}  | "
                        f"{data.get('potential_score', 0):5.1f}\n")

            f.write("-" * 60 + "\n")
            f.write(f"Top Candidate: {sorted_candidates[0][0] if sorted_candidates else 'None'}\n")

        return summary_path