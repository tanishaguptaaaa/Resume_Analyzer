def score_resume(resume_data, resume_text, scoring_only=False):
    """
    Score the resume based on presence of key sections.
    """
    score = 0
    if 'Objective' in resume_text or 'Summary' in resume_text:
        score += 6
    if 'Education' in resume_text:
        score += 12
    if 'Experience' in resume_text:
        score += 16
    if 'Internship' in resume_text:
        score += 6
    if 'Skills' in resume_text:
        score += 7
    if 'Hobbies' in resume_text:
        score += 4
    if 'Interests' in resume_text:
        score += 5
    if 'Achievements' in resume_text:
        score += 13
    if 'Certifications' in resume_text:
        score += 12
    if 'Projects' in resume_text:
        score += 19

    return score
