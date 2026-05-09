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
| 0.5.0 | 2026-05-09 | Phase 4: Frontend Integration Complete (Stitch MCP UI, PWA Web Share, TanStack Query) |

## What's Next (Phase 5: UX Polish & State Management)
With the frontend successfully capturing and displaying data from the live backend using the new Stitch MCP "Obsidian Glass" design system, the immediate next steps are:
1. **Search & Filtering:** Implement the logic in the dashboard to filter items by category and search by keyword.
2. **Real-time Status Updates:** Setup polling or WebSockets in the UI to seamlessly transition cards from "Processing" to "Complete" without a full page refresh.
3. **Detail View:** Build the `frontend/app/items/[id]/page.tsx` for viewing the full content of a saved item.
