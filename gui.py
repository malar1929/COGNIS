"""
COGNIS - Graphical User Interface
Handles all Tkinter GUI components and user interactions
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import threading
from pathlib import Path
import json
from datetime import datetime
from PyPDF2 import PdfReader

from resume_analyzer import ResumeAnalyzer
from jd_matcher import JDMather
from trust_score import TrustScoreAnalyzer
from potential_score import PotentialScoreAnalyzer
from consistency_engine import ConsistencyEngine
from ranking_engine import RankingEngine
from future_simulator import FutureSimulator
from dna_visualizer import DNAVisualizer
from report_generator import ReportGenerator
from career_recommender import recommend_careers


class CognisGUI:
    """Main GUI application class"""

    def __init__(self):
        """Initialize the GUI application"""
        self.root = tk.Tk()
        self.root.title("COGNIS - Human Potential Compiler")
        self.root.geometry("1400x800")
        self.root.configure(bg='#2c3e50')

        # Application state
        self.resume_files = []
        self.jd_content = None
        self.analysis_results = {}
        self.selected_candidates = []
        self.current_candidate = None

        # Initialize modules
        self.resume_analyzer = ResumeAnalyzer()
        self.jd_matcher = JDMather()
        self.trust_analyzer = TrustScoreAnalyzer()
        self.potential_analyzer = PotentialScoreAnalyzer()
        self.consistency_engine = ConsistencyEngine()
        self.ranking_engine = RankingEngine()
        self.future_simulator = FutureSimulator()
        self.dna_visualizer = DNAVisualizer()
        self.report_generator = ReportGenerator()

        # Setup UI
        self.setup_menu()
        self.setup_main_layout()

    def setup_menu(self):
        """Setup application menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Load Resumes", command=self.load_resumes)
        file_menu.add_command(label="Load Job Description", command=self.load_job_description)
        file_menu.add_separator()
        file_menu.add_command(label="Export Report", command=self.export_report)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Tools Menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Run Full Analysis", command=self.run_full_analysis)
        tools_menu.add_command(label="View DNA Visualization", command=self.view_dna)
        tools_menu.add_separator()
        tools_menu.add_command(label="Clear All Data", command=self.clear_data)

        # Help Menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Documentation", command=self.show_documentation)
        help_menu.add_command(label="About", command=self.show_about)

    def setup_main_layout(self):
        """Setup main application layout"""
        # Create main container
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left Panel - File Management
        self.left_panel = ttk.LabelFrame(self.main_container, text="File Management", padding=10)
        self.left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 10))

        # Resume section
        ttk.Label(self.left_panel, text="Resumes:").pack(anchor=tk.W)
        self.resume_listbox = tk.Listbox(self.left_panel, height=10, width=40)
        self.resume_listbox.pack(fill=tk.BOTH, expand=True, pady=5)

        btn_frame = ttk.Frame(self.left_panel)
        btn_frame.pack(fill=tk.X, pady=5)
        ttk.Button(btn_frame, text="Add Resumes", command=self.load_resumes).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Clear", command=self.clear_resumes).pack(side=tk.LEFT, padx=2)

        # JD section
        ttk.Label(self.left_panel, text="Job Description:").pack(anchor=tk.W, pady=(10, 0))
        self.jd_text = tk.Text(self.left_panel, height=10, width=40, wrap=tk.WORD)
        self.jd_text.pack(fill=tk.BOTH, expand=True, pady=5)

        ttk.Button(self.left_panel, text="Load JD", command=self.load_job_description).pack(pady=5)

        # Action buttons
        action_frame = ttk.Frame(self.left_panel)
        action_frame.pack(fill=tk.X, pady=10)
        ttk.Button(action_frame, text="▶ Run Analysis", command=self.run_full_analysis).pack(side=tk.LEFT, padx=2)
        ttk.Button(action_frame, text="View DNA", command=self.view_dna).pack(side=tk.LEFT, padx=2)
        ttk.Button(
            action_frame,
            text="Compare",
            command=self.compare_candidates
        ).pack(side=tk.LEFT, padx=2)

        # Center Panel - Results
        self.center_panel = ttk.LabelFrame(self.main_container, text="Analysis Results", padding=10)
        self.center_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Results Notebook
        self.notebook = ttk.Notebook(self.center_panel)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Summary Tab
        self.summary_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.summary_tab, text="Summary")
        self.summary_text = scrolledtext.ScrolledText(self.summary_tab, wrap=tk.WORD, font=('Courier', 10))
        self.summary_text.pack(fill=tk.BOTH, expand=True)

        # Ranking Tab
        self.ranking_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.ranking_tab, text="Ranking")
        self.ranking_tree = ttk.Treeview(
            self.ranking_tab,
            columns=('Name', 'Match', 'Trust', 'Potential', 'Overall'),
            show='headings',
            selectmode='extended'
        )
        for col in ['Name', 'Match', 'Trust', 'Potential', 'Overall']:
            self.ranking_tree.heading(col, text=col)
            self.ranking_tree.column(col, width=100)
        self.ranking_tree.pack(fill=tk.BOTH, expand=True)
        self.ranking_tree.bind('<Double-Button-1>', self.on_candidate_select)

        # DNA Tab
        self.dna_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.dna_tab, text="DNA Profile")
        self.dna_text = scrolledtext.ScrolledText(self.dna_tab, wrap=tk.WORD, font=('Courier', 10))
        self.dna_text.pack(fill=tk.BOTH, expand=True)

        # Right Panel - Details
        self.right_panel = ttk.LabelFrame(self.main_container, text="Candidate Details", padding=10)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)

        self.details_text = scrolledtext.ScrolledText(self.right_panel, wrap=tk.WORD, height=30, width=35)
        self.details_text.pack(fill=tk.BOTH, expand=True)

        # Status Bar
        self.status_bar = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def load_resumes(self):
        """Load resume files"""
        files = filedialog.askopenfilenames(
            title="Select Resume Files",
            filetypes=[
                ("Resume Files", "*.txt *.pdf"),
                ("PDF Files", "*.pdf"),
                ("Text Files", "*.txt"),
                ("All Files", "*.*")
            ]
        )
        if files:
            self.resume_files = list(files)
            self.resume_listbox.delete(0, tk.END)
            for file in files:
                self.resume_listbox.insert(tk.END, os.path.basename(file))
            self.status_bar.config(text=f"Loaded {len(files)} resumes")
            messagebox.showinfo("Success", f"Loaded {len(files)} resumes successfully!")

    def clear_resumes(self):
        """Clear loaded resumes"""
        self.resume_files = []
        self.resume_listbox.delete(0, tk.END)
        self.status_bar.config(text="Cleared resumes")

    def load_job_description(self):
        """Load job description file"""
        file = filedialog.askopenfilename(
            title="Select Job Description",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file:
            with open(file, 'r', encoding='utf-8') as f:
                self.jd_content = f.read()
                self.jd_text.delete(1.0, tk.END)
                self.jd_text.insert(1.0, self.jd_content)
                self.status_bar.config(text="Job description loaded")
                messagebox.showinfo("Success", "Job description loaded successfully!")

    def run_full_analysis(self):
        """Run complete analysis on all loaded resumes"""
        if not self.resume_files:
            messagebox.showerror("Error", "No resumes loaded!")
            return

        if not self.jd_content:
            messagebox.showerror("Error", "No job description loaded!")
            return

        # Run analysis in separate thread
        self.status_bar.config(text="Running analysis...")
        threading.Thread(target=self._perform_analysis, daemon=True).start()

    def _perform_analysis(self):
        """Perform the actual analysis (runs in background)"""
        try:
            self.analysis_results = {}
            candidates = []

            # Parse job description
            jd_skills = self.jd_matcher.extract_skills(self.jd_content)

            for resume_file in self.resume_files:
                if resume_file.lower().endswith(".pdf"):
                    reader = PdfReader(resume_file)
                    resume_content = ""

                    for page in reader.pages:
                        text = page.extract_text()
                        if text:
                            resume_content += text + "\n"

                else:
                    with open(resume_file, 'r', encoding='utf-8') as f:
                        resume_content = f.read()

                # Parse resume
                parsed_resume = self.resume_analyzer.analyze_resume(
                    resume_content,
                    resume_file
                )
                candidate_name = parsed_resume.get('name', os.path.basename(resume_file))

                # Calculate scores
                match_score = self.jd_matcher.calculate_match_score(parsed_resume, jd_skills)
                trust_score = self.trust_analyzer.calculate_trust_score(resume_content)
                potential_score = self.potential_analyzer.calculate_potential_score(parsed_resume)
                consistency = self.consistency_engine.calculate_consistency(resume_content)
                future_score = self.future_simulator.simulate_future(parsed_resume, match_score)

                # Store results
                # Calculate overall score
                overall_score = (
                        match_score * 0.25 +
                        trust_score * 0.20 +
                        potential_score * 0.25 +
                        consistency * 0.15 +
                        future_score * 0.15
                )

                # Shortlist decision
                if overall_score >= 70 and match_score >= 60:
                    shortlist_decision = "SHORTLISTED"
                elif overall_score >= 55 and match_score >= 45:
                    shortlist_decision = "REVIEW"
                else:
                    shortlist_decision = "NOT RECOMMENDED"

                # Store results
                candidate_data = {
                    'name': candidate_name,
                    'file': os.path.basename(resume_file),
                    'content': resume_content,
                    'parsed': parsed_resume,
                    'match_score': match_score,
                    'trust_score': trust_score,
                    'potential_score': potential_score,
                    'consistency_score': consistency,
                    'future_score': future_score,
                    'overall_score': overall_score,
                    'shortlist_decision': shortlist_decision
                }


                candidates.append(candidate_data)
                self.analysis_results[candidate_name] = candidate_data
                # Shortlist decision
            # Rank candidates
            ranked = self.ranking_engine.rank_candidates(candidates)

            # Update UI in main thread
            self.root.after(0, lambda: self._update_results(ranked))

        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Analysis failed: {str(e)}"))
            self.root.after(0, lambda: self.status_bar.config(text="Analysis failed"))

    def _update_results(self, ranked_candidates):
        """Update UI with analysis results"""
        # Update summary
        self.summary_text.delete(1.0, tk.END)
        self.summary_text.insert(1.0, "=== COGNIS ANALYSIS SUMMARY ===\n\n")
        self.summary_text.insert(tk.END, f"Total Candidates: {len(ranked_candidates)}\n")
        self.summary_text.insert(tk.END, f"Job Title: {self.jd_content[:100]}...\n\n")

        self.summary_text.insert(tk.END, "Top 3 Candidates:\n")
        self.summary_text.insert(tk.END, "-" * 50 + "\n")
        self.details_text.delete(1.0, tk.END)
        for i, candidate in enumerate(ranked_candidates[:3], 1):
            self.summary_text.insert(tk.END, f"{i}. {candidate['name']}\n")
            self.summary_text.insert(tk.END, f"   Overall: {candidate['overall_score']:.1f}%\n")
            self.summary_text.insert(tk.END, f"   Match: {candidate['match_score']:.1f}%\n")
            self.summary_text.insert(tk.END, f"   Trust: {candidate['trust_score']:.1f}%\n")
            self.summary_text.insert(tk.END, f"   Potential: {candidate['potential_score']:.1f}%\n\n")
            # SHORTLIST DECISION
            self.details_text.insert(
                tk.END,
                f"SHORTLIST DECISION: {candidate.get('shortlist_decision', 'N/A')}\n\n"
            )

        # Update ranking tree
        self.ranking_tree.delete(*self.ranking_tree.get_children())
        for candidate in ranked_candidates:
            self.ranking_tree.insert('', 'end', values=(
                candidate['name'],
                f"{candidate['match_score']:.1f}%",
                f"{candidate['trust_score']:.1f}%",
                f"{candidate['potential_score']:.1f}%",
                f"{candidate['overall_score']:.1f}%"
            ))

        # Update status
        self.status_bar.config(text="Analysis complete!")
        messagebox.showinfo("Success", "Analysis completed successfully!")

    def on_candidate_select(self, event):
        """Handle candidate selection from ranking tree"""

        selection = self.ranking_tree.selection()

        if not selection:
            return

        selected_candidates = []

        for item_id in selection:
            item = self.ranking_tree.item(item_id)
            candidate_name = item['values'][0]

            if candidate_name in self.analysis_results:
                selected_candidates.append(
                    self.analysis_results[candidate_name]
                )

        self.selected_candidates = selected_candidates

        # Show details of the first selected candidate
        if selected_candidates:
            self.show_candidate_details(selected_candidates[0])

    def compare_candidates(self):
        """Compare selected candidates"""

        if len(self.selected_candidates) < 2:
            messagebox.showwarning(
                "Comparison",
                "Please select at least 2 candidates."
            )
            return

        if len(self.selected_candidates) > 3:
            messagebox.showwarning(
                "Comparison",
                "Please select maximum 3 candidates."
            )
            return

        compare_window = tk.Toplevel(self.root)
        compare_window.title("Candidate Comparison")
        compare_window.geometry("800x400")

        title = ttk.Label(
            compare_window,
            text="CANDIDATE COMPARISON",
            font=("Arial", 14, "bold")
        )
        title.pack(pady=10)

        columns = ["Metric"]

        for candidate in self.selected_candidates:
            columns.append(candidate["name"])

        tree = ttk.Treeview(
            compare_window,
            columns=columns,
            show="headings"
        )

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        metrics = [
            ("Match", "match_score"),
            ("Trust", "trust_score"),
            ("Potential", "potential_score"),
            ("Consistency", "consistency_score"),
            ("Future Growth", "future_score"),
            ("Overall", "overall_score")
        ]

        for metric_name, key in metrics:

            values = [metric_name]

            for candidate in self.selected_candidates:
                values.append(
                    f"{candidate[key]:.1f}%"
                )

            tree.insert("", tk.END, values=values)

    def show_candidate_details(self, candidate):
        """Show detailed candidate information"""
        self.details_text.delete(1.0, tk.END)
        self.details_text.insert(tk.END, f"=== {candidate['name']} ===\n")
        self.details_text.insert(tk.END, "=" * 30 + "\n\n")
        self.details_text.insert(tk.END, "SCORE BREAKDOWN:\n")
        self.details_text.insert(tk.END, "-" * 30 + "\n")

        self.details_text.insert(
            tk.END,
            f"Match Score      : {candidate['match_score']:.1f}%  (25%)\n"
        )

        self.details_text.insert(
            tk.END,
            f"Trust Score      : {candidate['trust_score']:.1f}%  (20%)\n"
        )

        self.details_text.insert(
            tk.END,
            f"Potential Score  : {candidate['potential_score']:.1f}%  (25%)\n"
        )

        self.details_text.insert(
            tk.END,
            f"Consistency      : {candidate['consistency_score']:.1f}%  (15%)\n"
        )

        self.details_text.insert(
            tk.END,
            f"Future Growth    : {candidate['future_score']:.1f}%  (15%)\n"
        )

        self.details_text.insert(tk.END, "-" * 30 + "\n")

        self.details_text.insert(
            tk.END,
            f"OVERALL SCORE    : {candidate['overall_score']:.1f}%\n\n"
        )

        self.details_text.insert(tk.END, "KEY SKILLS:\n")
        skills = candidate['parsed'].get('skills', [])[:10]

        for skill in skills:
            self.details_text.insert(tk.END, f"• {skill}\n")

        # MATCHED SKILLS
        self.details_text.insert(tk.END, "\nMATCHED SKILLS:\n")

        candidate_skills = set(candidate['parsed'].get('skills', []))
        jd_skills = set(self.jd_matcher.extract_skills(self.jd_content))

        matched = candidate_skills.intersection(jd_skills)
        missing = jd_skills - candidate_skills
        # CAREER PATH RECOMMENDATION
        self.details_text.insert(tk.END, "\n\nCAREER PATH:\n")

        career_results = recommend_careers(
            candidate['parsed'].get('skills', [])
        )

        if career_results:
            best = career_results[0]
            # ALTERNATIVE CAREERS
            self.details_text.insert(
                tk.END,
                "\nAlternative Careers:\n"
            )

            for career in career_results[1:4]:
                self.details_text.insert(
                    tk.END,
                    f"• {career['career']} - {career['score']}%\n"
                )

            self.details_text.insert(
                tk.END,
                f"\n🎯 Best Career: {best['career']}\n"
            )

            self.details_text.insert(
                tk.END,
                f"Career Fit: {best['score']}%\n"
            )

            self.details_text.insert(
                tk.END,
                "\nMatched Skills:\n"
            )

            for skill in best['matched_skills']:
                self.details_text.insert(
                    tk.END,
                    f"• {skill}\n"
                )

            self.details_text.insert(
                tk.END,
                "\nSkills to Improve:\n"
            )

            for skill in best['missing_skills']:
                self.details_text.insert(
                    tk.END,
                    f"• {skill}\n"
                )

        if matched:
            for skill in matched:
                self.details_text.insert(tk.END, f"✓ {skill}\n")
        else:
            self.details_text.insert(tk.END, "No matched skills\n")

        # MISSING SKILLS
        self.details_text.insert(tk.END, "\nMISSING SKILLS:\n")

        if missing:
            for skill in missing:
                self.details_text.insert(tk.END, f"✗ {skill}\n")
        else:
            self.details_text.insert(tk.END, "No missing skills\n")

        # PROJECTS
        self.details_text.insert(tk.END, "\nPROJECTS:\n")
        projects = candidate['parsed'].get('projects', [])[:5]


        if projects:
            for project in projects:
                self.details_text.insert(tk.END, f"• {project}\n")
        else:
            self.details_text.insert(tk.END, "No projects found\n")

        # CERTIFICATIONS
        self.details_text.insert(tk.END, "\nCERTIFICATIONS:\n")
        certifications = candidate['parsed'].get('certifications', [])[:5]

        if certifications:
            for cert in certifications:
                self.details_text.insert(tk.END, f"• {cert}\n")
        else:
            self.details_text.insert(tk.END, "No certifications found\n")

    def view_dna(self):
        if not self.analysis_results:
            messagebox.showerror("Error", "No analysis results available!")
            return

        self.dna_text.delete(1.0, tk.END)

        for candidate_name, candidate_data in self.analysis_results.items():
            summary = self.dna_visualizer.generate_candidate_summary(
                candidate_name,
                candidate_data
            )

            self.dna_text.insert(tk.END, summary)
            self.dna_text.insert(tk.END, "\n\n")

        self.notebook.select(self.dna_tab)

        try:
            files = self.dna_visualizer.generate_visualization(
                self.analysis_results
            )

            self.status_bar.config(text="DNA visualization generated")

            messagebox.showinfo(
                "Success",
                f"{len(files)} DNA charts saved in results folder"
            )


        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Failed to generate visualization: {str(e)}"
            )

    def export_report(self):
        """Export comprehensive report"""
        if not self.analysis_results:
            messagebox.showerror("Error", "No analysis results available!")
            return

        try:
            report_path = self.report_generator.generate_report(self.analysis_results)
            messagebox.showinfo("Success", f"Report generated: {report_path}")
            self.status_bar.config(text=f"Report exported to {report_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")

    def clear_data(self):
        """Clear all loaded data"""
        self.resume_files = []
        self.resume_listbox.delete(0, tk.END)
        self.jd_text.delete(1.0, tk.END)
        self.jd_content = None
        self.analysis_results = {}
        self.summary_text.delete(1.0, tk.END)
        self.ranking_tree.delete(*self.ranking_tree.get_children())
        self.details_text.delete(1.0, tk.END)
        self.dna_text.delete(1.0, tk.END)
        self.status_bar.config(text="Cleared all data")

    def show_documentation(self):
        """Show documentation window"""
        doc_window = tk.Toplevel(self.root)
        doc_window.title("Documentation")
        doc_window.geometry("600x400")

        doc_text = scrolledtext.ScrolledText(doc_window, wrap=tk.WORD)
        doc_text.pack(fill=tk.BOTH, expand=True)

        doc_text.insert(tk.END, """
COGNIS - Human Potential Compiler
================================

How to Use:
1. Load resumes (TXT files)
2. Load job description (TXT file)
3. Click "Run Analysis"
4. View results in tabs
5. Export reports as needed

Features:
- Resume parsing and analysis
- Match score calculation
- Trust score evaluation
- Potential detection
- Consistency analysis
- Future success simulation
- DNA visualization
- Report generation

For more information, visit the documentation.
""")

    def show_about(self):
        """Show about window"""
        messagebox.showinfo("About COGNIS",
                            "COGNIS - Human Potential Compiler v1.0\n\n"
                            "An advanced hiring intelligence platform\n"
                            "that evaluates candidate suitability,\n"
                            "credibility, growth potential, and\n"
                            "future success.\n\n"
                            "Built with Python and Tkinter\n"
                            "© 2024 All Rights Reserved")

    def run(self):
        """Run the application"""
        self.root.mainloop()