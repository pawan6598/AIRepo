# AIRepo

This repository contains a voice-based task agent that uses the Microsoft Azure OpenAI realtime model for conversational responses.

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

Configure environment variables so the agent can access the Azure OpenAI realtime endpoint:

```bash
export AZURE_OPENAI_REALTIME_ENDPOINT="wss://<your-resource>.openai.azure.com/openai/realtime"
export AZURE_OPENAI_REALTIME_DEPLOYMENT="<model-deployment-name>"
export AZURE_OPENAI_API_KEY="<your-azure-openai-key>"
```

Speak commands such as:

- "note" — the agent records the next sentence as a task.
- "remind me to <task> in <minutes> minutes" — schedules a reminder.
- "quit" — exits the agent.

Tasks are stored in `tasks.json`.

The tasks file is generated at runtime and ignored by git.

