# RAG Demo Project

End-to-end Retrieval-Augmented Generation system featuring a FastAPI backend and Next.js frontend.

## Folder Structure

```
backend/
  app/
    api/
    core/
    services/
    ...
  tests/
frontend/
  pages/
  components/
  state/
  ...
docs/
```

See [docs/architecture.md](docs/architecture.md) for the architecture diagram and [docs/implementation-plan.md](docs/implementation-plan.md) for milestones.

## Requirements

- Python 3.11+
- Node.js 18+

## Setup

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r ../requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```
