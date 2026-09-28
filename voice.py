def listen():
    import speech_recognition as sr
    r = sr.Recognizer()
    with sr.Microphone() as src:
        audio = r.listen(src, timeout=5)
    return r.recognize_google(audio)


def reply(text):
    t = text.lower()
    if "hello" in t or "hi" in t.split():
        return "Hey, I'm here."
    if "time" in t:
        from datetime import datetime
        return datetime.now().strftime("It's %H:%M.")
    return f"You said: {text}"


def speak(text):
    try:
        import pyttsx3
        e = pyttsx3.init()
        e.say(text)
        e.runAndWait()
    except Exception:
        pass
