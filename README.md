# YU Trade

A verified campus marketplace for York University. Students and faculty can buy and sell items within a trusted community, restricted to `@my.yorku.ca` and `@yorku.ca` email addresses.

**Course:** EECS4314 — Winter 2026

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, FastAPI, SQLAlchemy, SQLite |
| Frontend | React, TypeScript, Axios |
| Auth | JWT (python-jose), bcrypt (passlib) |
| Image Storage | Local file system (`uploads/`) |

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm or yarn

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env        # Edit .env with your SECRET_KEY
uvicorn app.main:app --reload
```

The API will run at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

### Frontend Setup

The frontend needs to be scaffolded first (see F1.1 task below), then our stub files go into the generated `src/` folder.

```bash
# One-time setup (Mai's F1.1 task):
npx create-react-app frontend --template typescript
# Then move/merge our existing src/ stubs into the generated src/ directory

# After setup:
cd frontend
npm install axios react-router-dom
npm start
```

The app will run at `http://localhost:3000`.

### Running Tests

```bash
cd backend
pytest tests/
```

### Environment Variables

See `backend/.env.example`. Key settings:

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | JWT signing key | (must set) |
| `DATABASE_URL` | SQLAlchemy DB URL | `sqlite:///./yutrade.db` |
| `EMAIL_BACKEND` | `console` (dev) or `smtp` (prod) | `console` |

In dev mode (`EMAIL_BACKEND=console`), verification codes are printed to the backend terminal instead of emailed.

---

## Team Assignments

### Backend

#### Mickey (Michael Byalsky) — Database Layer

Responsible for all ORM models, database setup, and schema design.

| Phase | Task | File(s) |
|-------|------|---------|
| 1 | B1.1 — Project setup, `requirements.txt`, `main.py` | `app/main.py`, `requirements.txt`, `.env.example` |
| 1 | B1.2 — Config and database connection | `app/config.py`, `app/database.py` |
| 1 | B1.3 — User and VerificationCode models | `app/models/user.py`, `app/models/verification.py` |
| 1 | B1.9a — Test fixtures | `tests/conftest.py` |
| 2 | B2.1 — Listing and Image models | `app/models/listing.py`, `app/models/image.py` |
| 3 | B3.1 — Message model | `app/models/message.py` |

Also: `app/models/__init__.py` (import all models so `create_all()` works).

#### Daniel Chahine — Authentication

Responsible for auth endpoints, JWT, password hashing, email verification.

| Phase | Task | File(s) |
|-------|------|---------|
| 1 | B1.4 — Auth schemas | `app/schemas/auth.py`, `app/schemas/user.py` |
| 1 | B1.5 — Security utilities | `app/utils/security.py` |
| 1 | B1.6 — Dependencies | `app/dependencies.py` |
| 1 | B1.7 — Auth + email services | `app/services/auth_service.py`, `app/services/email_service.py` |
| 1 | B1.8 — Auth router | `app/routers/auth.py` |
| 1 | B1.9b — Auth tests | `tests/test_auth.py` |

#### Lakshan Kandeepan — Listings

Responsible for listing CRUD, image upload handling, search/filter.

| Phase | Task | File(s) |
|-------|------|---------|
| 2 | B2.2 — Listing schemas | `app/schemas/listing.py` |
| 2 | B2.3 — Listing service | `app/services/listing_service.py` |
| 2 | B2.4 — Image upload handling | (within `listing_service.py` and `routers/listings.py`) |
| 2 | B2.5 — Listings router | `app/routers/listings.py` |
| 2 | B2.6 — Listing tests | `tests/test_listings.py` |
| 3 | B3.5 — Search/filter on GET /listings | `app/routers/listings.py`, `app/services/listing_service.py` |

#### Raj (Rajendra Brahmbhatt) — Messaging

Responsible for messaging endpoints, thread logic, CI setup.

| Phase | Task | File(s) |
|-------|------|---------|
| 1 | B1.10 — GitHub Actions CI | `.github/workflows/ci.yml` |
| 3 | B3.2 — Message schemas | `app/schemas/message.py` |
| 3 | B3.3 — Message service | `app/services/message_service.py` |
| 3 | B3.4 — Messages router | `app/routers/messages.py` |
| 3 | B3.6 — Message tests | `tests/test_messages.py` |

---

### Frontend

#### Mai Komar — Pages and API Layer

