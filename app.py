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
