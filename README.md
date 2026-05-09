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
| 0.4.0 | 2026-05-09 | Phase 3: Intake Pipeline Complete (DB Migration, Scraper, Background Processing) |

## What's Next (Phase 4: PWA Capture & Frontend Wiring)
With the backend enrichment pipeline complete, my immediate next steps are:
1. **PWA Web Share Target:** Configuring `manifest.json` so the app appears in the mobile share sheet.
2. **Capture Page:** Building `frontend/app/capture/page.tsx` to handle incoming shared content.
3. **Frontend Integration:** Connecting the TanStack Query hooks to the live `/api/items/` endpoint to display enriched data.