| Phase | Task | File(s) |
|-------|------|---------|
| 1 | F1.1 — Scaffold React app | `package.json`, `tsconfig.json` (via create-react-app) |
| 1 | F1.2 — Axios client with JWT interceptor | `src/api/client.ts` |
| 1 | F1.5 — Auth pages | `src/pages/RegisterPage.tsx`, `src/pages/VerifyPage.tsx`, `src/pages/LoginPage.tsx` |
| 1 | F1.6 — Router setup | `src/App.tsx` |
| 1 | F1.8 — Auth API functions | `src/api/auth.ts` |
| 1 | — | `src/index.tsx` |
| 2 | F2.1 — Listings API functions | `src/api/listings.ts` |
| 2 | F2.4 — Listing detail page | `src/pages/ListingDetailPage.tsx` |
| 2 | F2.5 — Create listing page + image upload | `src/pages/CreateListingPage.tsx`, `src/components/ImageUpload.tsx` |
| 2 | F2.7 — Add listing routes to App.tsx | `src/App.tsx` |
| 3 | F3.1 — Messages API functions | `src/api/messages.ts` |
| 3 | F3.2 — Message thread component | `src/components/MessageThread.tsx` |
| 3 | F3.3 — Messaging UI in listing detail | `src/pages/ListingDetailPage.tsx` |
| 3 | F3.7a — UI polish on own pages | `RegisterPage`, `VerifyPage`, `LoginPage`, `ListingDetailPage`, `CreateListingPage` |
| 3 | F3.8a — Responsive design on own pages | `RegisterPage`, `VerifyPage`, `LoginPage`, `ListingDetailPage`, `CreateListingPage` |

#### Harnaindeep Kaur — Components and Styling

| Phase | Task | File(s) |
|-------|------|---------|
| 1 | F1.3 — TypeScript types | `src/types/index.ts` |
| 1 | F1.4 — Auth context + protected route | `src/context/AuthContext.tsx`, `src/hooks/useAuth.ts`, `src/components/ProtectedRoute.tsx` |
| 1 | F1.7 — Layout + Navbar | `src/components/Layout.tsx`, `src/components/Navbar.tsx` |
| 1 | F1.9 — Global CSS + YU color variables | `src/styles/global.css`, `src/styles/variables.css` |
| 1 | — | `src/utils/validators.ts` |
| 2 | F2.2 — Listing card component | `src/components/ListingCard.tsx` |
| 2 | F2.3 — Browse page | `src/pages/BrowsePage.tsx` |
| 2 | F2.6 — My listings page | `src/pages/MyListingsPage.tsx` |
| 3 | F3.4 — Messages page | `src/pages/MessagesPage.tsx` |
| 3 | F3.5 — Search bar component | `src/components/SearchBar.tsx` |
| 3 | F3.6 — Integrate search into browse page | `src/pages/BrowsePage.tsx` |
| 3 | F3.7b — UI polish on own pages | `BrowsePage`, `MyListingsPage`, `MessagesPage` |
| 3 | F3.8b — Responsive design on own pages/components | `BrowsePage`, `MyListingsPage`, `MessagesPage`, `Layout`, `Navbar`, `SearchBar` |

---

## Project Structure

```
YUTrade/
  backend/
    app/
      main.py, config.py, database.py, dependencies.py
      models/     user, listing, image, message, verification
      schemas/    auth, user, listing, message
      routers/    auth, listings, messages
      services/   auth_service, email_service, listing_service, message_service
      utils/      security
    uploads/
    tests/        conftest, test_auth, test_listings, test_messages
    requirements.txt
    .env.example
  frontend/
    src/
      api/        client, auth, listings, messages
      context/    AuthContext
      hooks/      useAuth
      pages/      Register, Verify, Login, Browse, ListingDetail, CreateListing, MyListings, Messages
      components/ Layout, Navbar, ListingCard, MessageThread, ProtectedRoute, SearchBar, ImageUpload
      styles/     global.css, variables.css
      types/      index.ts
      utils/      validators.ts
    .env.example
  IMPLEMENTATION_PLAN.md
```

## How to Work on Your Tasks

1. **Read your assigned file** — each file has a detailed TODO comment at the top explaining exactly what to implement, including function signatures, data structures, and behavior.
2. **Follow the phase order** — Phase 1 tasks must be done before Phase 2, etc. Within a phase, check if your work depends on someone else's (e.g., routers depend on models being done first).
3. **No merge conflicts** — every file is assigned to exactly one person. You can all work on the same branch simultaneously without conflicts.
4. **Dependencies between team members:**
   - Mickey's models must be done before Daniel's services (Phase 1), Lakshan's services (Phase 2), and Raj's services (Phase 3)
   - Daniel's auth must be done before any protected endpoint works
   - Frontend API layer (Mai) depends on backend endpoints being functional
5. **Test locally** — backend devs run `uvicorn app.main:app --reload` and test via `http://localhost:8000/docs`. Frontend devs run `npm start`.

## API Documentation

Once the backend is running, visit `http://localhost:8000/docs` for interactive Swagger UI documentation of all endpoints.

See [IMPLEMENTATION_PLAN.md](./IMPLEMENTATION_PLAN.md) for the full API contract, database schema, and detailed phase breakdown.
