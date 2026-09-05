import os, random, time
from datetime import timedelta
from functools import wraps
from flask import Flask, jsonify, render_template, request, session

app = Flask(__name__) 
app.config.update(SECRET_KEY=os.getenv("SECRET_KEY", "local-dev-key-change-before-deploy"), PERMANENT_SESSION_LIFETIME=timedelta(hours=4))

COLORS = ("#f7a8b8", "#a9d6ca", "#b9b7ef", "#f5c889", "#a9c6ea", "#e6b6d4")
EMOJIS = ("✦", "⚗", "π", "⌛", "☀", "✿")
GIFTS = ("The Golden Quill", "The Curiosity Jar", "The Puzzle Compass", "The Timekeeper's Medal", "The Kindness Lantern", "The Sparkle Badge")
TEACHERS = {f"Teacher {number}": {"pin": str(1000 + number), "subject": "Teacher's Day", "emoji": EMOJIS[(number - 1) % 6], "color": COLORS[(number - 1) % 6], "gift": GIFTS[(number - 1) % 6], "line": "For making every school day brighter."} for number in range(1, 35)}
NOTES = {teacher: [("Student 1", "Thank you for believing in us every day."), ("Student 2", "Your patience makes learning feel possible."), ("Student 3", "Thank you for turning lessons into lovely memories."), ("Student 4", "We are grateful for every little encouragement.")] for teacher in TEACHERS}

# Personalised Teacher's Day space — edit this section whenever you add another individual gift.
TEACHERS["Mudita Ma'am"] = TEACHERS.pop("Teacher 1") | {
    "gift": "A Little Book of Gratitude",
    "line": "With warmth and appreciation, from Anas.",
}
NOTES["Mudita Ma'am"] = [(
    "Anas",
    "Dear Mudita Ma'am, thank you for being far more than a teacher — for bringing patience to every question, kindness to every ordinary day, and confidence to moments when I needed it most. The lessons you give do not end with a bell; they stay with me as courage, curiosity, and the wish to do better. I hope this small gift reminds you of the enormous difference your warmth and guidance make. Happy Teacher's Day, Ma'am — with heartfelt gratitude, Anas.",
)]
NOTES.pop("Teacher 1", None)

TEACHERS["Hari Krishnan Sir"] = TEACHERS.pop("Teacher 2") | {
    "pin": "1002", "subject": "Academic Writing", "emoji": "✒", "gift": "The Red-Pen Survival Kit",
    "line": "For teaching us that a comma can be a matter of academic survival.",
}
NOTES["Hari Krishnan Sir"] = [(
    "Anas",
    "Dear Hari Krishnan Sir, thank you for teaching us that academic writing is not simply putting big words into a paragraph and hoping they sound intelligent — although we have all bravely attempted that strategy. You showed us how to turn scattered thoughts into clear arguments, how to respect a citation, and how one carefully placed comma can save an entire sentence from disaster. Thank you for making us better writers, sharper thinkers, and slightly more suspicious of the word 'very'. Happy Teacher's Day, Sir — with sincere gratitude and a carefully proofread thank-you from Anas.",
)]
NOTES.pop("Teacher 2", None)

TEACHERS["Shilpa Srivastava Ma'am"] = TEACHERS.pop("Teacher 3") | {
    "pin": "0101", "subject": "DCF", "emoji": "✦", "gift": "The Creative Spark Trophy",
    "line": "For turning every brief into a bright new possibility.",
}
NOTES["Shilpa Srivastava Ma'am"] = [(
    "Anas",
    "Dear Shilpa Srivastava Ma'am, thank you for making DCF feel like a place where ideas are allowed to be bold, colourful, and occasionally created five minutes before the deadline. You taught us to look beyond the obvious, trust the process, and remember that the first draft is not a final verdict — it is simply the brave beginning of something better. Thank you for bringing creativity, energy, and just the right amount of productive chaos into every class. Happy Teacher's Day, Ma'am — with lots of gratitude and imagination from Anas.",
)]
NOTES.pop("Teacher 3", None)

