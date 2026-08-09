"""
COGNIS - DNA Visualization Dashboard
Creates visual representations of candidate profiles
"""

import os
import json
from datetime import datetime
import matplotlib

matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Circle, Rectangle, Polygon
import numpy as np


class DNAVisualizer:
    """Generate visual representations of candidate DNA"""

    def __init__(self):
        """Initialize DNA visualizer"""
        self.output_dir = 'results'
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate_visualization(self, analysis_results):
        """
        Generate comprehensive DNA visualization for all candidates
        """
        if not analysis_results:
            return None

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Generate multiple visualizations
        visualizations = []

        # 1. Radar chart for each candidate
        for candidate_name, candidate_data in analysis_results.items():
            radar_file = self._generate_radar_chart(candidate_name, candidate_data, timestamp)
            if radar_file:
                visualizations.append(radar_file)

        # 2. Comparison radar chart for top candidates
        comparison_file = self._generate_comparison_chart(analysis_results, timestamp)
        if comparison_file:
            visualizations.append(comparison_file)

        # 3. DNA helix visualization
        dna_file = self._generate_dna_helix(analysis_results, timestamp)
        if dna_file:
            visualizations.append(dna_file)

        # 4. Performance heatmap
        heatmap_file = self._generate_performance_heatmap(analysis_results, timestamp)
        if heatmap_file:
            visualizations.append(heatmap_file)

        return visualizations

    def _generate_radar_chart(self, candidate_name, candidate_data, timestamp):
        """Generate individual radar chart for a candidate"""
        try:
            # Define categories for radar chart
            categories = ['Match Score', 'Trust Score', 'Potential', 'Consistency', 'Future']

            # Get scores
            scores = [
                candidate_data.get('match_score', 0),
                candidate_data.get('trust_score', 0),
                candidate_data.get('potential_score', 0),
                candidate_data.get('consistency_score', 0),
                candidate_data.get('future_score', 0)
            ]

            # Normalize to percentage
            scores = [min(100, max(0, s)) for s in scores]

            # Create figure
            fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))

            # Number of variables
            N = len(categories)
            angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
            angles += angles[:1]  # Close the loop

            # Add scores
            scores += scores[:1]  # Close the loop

            # Plot
            ax.plot(angles, scores, 'o-', linewidth=2, color='#3498db', label=candidate_name)
            ax.fill(angles, scores, alpha=0.25, color='#3498db')

            # Set category labels
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(categories, fontsize=12)

            # Set y-axis limits
            ax.set_ylim(0, 100)
            ax.set_yticks([20, 40, 60, 80, 100])
            ax.set_yticklabels(['20%', '40%', '60%', '80%', '100%'], fontsize=10)

            # Add title
            plt.title(f"COGNIS DNA Profile: {candidate_name}",
                      fontsize=16, fontweight='bold', pad=20)

            # Add grid
            ax.grid(True)

            # Add legend
            ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

            # Save
            filename = f"candidate_dna_{candidate_name.replace(' ', '_')}_{timestamp}.png"
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()

            return filepath

        except Exception as e:
            print(f"Error generating radar chart: {e}")
            return None

    def _generate_comparison_chart(self, analysis_results, timestamp):
        """Generate comparison radar chart for top candidates"""
        try:
            # Get top 3 candidates
            candidates = list(analysis_results.items())
            candidates.sort(key=lambda x: x[1].get('overall_score', 0), reverse=True)
            top_candidates = candidates[:3]

            if not top_candidates:
                return None

            # Define categories
            categories = ['Match Score', 'Trust Score', 'Potential', 'Consistency', 'Future']
            N = len(categories)
            angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
            angles += angles[:1]

            # Create figure
            fig, ax = plt.subplots(figsize=(12, 12), subplot_kw=dict(projection='polar'))

            # Colors for different candidates
            colors = ['#3498db', '#e74c3c', '#2ecc71']

            # Plot each candidate
            for i, (name, data) in enumerate(top_candidates):
                scores = [
                    data.get('match_score', 0),
                    data.get('trust_score', 0),
                    data.get('potential_score', 0),
                    data.get('consistency_score', 0),
                    data.get('future_score', 0)
                ]
                scores = [min(100, max(0, s)) for s in scores]
                scores += scores[:1]

                ax.plot(angles, scores, 'o-', linewidth=2, color=colors[i],
                        label=f"#{i + 1}: {name}")
                ax.fill(angles, scores, alpha=0.1, color=colors[i])

            # Set category labels
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(categories, fontsize=12)

            # Set y-axis limits
            ax.set_ylim(0, 100)
            ax.set_yticks([20, 40, 60, 80, 100])
            ax.set_yticklabels(['20%', '40%', '60%', '80%', '100%'], fontsize=10)

            # Add title
            plt.title("COGNIS DNA Comparison: Top Candidates",
                      fontsize=16, fontweight='bold', pad=20)

            # Add grid
            ax.grid(True)

            # Add legend
            ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

            # Save
            filename = f"comparison_dna_{timestamp}.png"
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()

            return filepath

        except Exception as e:
            print(f"Error generating comparison chart: {e}")
            return None

    def _generate_dna_helix(self, analysis_results, timestamp):
        """Generate DNA helix visualization"""
        try:
            # Get top candidates
            candidates = list(analysis_results.items())
            candidates.sort(key=lambda x: x[1].get('overall_score', 0), reverse=True)

            if not candidates:
                return None

            # Create figure
            fig, ax = plt.subplots(figsize=(14, 10))

            # Prepare data for helix
            candidate_data = []
            for name, data in candidates[:5]:  # Top 5
                candidate_data.append({
                    'name': name,
                    'match': data.get('match_score', 0),
                    'trust': data.get('trust_score', 0),
                    'potential': data.get('potential_score', 0),
                    'consistency': data.get('consistency_score', 0),
                    'future': data.get('future_score', 0)
                })

            # Create helix visualization
            x_pos = np.linspace(0, 10, len(candidate_data))
            y_pos = np.arange(len(candidate_data))

            # Create bars for each metric
            width = 0.15
            colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6']
            metrics = ['match', 'trust', 'potential', 'consistency', 'future']
            metric_labels = ['Match', 'Trust', 'Potential', 'Consistency', 'Future']

            # Create grouped bar chart
            for i, (metric, color, label) in enumerate(zip(metrics, colors, metric_labels)):
                values = [d[metric] for d in candidate_data]
                offset = (i - len(metrics) / 2) * width
                bars = ax.bar(x_pos + offset, values, width,
                              color=color, alpha=0.8, label=label)

                # Add value labels on bars
                for bar, value in zip(bars, values):
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width() / 2., height + 2,
                            f'{value:.0f}%', ha='center', va='bottom', fontsize=8)

            # Customize chart
            ax.set_xlabel('Candidates', fontsize=12)
            ax.set_ylabel('Score (%)', fontsize=12)
            ax.set_title('COGNIS DNA Helix: Multi-dimensional Analysis',
                         fontsize=16, fontweight='bold')

            # Set x-axis labels
            ax.set_xticks(x_pos)
            ax.set_xticklabels([d['name'][:15] for d in candidate_data],
                               rotation=45, ha='right')

            # Set y-axis limits
            ax.set_ylim(0, 110)

            # Add grid
            ax.grid(True, alpha=0.3, axis='y')

            # Add legend
            ax.legend(loc='upper right', bbox_to_anchor=(1.15, 1))

            # Add overall scores as text
            for i, data in enumerate(candidate_data):
                overall = sum([data[m] for m in metrics]) / len(metrics)
                ax.text(x_pos[i], 105, f'Overall: {overall:.0f}%',
                        ha='center', fontsize=10, fontweight='bold')

            plt.tight_layout()

            # Save
            filename = f"dna_helix_{timestamp}.png"
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()

            return filepath

        except Exception as e:
            print(f"Error generating DNA helix: {e}")
            return None

    def _generate_performance_heatmap(self, analysis_results, timestamp):
        """Generate performance heatmap for all candidates"""
        try:
            if not analysis_results:
                return None

            # Prepare data for heatmap
            candidate_names = []
            metrics = ['Match Score', 'Trust Score', 'Potential', 'Consistency', 'Future', 'Overall']
            data_matrix = []

            for name, data in analysis_results.items():
                candidate_names.append(name[:20])  # Truncate long names
                data_matrix.append([
                    data.get('match_score', 0),
                    data.get('trust_score', 0),
                    data.get('potential_score', 0),
                    data.get('consistency_score', 0),
                    data.get('future_score', 0),
                    data.get('overall_score', 0)
                ])

            # Convert to numpy array
            data_array = np.array(data_matrix)

            # Create figure
            fig, ax = plt.subplots(figsize=(12, max(6, len(candidate_names) * 0.5)))

            # Create heatmap
            im = ax.imshow(data_array, cmap='RdYlGn', aspect='auto', vmin=0, vmax=100)

            # Set axis labels
            ax.set_xticks(np.arange(len(metrics)))
            ax.set_yticks(np.arange(len(candidate_names)))
            ax.set_xticklabels(metrics, fontsize=10)
            ax.set_yticklabels(candidate_names, fontsize=9)

            # Rotate x-axis labels
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right', rotation_mode='anchor')

            # Add colorbar
            cbar = ax.figure.colorbar(im, ax=ax)
            cbar.set_label('Score (%)', fontsize=10)

            # Add text annotations
            for i in range(len(candidate_names)):
                for j in range(len(metrics)):
                    text = ax.text(j, i, f'{data_array[i, j]:.0f}',
                                   ha='center', va='center', color='black', fontsize=8)

            # Add title
            ax.set_title('COGNIS Performance Heatmap: All Candidates',
                         fontsize=14, fontweight='bold', pad=20)

            plt.tight_layout()

            # Save
            filename = f"performance_heatmap_{timestamp}.png"
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()

            return filepath

        except Exception as e:
            print(f"Error generating heatmap: {e}")
            return None

    def generate_candidate_summary(self, candidate_name, candidate_data):
        """Generate text summary of candidate DNA"""
        summary = []
        summary.append("=" * 70)
        summary.append(f"COGNIS DNA SUMMARY: {candidate_name}")
        summary.append("=" * 70)
        summary.append("")
        summary.append("SCORE BREAKDOWN:")
        summary.append("-" * 40)
        summary.append(f"Match Score:     {candidate_data.get('match_score', 0):.1f}%")
        summary.append(f"Trust Score:     {candidate_data.get('trust_score', 0):.1f}%")
        summary.append(f"Potential Score: {candidate_data.get('potential_score', 0):.1f}%")
        summary.append(f"Consistency:     {candidate_data.get('consistency_score', 0):.1f}%")
        summary.append(f"Future Score:    {candidate_data.get('future_score', 0):.1f}%")
        summary.append(f"Overall Score:   {candidate_data.get('overall_score', 0):.1f}%")
        summary.append("")
        summary.append("STRENGTHS:")
        summary.append("-" * 40)

        # Identify strengths
        strengths = []
        scores = {
            'Match': candidate_data.get('match_score', 0),
            'Trust': candidate_data.get('trust_score', 0),
            'Potential': candidate_data.get('potential_score', 0),
            'Consistency': candidate_data.get('consistency_score', 0),
            'Future': candidate_data.get('future_score', 0)
        }

        for metric, score in scores.items():
            if score >= 80:
                strengths.append(f"• High {metric} Score: {score:.0f}%")

        if not strengths:
            strengths.append("• Balanced performance across all metrics")

        for strength in strengths:
            summary.append(strength)

        summary.append("")
        summary.append("AREAS FOR DEVELOPMENT:")
        summary.append("-" * 40)

        weaknesses = []
        for metric, score in scores.items():
            if score < 60:
                weaknesses.append(f"• {metric} Score could improve: {score:.0f}%")

        if not weaknesses:
            weaknesses.append("• Well-rounded profile with no significant gaps")

        for weakness in weaknesses:
            summary.append(weakness)

        summary.append("")
        summary.append("RECOMMENDATIONS:")
        summary.append("-" * 40)

        # Add recommendations based on scores
        if candidate_data.get('match_score', 0) < 70:
            summary.append("• Consider skill enhancement in key areas")
        if candidate_data.get('trust_score', 0) < 70:
            summary.append("• Add more verifiable achievements and metrics")
        if candidate_data.get('potential_score', 0) < 70:
            summary.append("• Seek challenging projects to demonstrate growth")
        if candidate_data.get('consistency_score', 0) < 70:
            summary.append("• Focus on consistent career progression")
        if candidate_data.get('future_score', 0) < 70:
            summary.append("• Develop skills aligned with future industry trends")

        summary.append("")
        summary.append("=" * 70)

        return "\n".join(summary)