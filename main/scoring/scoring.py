from llm.conversation import get_ielts_examiner_response


def score_response(response, confidence):
    """
    Score the user's response using LLM feedback on different aspects.
    """
    prompt = (
        f"I am an IELTS examiner. Evaluate the following response in detail:\n\n"
        f"Response: {response}\n\n"
        f"Rate it on a scale of 1 to 9 for the following categories:\n"
        f"1. Fluency & Coherence\n"
        f"2. Pronunciation\n"
        f"3. Grammar\n"
        f"4. Vocabulary\n"
        f"Provide a brief score summary in this format:\n"
        f"Fluency: [score]\n"
        f"Pronunciation: [score]\n"
        f"Grammar: [score]\n"
        f"Vocabulary: [score]\n\n"
        f"Recommendations: Give any improvement recommendations based on the feedback and scores\n"
    )

    # Get feedback and scores from the LLM
    feedback = get_ielts_examiner_response(prompt)

    # Parse the scores from the LLM's response
    scores = {
        "fluency": parse_score(feedback, "Fluency"),
        "pronunciation": parse_score(feedback, "Pronunciation"),
        "grammar": parse_score(feedback, "Grammar"),
        "vocabulary": parse_score(feedback, "Vocabulary"),
    }

    if confidence < 0.8:
        scores["pronunciation"] = max(1, scores["pronunciation"] - 1)

    return feedback, scores


def parse_score(feedback, category):
    
    """
    Extract the score for a specific category from the LLM's feedback.
    """
    try:
        for line in feedback.splitlines():
            if line.lower().startswith(category.lower()):
                score = int(line.split(":")[1].strip())
                return score
    except (IndexError, ValueError):
        pass
    return 0  


def provide_detailed_feedback(response, confidence):
    """
    Provide detailed feedback and scores for the user's response.
    """
    feedback, scores = score_response(response, confidence)

    detailed_feedback = {
        "feedback": feedback,
        "scores": scores,
    }
    return detailed_feedback
