import time
from speech_to_text.transcription import transcribe_streaming
from scoring.scoring import provide_detailed_feedback
from feedback.feedback import generate_pdf_report
from llm.conversation import get_ielts_examiner_response
from llm.questions import (
    part1_introduction,
    part2_cue_card,
    practice_questions,
)


def display_header(title):
    """
    Displays a formatted header with the given title.

    Args:
        title (str): The title to display.
    """
    print("=" * 50)
    print(f"{title.center(50)}")
    print("=" * 50)


def split_text(text, words_per_line=10):
    """
    Splits a given text into lines, each containing a specified number of words.

    Args:
        text (str): The text to split.
        words_per_line (int): Number of words per line.

    Returns:
        str: The text split into lines.
    """
    words = text.split()
    lines = [
        " ".join(words[i : i + words_per_line])
        for i in range(0, len(words), words_per_line)
    ]
    return "\n".join(lines)


def start_conversation():
    """
    Initiates the IELTS speaking test simulation.
    Allows the user to choose between practice and test modes.
    """
    display_header("IELTS Speaking Test Simulation")

    mode = input("Choose mode: Practice (P) or Test (T): ").strip().upper()

    if mode == "P":
        practice_mode()
    elif mode == "T":
        test_mode()
    else:
        print("Invalid mode selected. Please restart and choose a valid mode.")


def practice_mode():
    """
    Handles the practice mode of the IELTS speaking test simulation.
    The user answers practice questions and receives feedback.
    """
    display_header("Practice Mode")
    questions = practice_questions()

    for question in questions:
        print(f"Question: {question}\n")
        input("Press Enter when you are ready to start speaking...")

        transcript, confidence = transcribe_streaming()
        if not transcript:
            print("No speech detected. Please try again.\n")
            continue

        print(f"You said: {transcript}\n")
        prompt = (
            f"I am an IELTS examiner. Evaluate the following response in detail:\n\n"
            f"Response: {transcript}\n\n"
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
        response = get_ielts_examiner_response(prompt)
        print(f"Examiner Feedback: {response}\n")

        if input("Do you want to continue? (y/n): ").lower() != "y":
            print("Exiting Practice Mode.\n")
            break


def test_mode():
    """
    Handles the test mode of the IELTS speaking test simulation.
    Guides the user through all three parts of the IELTS speaking test and provides feedback.
    """
    display_header("Test Mode")
    print("You will go through all three parts of the IELTS Speaking Test.\n")

    part1_responses = part1()
    part2_response = part2()
    part3_responses = part3()

    provide_feedback(part1_responses, part2_response, part3_responses)


def part1():
    """
    Conducts Part 1 (Introduction) of the IELTS Speaking Test.

    Returns:
        list: A list of tuples containing user responses and confidence scores.
    """
    display_header("Part 1: Introduction")
    responses = []

    for question in part1_introduction():
        print(f"Question: {split_text(question)}\n")

        transcript, confidence = transcribe_streaming()
        if transcript:
            responses.append((transcript, confidence))
            print(f"You said: {split_text(transcript)}\n")
        else:
            print("No speech detected. Please try again.\n")
        time.sleep(2)

    return responses


def part2():
    """
    Conducts Part 2 (Long Turn/Cue Card Activity) of the IELTS Speaking Test.

    Returns:
        tuple: A tuple containing the user response and confidence score.
    """
    display_header("Part 2: Long Turn (Cue Card Activity)")
    cue_card = part2_cue_card()

    print(f"Topic: {split_text(cue_card['topic'])}\n")
    print("You should talk about:")
    for point in cue_card["points"]:
        print(f"- {split_text(point)}")

    print("\nYou have 1 minute to prepare.")
    input("Press Enter when you are ready to start speaking...")

    transcript, confidence = transcribe_streaming()
    print(f"You said: {split_text(transcript)}\n")
    time.sleep(2)

    return transcript, confidence


def part3():
    """
    Conducts Part 3 (Two-Way Discussion) of the IELTS Speaking Test.

    Returns:
        list: A list of tuples containing user responses and confidence scores.
    """
    display_header("Part 3: Two-Way Discussion")
    responses = []
    question_count = 0 

    print("This section involves a two-way discussion.\n")

    while question_count < 2:  
        if question_count == 0:
            prompt = "I am an IELTS examiner. Ask a question about why exercise is important."
        else:
            prompt = "I am an IELTS examiner. Ask a follow-up question about staying healthy."

        response = get_ielts_examiner_response(prompt)
        print(f"Examiner: {split_text(response)}\n")

        transcript, confidence = transcribe_streaming()
        print(f"You said: {split_text(transcript)}")
        responses.append((transcript, confidence))

        question_count += 1
        time.sleep(2)

    print("You have completed the test. Thank you for taking the test!\n")
    return responses


def provide_feedback(part1_responses, part2_response, part3_responses):
    """
    Provides detailed feedback for all parts of the IELTS Speaking Test.

    Args:
        part1_responses (list): Responses from Part 1.
        part2_response (tuple): Response and confidence score from Part 2.
        part3_responses (list): Responses from Part 3.
    """

    # Part 1:  Introduction
    display_header("Introduction Feedback")
    part1_feedback = ""
    for response, confidence in part1_responses:
        detailed_feedback = provide_detailed_feedback(response, confidence)
        feedback_text = f"Part 1 Feedback: {detailed_feedback['feedback']}\nScores: {detailed_feedback['scores']}\n\n"
        part1_feedback += feedback_text
        print(feedback_text)

    # Part 2: Long Turn
    display_header("Long Turn Feedback")
    detailed_feedback = provide_detailed_feedback(part2_response[0], part2_response[1])
    part2_feedback = f"Part 2 Feedback: {detailed_feedback['feedback']}\nScores: {detailed_feedback['scores']}\n\n"
    print(part2_feedback)

    # Part 3: Two-Way Discussion
    display_header("Two-Way Discussion Feedback")
    part3_feedback = ""
    for response, confidence in part3_responses:
        detailed_feedback = provide_detailed_feedback(response, confidence)
        feedback_text = f"Part 3 Feedback: {detailed_feedback['feedback']}\nScores: {detailed_feedback['scores']}\n\n"
        part3_feedback += feedback_text
        print(feedback_text)

    generate_pdf_report(part1_feedback, part2_feedback, part3_feedback)


if __name__ == "__main__":
    start_conversation()
