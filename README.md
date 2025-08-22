# AIRepo

This repository contains a simple voice-based task agent.

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the agent:

```bash
python voice_task_agent.py
```

Speak commands such as:

- "note" — the agent records the next sentence as a task.
- "remind me to <task> in <minutes> minutes" — schedules a reminder.
- "quit" — exits the agent.

Tasks are stored in `tasks.json`.

