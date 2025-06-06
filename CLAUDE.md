# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a monorepo containing a full-stack AI-powered advertising copy generation service with two main applications:

- **`apps/api-ad-generator/`** - FastAPI backend using Claude API for AI-generated content
- **`apps/web-console/`** - Next.js frontend with shadcn/ui components
- **`libs/`** - Shared libraries and utilities

## Development Commands

### Backend (api-ad-generator)
```bash
# Setup and dependencies
uv sync

# Development server
uv run uvicorn app.main:app --reload

# Testing
uv run --frozen pytest
```

### Frontend (web-console)
```bash
# Setup and dependencies  
npm install

# Development server (http://localhost:3000)
npm run dev

# Testing
npm run test        # Unit tests
npm run e2e         # End-to-end tests
```

## Architecture

### Backend Architecture
- **Clean Architecture + Domain-Driven Design** with strict layer separation
- **Domain Layer**: `app/domain/` - Business entities and rules
- **Application Layer**: `app/application/` - Use cases and orchestration  
- **Infrastructure Layer**: `app/infrastructure/` - FastAPI routes and external APIs
- **Stateless service** - No database, focuses on AI content generation

### Frontend Architecture
- **Next.js App Router** with server/client component pattern
- **Component Structure**: 
  - `components/ui/` - shadcn/ui base components
  - `components/common/` - Reusable application components
  - `components/specific/` - Feature-specific components
- **API Integration**: Centralized client in `lib/` directory

## Environment Setup

### Required Environment Variables
- **Backend**: `ANTHROPIC_API_KEY` - Claude API access key
- **Frontend**: `NEXT_PUBLIC_API_BASE_URL` - Backend API endpoint

## Code Standards

### Backend
- **Type hints are mandatory** for all functions and classes
- **Follow Clean Architecture patterns** - no domain logic in infrastructure layer
- **Use uv** for all Python package management (never pip/poetry)

### Frontend  
- **Full TypeScript** - no JavaScript files
- **Use shadcn/ui components** instead of custom styling where possible
- **Server components by default** - only use client components when necessary
- **Use npm** for package management (never yarn/pnpm)

## API Documentation

The OpenAPI specification is in `docs/openapi.yaml` and defines the complete API contract between frontend and backend.