TEACHERS["Vandna Kansal Ma'am"] = TEACHERS.pop("Teacher 4") | {
    "pin": "1004", "subject": "Webstack", "emoji": "</>", "gift": "The Debugging Hero Badge",
    "line": "For proving that every bug has a solution — eventually.",
}
NOTES["Vandna Kansal Ma'am"] = [(
    "Anas",
    "Dear Vandna Kansal Ma'am, thank you for guiding us through Webstack, where one missing semicolon can somehow become a full-time emotional experience. You made HTML, CSS, JavaScript, and the mysterious world behind a working website feel less like magic and more like a challenge we could actually solve. Thank you for your patience when our layouts moved unexpectedly, our code refused to cooperate, and we insisted that it worked perfectly on our screen. Happy Teacher's Day, Ma'am — with appreciation, fewer console errors, and a grateful thank-you from Anas.",
)]
NOTES.pop("Teacher 4", None)

TEACHERS["Bosco Paul Alapatt Sir"] = TEACHERS.pop("Teacher 5") | {"pin": "1005", "subject": "School of Sciences · Associate Dean", "emoji": "★", "gift": "The Steady Compass", "line": "For leading with understanding and unwavering support."}
NOTES["Bosco Paul Alapatt Sir"] = [("Anas", "Dear Bosco Paul Alapatt Sir, thank you for being one of the most supportive and understanding people I have met in college. As the HOD of the School of Sciences and Associate Dean, you carry many responsibilities, yet you still make people feel heard, encouraged, and capable. Your guidance gives students the confidence to move forward even when things feel uncertain. Thank you for leading with both wisdom and kindness. Happy Teacher's Day, Sir — with deep respect and gratitude from Anas.")]
NOTES.pop("Teacher 5", None)
TEACHERS["Ranjeeta Ma'am"] = TEACHERS.pop("Teacher 6") | {"pin": "1006", "subject": "TCLS", "emoji": "✿", "gift": "The Future-Ready Notebook", "line": "For teaching lessons that reach far beyond the classroom."}
NOTES["Ranjeeta Ma'am"] = [("Anas", "Dear Ranjeeta Ma'am, thank you for making TCLS feel like a guide for real life rather than just another subject to complete. You teach us the things we genuinely need for a better future — how to think clearly, grow responsibly, and face every field of life with confidence. Your lessons have a way of staying useful long after the class is over, which is probably the best kind of teaching. Happy Teacher's Day, Ma'am — with sincere appreciation from Anas.")]
NOTES.pop("Teacher 6", None)
TEACHERS["Dr Glory Ma'am"] = TEACHERS.pop("Teacher 7") | {"pin": "1007", "subject": "Mentorship", "emoji": "♥", "gift": "The Mentor's Lantern", "line": "For being a steady light whenever students need direction."}
NOTES["Dr Glory Ma'am"] = [("Anas", "Dear Dr Glory Ma'am, thank you for being such a supportive mentor and one of the kindest people in our college journey. Your encouragement makes difficult moments feel manageable, and your guidance helps students see possibilities in themselves that they may not have noticed yet. You support us not only in our work, but also in becoming more confident people. Happy Teacher's Day, Ma'am — with heartfelt gratitude from Anas.")]
NOTES.pop("Teacher 7", None)
TEACHERS["Lawrence Kujur Sir"] = TEACHERS.pop("Teacher 8") | {"pin": "1008", "subject": "HED", "emoji": "☀", "gift": "The Alumni Inspiration Badge", "line": "For showing us that a Christ journey can come full circle."}
NOTES["Lawrence Kujur Sir"] = [("Anas", "Dear Lawrence Kujur Sir, thank you for making HED engaging, thoughtful, and connected to the values that matter outside a classroom too. It is inspiring to learn from a Christ alumnus who has returned to guide the next generation. Your journey reminds us that our time here can become the beginning of something meaningful, not just a collection of attendance marks and deadlines. Happy Teacher's Day, Sir — with respect and gratitude from Anas.")]
NOTES.pop("Teacher 8", None)
TEACHERS["Yash Thakur Sir"] = TEACHERS.pop("Teacher 9") | {"pin": "1009", "subject": "AI · Python · Eulim Science Club", "emoji": "⚙", "gift": "The Code Explorer Medal", "line": "For making technology, curiosity, and community go together."}
NOTES["Yash Thakur Sir"] = [("Anas", "Dear Yash Thakur Sir, thank you for making AI and Python feel exciting instead of intimidating — even when the code has other plans and produces errors with great confidence. As our teacher, Eulim Science Club mentor, and a Christ alumnus, you show us how curiosity can grow into real skill and community. Your support encourages us to explore, build, and keep trying until the program finally runs. Happy Teacher's Day, Sir — with gratitude, curiosity, and hopefully fewer bugs from Anas.")]
NOTES.pop("Teacher 9", None)

