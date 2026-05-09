# Nexus Vault (Local MVP)

A local-first content saving system. Save, organize, and access anything from your desktop or mobile device — privately, with no cloud dependency.

## Architecture
- **Backend:** FastAPI + PostgreSQL
- **Frontend:** Next.js (Desktop UI + Mobile PWA)
- **Database:** PostgreSQL via SQLAlchemy (async)

## Project Structure
```
Phone Connector/
├── backend/         # FastAPI application
├── frontend/        # Next.js application
├── docs/            # Technical docs
├── venv/            # Python virtual environment
├── context.md       # Session-by-session change log
├── README.md        # This file
└── requirements.txt # Python dependencies
```

## Version History
| Version | Date | Description |
|---------|------|-------------|
| 0.1.0 | 2026-05-05 | Phase 0: Project scaffolding and environment setup |
| 0.2.0 | 2026-05-06 | Phase 1: FastAPI Backend with PostgreSQL & Item CRUD |
| 0.3.0 | 2026-05-06 | Phase 2: UI System Complete & Pivot to MVP v2 |
| 0.3.1 | 2026-05-08 | Phase 3: Intake Pipeline Setup (Dependencies & Migration Prep) |

## Current Goals (MVP v2)
Nexus Vault is now focused on **Universal Share Capture**:
- **Capture:** Instant saving via Mobile Share Target (PWA) or desktop Quick-Save.
- **Enrich:** Automated metadata extraction (Scraper Service).
- **Vault:** A premium, exploratory interface for curated discoveries.

## Getting Started (Phase 3)
1. **Configure Environment:**
   - Copy `backend/.env.example` to `backend/.env`.
   - Update `DATABASE_URL` with your local PostgreSQL password.
2. **Reset Database (CRITICAL):**
   ```bash
   # From root
   python backend/scripts/reset_db.py
   ```
3. **Run Services:**
   - **Backend:** `cd backend && uvicorn app.main:app --reload`
   - **Frontend:** `cd frontend && npm run dev`

## Setup & Migration Notes
> [!IMPORTANT]
> The Phase 2 -> Phase 3 transition requires a full database reset to apply the new `raw_url` and `processing_status` columns. Run this BEFORE starting the server for the first time in Phase 3.
