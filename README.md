# Nexus Vault (Local MVP)

I am building a local-first content saving system called Nexus Vault. My goal is to create a tool to save, organize, and access anything from my desktop or mobile device — privately, with zero cloud dependency.

## My Tech Stack
- **Backend:** FastAPI + PostgreSQL
- **Frontend:** Next.js (Desktop UI + Mobile PWA)
- **Database:** PostgreSQL via SQLAlchemy (async)

## What I'm Currently Focused On (MVP v2)
I recently pivoted the project focus to **Universal Share Capture**:
- **Capture:** I'm building an instant saving mechanism via Mobile Share Target (PWA) or desktop Quick-Save.
- **Enrich:** I am developing a Backend Enrichment Service (Scraper) for automated metadata extraction.
- **Vault:** I am designing a premium, exploratory interface for curated discoveries.

## Version History
| Version | Date | Description |
|---------|------|-------------|
| 0.1.0 | 2026-05-05 | Phase 0: Project scaffolding and environment setup |
| 0.2.0 | 2026-05-06 | Phase 1: FastAPI Backend with PostgreSQL & Item CRUD |
| 0.3.0 | 2026-05-06 | Phase 2: UI System Complete & Pivot to MVP v2 |
| 0.3.1 | 2026-05-08 | Phase 3: Intake Pipeline Setup (Dependencies & Migration Prep) |

## What's Next (Phase 3)
Right now, I am working on the Intake Pipeline. My immediate next steps are:
1. **Fixing a Database Blocker:** Resolving a PostgreSQL password authentication error so I can run `python backend/scripts/reset_db.py` to reset the database schema.
2. **Scraper Development:** Building out `backend/app/services/scraper.py` using `httpx` and `BeautifulSoup4` to parse titles and metadata from saved URLs.
3. **PWA Integration:** Setting up the Web Share Target in the Next.js frontend to send URLs directly to the backend background processor.