TEACHERS["Abhinav Sir"] = TEACHERS.pop("Teacher 10") | {"pin": "1010", "subject": "Mathematics", "emoji": "π", "gift": "The Calm Problem-Solver Award", "line": "For making every difficult problem feel possible."}
NOTES["Abhinav Sir"] = [("Anas", "Dear Abhinav Sir, thank you for being such a talented, understanding, and calm teacher. You have a wonderful way of making mathematics feel less like a maze of numbers and more like a puzzle that can be solved one patient step at a time. Your calm guidance makes even the toughest questions feel manageable, and your encouragement gives students the confidence to keep trying. Happy Teacher's Day, Sir — with sincere gratitude from Anas.")]
NOTES.pop("Teacher 10", None)

# School of Sciences faculty list. Add subject-specific notes later by replacing an entry in NOTES.
SCHOOL_OF_SCIENCES_FACULTY = [
    "Vaibhav Sir", "Aparna Ma'am", "Lata Ma'am", "Swati Ma'am", "Kuljeet Sir", "Garima Ma'am", "Rajesh Sir", "Akshita Ma'am",
    "Manjula Ma'am", "Vidushi Ma'am", "Jaspreet Sir", "Neelam Ma'am", "Meghavi Ma'am", "Ramesh Sir", "Madan Sir", "Indu Ma'am",
    "Purnima Ma'am", "Neha Ma'am", "Jayalakshmi Ma'am", "Ashish Sir", "Sanjeev Sir", "Vandana Ma'am", "Varuna Ma'am", "Kamal Sir",
    "Amrit Ma'am", "Preety Ma'am",
]
for number, name in enumerate(SCHOOL_OF_SCIENCES_FACULTY, start=11):
    source = f"Teacher {number}"
    base = TEACHERS.pop(source, {"subject": "School of Sciences", "emoji": "✦", "color": COLORS[(number - 1) % 6], "gift": "The Gratitude Star", "line": "For making learning brighter every day."})
    TEACHERS[name] = base | {"pin": str(1000 + number), "subject": "School of Sciences", "gift": "The Gratitude Star", "line": "For helping students learn, grow, and believe in themselves."}
    NOTES[name] = [("Anas", f"Dear {name}, thank you for the dedication, patience, and encouragement you bring to students every day. Your guidance makes the School of Sciences a more thoughtful and inspiring place to learn, and the impact of your work reaches far beyond a single classroom. Happy Teacher's Day — with sincere gratitude and warm wishes from Anas.")]
    NOTES.pop(source, None)

def current_teacher(): return session.get("teacher")
def protected(fn):
    @wraps(fn)
    def inner(*args, **kwargs):
        if not current_teacher(): return jsonify(error="Please unlock your memory space."), 401
        return fn(*args, **kwargs)
    return inner

@app.get("/")
def home():
    teacher = current_teacher()
    return render_template("index.html", teacher=teacher, data=TEACHERS[teacher]) if teacher else render_template("login.html")

@app.post("/api/login")
def login():
    now, attempts, locked_until = time.time(), session.get("attempts", 0), session.get("locked_until", 0)
    if now < locked_until: return jsonify(error="Please wait one minute before trying again."), 429
    pin = str((request.get_json(silent=True) or {}).get("pin", ""))
    teacher = next((name for name, data in TEACHERS.items() if data["pin"] == pin), None)
    if not teacher:
        attempts += 1; session["attempts"] = attempts
        if attempts >= 5: session["locked_until"] = now + 60; session["attempts"] = 0
        return jsonify(error="That key does not match a memory space."), 401
    session.clear(); session["teacher"] = teacher; session.permanent = True
    return jsonify(ok=True)

@app.post("/api/logout")
def logout(): session.clear(); return jsonify(ok=True)

@app.post("/api/message")
@protected
def message():
    teacher, seen = current_teacher(), session.setdefault("seen", {})
    used = seen.get(teacher, []); available = [i for i in range(len(NOTES[teacher])) if i not in used]
    if not available: used, available = [], list(range(len(NOTES[teacher])))
    picked = random.choice(available); used.append(picked); seen[teacher] = used; session["seen"] = seen
    student, text = NOTES[teacher][picked]
    return jsonify(student=student, text=text, remaining=len(NOTES[teacher]) - len(used), total=len(NOTES[teacher]))

@app.post("/api/reset")
@protected
def reset():
    session.setdefault("seen", {}).pop(current_teacher(), None); session.modified = True
    return jsonify(ok=True)

if __name__ == "__main__": app.run(debug=True)
