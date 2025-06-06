# AI-Powered Ad Copy Generator

**Note: This repository is used for testing git worktree functionality.**

**🤖 Built with Claude Code in ~2 hours for approximately $6**

![ai-ad-generator](https://github.com/user-attachments/assets/eb14eb9c-6035-4302-8684-45fa1543e24e)

## Project Overview

This is a full-stack AI-powered advertising copy generation service built as a monorepo. The system leverages Claude AI to generate high-quality advertisement copy based on user input and preferences.

### Applications

- **`apps/api-ad-generator/`** - FastAPI backend service using Claude API for AI content generation
- **`apps/web-console/`** - React frontend with shadcn/ui components for user interaction
- **`libs/`** - Shared libraries and utilities (future expansion)

## Architecture

### Backend (api-ad-generator)
- **Clean Architecture + Domain-Driven Design** with strict layer separation
- **Stateless service** - No database dependency, focuses on AI content generation
- **FastAPI** framework with automatic OpenAPI documentation
- **Python with uv** package management

### Frontend (web-console)
- **Vite + React** with TypeScript
- **shadcn/ui components** for consistent UI design
- **Tailwind CSS** for styling
- **npm** package management

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- uv (Python package manager)
- Anthropic API key

### Backend Setup
```bash
cd apps/api-ad-generator
uv sync
export ANTHROPIC_API_KEY="your_api_key_here"
uv run uvicorn app.main:app --reload
```

### Frontend Setup
```bash
cd apps/web-console
npm install
echo "NEXT_PUBLIC_API_BASE_URL=http://localhost:8000" > .env.local
npm run dev
```

## Environment Variables

### Backend
- `ANTHROPIC_API_KEY` - Required for Claude API access

### Frontend
- `NEXT_PUBLIC_API_BASE_URL` - Backend API endpoint (default: http://localhost:8000)

## Testing

### Backend
```bash
cd apps/api-ad-generator
uv run --frozen pytest
```

### Frontend
```bash
cd apps/web-console
npm run test        # Unit tests
npm run e2e         # End-to-end tests
```

## API Documentation

- Backend API docs: http://localhost:8000/docs (when running)
- OpenAPI specification: `docs/openapi.yaml`

## Development Guidelines

- **Backend**: Follow Clean Architecture patterns, use type hints, uv for package management
- **Frontend**: Full TypeScript, prefer shadcn/ui components, npm for package management
- **Code Quality**: Maintain test coverage, follow existing patterns, add documentation

## Project Structure

```
├── apps/
│   ├── api-ad-generator/     # FastAPI backend
│   └── web-console/          # React frontend
├── docs/
│   └── openapi.yaml          # API specification
├── libs/                     # Shared libraries
└── CLAUDE.md                 # AI assistant instructions
```
