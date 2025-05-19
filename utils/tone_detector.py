def detect_tone(message):
    message = message.lower()
    flirt_keywords = ["tu veux", "envie", "chaud", "viens", "séduire", "craquer"]
    humour_keywords = ["haha", "lol", "mdr", "blague", "rigolo"]
    irony_keywords = ["ah bon", "ok...", "super...", "bravo", "merci hein"]

    if any(k in message for k in flirt_keywords):
        return "flirt"
    elif any(k in message for k in humour_keywords):
        return "humour"
    elif any(k in message for k in irony_keywords):
        return "ironie"
    else:
        return "neutre"