import json
import datetime
import threading
import time
import re
import os
from pathlib import Path
import websocket

class AzureRealtimeClient:
    """Client for Azure OpenAI realtime responses."""

    def __init__(self) -> None:
        endpoint = os.environ.get("AZURE_OPENAI_REALTIME_ENDPOINT")
        deployment = os.environ.get("AZURE_OPENAI_REALTIME_DEPLOYMENT")
        key = os.environ.get("AZURE_OPENAI_API_KEY")
        if not all([endpoint, deployment, key]):
            raise RuntimeError("Missing Azure realtime environment variables")
        url = f"{endpoint}?deployment={deployment}&api-version=2024-07-15-preview"
        headers = [
            f"Authorization: Bearer {key}",
            "OpenAI-Beta: realtime=v1",
        ]
        self.ws = websocket.create_connection(url, header=headers)

    def ask(self, text: str) -> str:
        """Send text and return model response."""
        self.ws.send(json.dumps({"type": "input_text", "text": text}))
        self.ws.send(json.dumps({"type": "response.create"}))
        chunks: list[str] = []
        while True:
            message = json.loads(self.ws.recv())
            mtype = message.get("type")
            if mtype == "response.output_text.delta":
                chunks.append(message.get("delta", ""))
            elif mtype == "response.completed":
                break
        return "".join(chunks)

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
        self.ai_client = AzureRealtimeClient()
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

    def chat(self, prompt: str) -> str | None:
        """Get a conversational response from Azure OpenAI."""
        try:
            return self.ai_client.ask(prompt)
        except Exception:
            return None

    def add_task(self, description: str, remind_at: datetime.datetime | None = None) -> None:
        task = {"description": description}
        if remind_at:
            task["remind_at"] = remind_at.isoformat()
        self.tasks.append(task)
        self.save_tasks()
        confirmation = self.chat(f"Confirm to the user that '{description}' has been noted.")
        self.speak(confirmation if confirmation else f"Noted: {description}")

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
                farewell = self.chat("Say goodbye to the user")
                self.speak(farewell if farewell else "Goodbye!")
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
            reply = self.chat(text)
            if reply:
                self.speak(reply)
            else:
                self.speak("Sorry, I did not understand.")


if __name__ == "__main__":
    agent = VoiceTaskAgent()
    agent.run()
