# PASSWORD TESTER (Python file)
# Case types used: snake_case (for functions and variables)
# and SCREAMING_SNAKE_CASE (for constants)

# Importing the necessary libraries and modules
# Using the zxcvbn library: https://github.com/dwolfhub/zxcvbn-python
from flask import jsonify, request
import zxcvbn


# Evaluating the password strength
def evaluate_password():

    # Extracting the password from the JSON data sent by the front-end
    password = request.json["password"]

    # If the password is empty or null, return default values
    if not password:
        return jsonify(
            {
                "score": "---",
                "crack_time_offline": "---",
                "crack_time_online_throttled": "---",
            }
        )

    try:
        # Using the zxcvbn library to evaluate the password
        result = zxcvbn.zxcvbn(password)

        # Extracting the score, offline crack time, and online crack time
        score_number = result["score"]
        crack_time_offline = result["crack_times_display"][
            "offline_slow_hashing_1e4_per_second"
        ]  # Time to crack the password offline,
        # slow hashing, 10000 guesses per second
        crack_time_online_throttled = result["crack_times_display"][
            "online_throttling_100_per_hour"
        ]  # Time to crack the password online,
        # throttled, 100 guesses per hour

        # Mapping the score to a human-readable strength label
        score_mapping = {
            0: "1 (very unsafe)",
            1: "2 (weak)",
            2: "3 (okay)",
            3: "4 (good)",
            4: "5 (strong)",
        }
        # Get the strength label based on the score
        # (e.g., 0 -> "1 (very unsafe)")
        strength_label = score_mapping[score_number]

        return jsonify(
            {  # Returning the password evaluation results as JSON
                "score": strength_label,
                "crack_time_offline": crack_time_offline,
                "crack_time_online_throttled": crack_time_online_throttled,
            }
        )

    except (KeyError, TypeError):
        return jsonify(
            {  # Return an error message if the password evaluation fails
                "score": "Error",
                "crack_time_offline": "N/A",
                "crack_time_online_throttled": "N/A",
            }
        )
