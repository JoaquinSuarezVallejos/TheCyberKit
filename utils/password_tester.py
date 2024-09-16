# PASSWORD TESTER (Python file)
# Case types used: snake_case (for functions and variables) and SCREAMING_SNAKE_CASE (for constants)

# Importing the necessary libraries and modules
# Using the zxcvbn library: https://github.com/dwolfhub/zxcvbn-python
from flask import jsonify, request
import zxcvbn


def evaluate_password():
    password = request.json["password"]

    if not password:  # Check for blank input
        return jsonify(
            {
                "score": "---",
                "crack_time_offline": "---",
                "crack_time_online_throttled": "---",
            }
        )

    try:
        result = zxcvbn.zxcvbn(password)

        score_number = result["score"]
        crack_time_offline = result["crack_times_display"][
            "offline_slow_hashing_1e4_per_second"
        ]  # Time to crack the password offline, slow hashing, 10000 guesses per second
        crack_time_online_throttled = result["crack_times_display"][
            "online_throttling_100_per_hour"
        ]  # Time to crack the password online, throttled, 100 guesses per hour

        score_mapping = {
            0: "1 (very unsafe)",
            1: "2 (weak)",
            2: "3 (okay)",
            3: "4 (good)",
            4: "5 (strong)",
        }
        strength_label = score_mapping[score_number]

        return jsonify(
            {  # Send the full label
                "score": strength_label,
                "crack_time_offline": crack_time_offline,
                "crack_time_online_throttled": crack_time_online_throttled,
            }
        )

    except IndexError:  # Still handle potential IndexErrors for other cases
        return jsonify(
            {
                "score": "Error",
                "crack_time_offline": "N/A",
                "crack_time_online_throttled": "N/A",
            }
        )
