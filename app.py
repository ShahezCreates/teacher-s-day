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

ADDITIONAL_TEACHERS = {
    "Gautam Sir": ("1037", "Computer Science", "The Guru's Guidance Scroll", "For guidance that has stayed with us far beyond the classroom.", "Dear Gautam Sir, on this Teachers’ Day, I want to thank you for being much more than just a teacher to me. You taught me Computer Science in classes 6th and 7th, but even after that, you have continued to guide and help me whenever I needed it. You have always been there for every little doubt, problem, or situation — not just as a teacher, but truly as a Guru. What makes our bond even more special is that you have stayed connected with our family over the years and have always treated us with the same warmth and care. You have guided not only me but also my family whenever we needed your advice, and I am genuinely grateful to have someone like you in our lives. Thank you for always being there, for believing in us, guiding us, and being a part of our journey. Happy Teachers’ Day, Sir ji! 🌸🙏🏻"),
    "Neetu Ma'am": ("1038", "EVS", "The Green Guide Badge", "For making learning clear, comfortable, and engaging.", "Dear Neetu Ma'am, thank you for being such a kind and approachable teacher. The way you explain EVS so clearly and make every class engaging helps students learn with ease and confidence. Your supportive and pleasant nature makes the classroom feel comfortable, enjoyable, and welcoming. Happy Teacher's Day, Ma'am — with warm gratitude from Anas."),
    "Bholey Singh Sir": ("1039", "Physical Chemistry", "The Concept Catalyst Award", "For making difficult concepts feel wonderfully clear.", "Dear Bholey Singh Sir, thank you for explaining Physical Chemistry concepts with such clarity and patience. Your supportive nature and readiness to help whenever students face difficulties make you a wonderful teacher and mentor. You make a subject full of equations and concepts feel far more approachable. Happy Teacher's Day, Sir — with sincere appreciation from Anas."),
    "Tanushree Ma'am": ("1040", "Zoology", "The Living World Medal", "For making every concept easier to understand and remember.", "Dear Tanushree Ma'am, thank you for being one of the warmest, most caring, and dedicated teachers we have had in college. Your clear and effective way of teaching Zoology helped students understand concepts even when they began with very little prior knowledge. Your experience, patience, and genuine care for students are deeply respected and appreciated. Happy Teacher's Day, Ma'am — with heartfelt gratitude from Anas."),
    "Sweta Ma'am": ("1041", "Microbiology", "The Growth Mindset Star", "For discipline that helps students become their best.", "Dear Sweta Ma'am, thank you for being a disciplined and constructive teacher who genuinely cares about every student's learning and progress. Your high standards encourage us to work harder, while your support reminds us that those standards come from a place of care. Your effective teaching has made you one of the best teachers we have had. Happy Teacher's Day, Ma'am — with respect and gratitude from Anas."),
    "Manisha Ma'am": ("1042", "Botany", "The Blooming Knowledge Pin", "For helping every topic take root and grow clearly.", "Dear Manisha Ma'am, thank you for your dedication and for explaining Botany in such a clear and structured way. Your teaching helps students understand topics effectively and build a stronger connection with the subject. We appreciate the care and effort you bring into every class. Happy Teacher's Day, Ma'am — with sincere gratitude from Anas."),
    "Sunil Sir": ("1043", "Biochemistry · Zoology", "The Learning Beyond Syllabus Award", "For teaching understanding, not only chapters.", "Dear Sunil Sir, thank you for focusing not only on completing the Biochemistry syllabus but also on helping students genuinely understand and enjoy the subject. Your clear explanations, valuable knowledge, and positive approachable nature make your classes meaningful and memorable. Happy Teacher's Day, Sir — with warm appreciation from Anas."),
    "Mukesh Sir": ("1044", "Biochemistry · Zoology", "The Precision Mentor Badge", "For discipline and concepts that stay with students.", "Dear Mukesh Sir, thank you for your strong command over Biochemistry and for explaining concepts so thoroughly. Your disciplined approach in the classroom helps students take their learning seriously and understand the subject with greater depth. Your teaching has made a real difference, and you are truly one of the best teachers we have had. Happy Teacher's Day, Sir — with respect and gratitude from Anas."),
}
for position, (name, (pin, subject, gift, line, note)) in enumerate(ADDITIONAL_TEACHERS.items()):
    TEACHERS[name] = {"pin": pin, "subject": subject, "emoji": EMOJIS[position % 6], "color": COLORS[position % 6], "gift": gift, "line": line}
    NOTES[name] = [("Anas", note)]

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
