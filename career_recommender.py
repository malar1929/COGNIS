CAREER_ROLES = {
    "Python Developer": [
        "python",
        "flask",
        "django",
        "sql",
        "git"
    ],

    "Data Analyst": [
        "python",
        "sql",
        "excel",
        "power bi",
        "pandas"
    ],

    "Data Scientist": [
        "python",
        "machine learning",
        "pandas",
        "numpy",
        "statistics"
    ],

    "Frontend Developer": [
        "html",
        "css",
        "javascript",
        "react"
    ],

    "Backend Developer": [
        "python",
        "flask",
        "sql",
        "api",
        "git"
    ]
}
def recommend_careers(skills):
    """
    Recommend careers based on candidate skills.
    """

    candidate_skills = set(
        skill.lower().strip()
        for skill in skills
    )

    results = []

    for career, required_skills in CAREER_ROLES.items():

        required = set(
            skill.lower().strip()
            for skill in required_skills
        )

        matched = candidate_skills.intersection(required)
        missing = required - candidate_skills

        if required:
            score = (len(matched) / len(required)) * 100
        else:
            score = 0

        results.append({
            "career": career,
            "score": round(score, 2),
            "matched_skills": sorted(matched),
            "missing_skills": sorted(missing)
        })

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results
if __name__ == "__main__":

    skills = [
        "Python",
        "Flask",
        "SQL",
        "Git"
    ]

    results = recommend_careers(skills)

    for result in results:
        print("\nCareer:", result["career"])
        print("Score:", result["score"], "%")
        print("Matched:", result["matched_skills"])
        print("Missing:", result["missing_skills"])