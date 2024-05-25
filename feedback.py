import json
import os

def store_feedback(question, answer, feedback):
    # Check if the feedback file exists, if not create it
    feedback_file = "feedback.json"
    if not os.path.exists(feedback_file):
        with open(feedback_file, "w") as f:
            json.dump([], f)

    # Load the existing feedback data
    with open(feedback_file, "r") as f:
        feedback_data = json.load(f)

    # Add the new feedback to the data
    feedback_data.append({"question": question, "answer": answer, "feedback": feedback})

    # Save the updated feedback data
    with open(feedback_file, "w") as f:
        json.dump(feedback_data, f, indent=2)

    return "Thank you for your feedback!"