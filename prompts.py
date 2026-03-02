def system_prompt(history):
    return [
        {"role": "system", "content": "You are an intelligent hiring assistant for a tech recruitment company. Stay within hiring context only."}
    ] + history

def info_collection_prompt(user_message):
    return [
        {"role": "system", "content": "Extract or request candidate information. Format clearly as:\nFull Name:\nEmail:\nPhone:\nYears of Experience:\nDesired Position:\nLocation:\nTech Stack:"},
        {"role": "user", "content": user_message}
    ]

def tech_question_prompt(tech_stack):
    return [
        {"role": "system", "content": "Generate 3-5 technical interview questions for each technology mentioned. Keep difficulty moderate to advanced."},
        {"role": "user", "content": f"Tech Stack: {tech_stack}"}
    ]

def closing_prompt():
    return "Thank you for your time. Our recruitment team will review your responses and contact you regarding next steps. Have a great day."
