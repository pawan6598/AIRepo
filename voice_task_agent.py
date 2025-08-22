import json
import datetime
import threading
import time
import re
from pathlib import Path

try:
    import speech_recognition as sr
    import pyttsx3
except ImportError:
    sr = None
    pyttsx3 = None

TASKS_FILE = Path("tasks.json")


class VoiceTaskAgent:
    """Simple voice agent that stores notes and reminders."""

    def __init__(self) -> None:
        if sr is None or pyttsx3 is None:
            raise RuntimeError(
                "Required libraries not installed. Please install 'SpeechRecognition' and 'pyttsx3'."
            )
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.tasks = self.load_tasks()
        # Start reminder loop in background
        reminder_thread = threading.Thread(target=self.reminder_loop, daemon=True)
        reminder_thread.start()

    def speak(self, text: str) -> None:
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self) -> str | None:
        with sr.Microphone() as source:
            audio = self.recognizer.listen(source)
        try:
            return self.recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            self.speak("Sorry, I didn't catch that.")
        except sr.RequestError:
            self.speak("Speech service is unavailable.")
        return None

    def load_tasks(self) -> list:
        if TASKS_FILE.exists():
            with TASKS_FILE.open("r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_tasks(self) -> None:
        with TASKS_FILE.open("w", encoding="utf-8") as f:
            json.dump(self.tasks, f, indent=2)

    def add_task(self, description: str, remind_at: datetime.datetime | None = None) -> None:
        task = {"description": description}
        if remind_at:
            task["remind_at"] = remind_at.isoformat()
        self.tasks.append(task)
        self.save_tasks()
        self.speak(f"Noted: {description}")

    def reminder_loop(self) -> None:
        while True:
            now = datetime.datetime.now()
            updated = False
            for task in self.tasks:
                remind_at = task.get("remind_at")
                if remind_at and not task.get("notified"):
                    reminder_time = datetime.datetime.fromisoformat(remind_at)
                    if reminder_time <= now:
                        self.speak(f"Reminder: {task['description']}")
                        task["notified"] = True
                        updated = True
            if updated:
                self.save_tasks()
            time.sleep(30)

    def run(self) -> None:
        self.speak(
            "Ready. Say 'note' to store a task, 'remind me to ... in ... minutes', or 'quit' to exit."
        )
        while True:
            command = self.listen()
            if not command:
                continue
            text = command.lower()
            if "quit" in text:
                self.speak("Goodbye!")
                break
            match = re.match(r"remind me to (.+) in (\d+) minutes", text)
            if match:
                description, minutes = match.groups()
                remind_at = datetime.datetime.now() + datetime.timedelta(minutes=int(minutes))
                self.add_task(description, remind_at)
                continue
            if "note" in text:
                self.speak("What should I note?")
                note = self.listen()
                if note:
                    self.add_task(note)
                continue
            self.speak("Sorry, I did not understand.")


if __name__ == "__main__":
    agent = VoiceTaskAgent()
    agent.run()
