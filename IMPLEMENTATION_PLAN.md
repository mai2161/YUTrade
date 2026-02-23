# YU Trade - Full Implementation Plan

## Context

YU Trade is a verified campus marketplace for York University (EECS4314 course project). It allows students and faculty to buy/sell items within a trusted community, restricted to `@my.yorku.ca` and `@yorku.ca` email addresses. The project has 6 team members (4 backend, 2 frontend). All stub files have been created with TODO instructions — each team member needs to implement their assigned files.

**Team Assignments:**
- **Backend (4 members):**
  - Mickey (Michael Byalsky) — DB layer (models, schema, database setup)
  - Daniel Chahine — Authentication (auth routes, JWT, email verification)
  - Lakshan Kandeepan — Listings (listing routes, CRUD, image handling)
  - Raj (Rajendra Brahmbhatt) — Messaging (message routes, thread logic)
- **Frontend (2 members):**
  - Mai Komar — Frontend pages and components
  - Harnaindeep Kaur — Frontend pages and components

**Decisions made:** JWT auth, file system image storage, React + TypeScript frontend, FastAPI + SQLAlchemy backend, SQLite database.

---

## 1. Project Structure

### Backend (`backend/`)

```
backend/
  app/
    __init__.py
    main.py                  # FastAPI app, CORS, static files, router includes
    config.py                # Settings via env vars (SECRET_KEY, DB URL, SMTP, etc.)
    database.py              # SQLAlchemy engine, SessionLocal, Base
    dependencies.py          # get_db, get_current_user (JWT dependency)
    models/
      __init__.py
      user.py                # User ORM model
      listing.py             # Listing ORM model
      image.py               # Image ORM model
      message.py             # Message ORM model
      verification.py        # VerificationCode ORM model
    schemas/
      __init__.py
      user.py                # Pydantic: UserOut
      listing.py             # Pydantic: ListingCreate, ListingOut, ListingUpdate
      message.py             # Pydantic: MessageCreate, MessageOut
      auth.py                # Pydantic: RegisterRequest, LoginRequest, TokenResponse, VerifyRequest
    routers/
      __init__.py
      auth.py                # POST /auth/register, /auth/verify, /auth/login
      listings.py            # GET/POST /listings, GET/PATCH /listings/{id}
      messages.py            # POST/GET /listings/{id}/messages
    services/
      __init__.py
      auth_service.py        # Registration, verification, login logic
      email_service.py       # Send verification email (SMTP or console stub)
      listing_service.py     # Listing CRUD logic
      message_service.py     # Message thread logic
    utils/
      __init__.py
      security.py            # JWT encode/decode, password hashing (passlib + python-jose)
  uploads/
    .gitkeep
  tests/
    __init__.py
    conftest.py              # pytest fixtures (test client, test DB, auth headers)
    test_auth.py
    test_listings.py
    test_messages.py
  requirements.txt
  .env.example
```

### Frontend (`frontend/`)

```
frontend/
  src/
    index.tsx
    App.tsx                  # Router setup, AuthProvider wrapper
    api/
      client.ts              # Axios instance with JWT interceptor
      auth.ts                # register(), verify(), login()
      listings.ts            # getListings(), createListing(), getListing(), updateListing()
      messages.ts            # sendMessage(), getMessages()
    context/
      AuthContext.tsx         # User state, token, login/logout helpers
    hooks/
      useAuth.ts
    pages/
      RegisterPage.tsx
      VerifyPage.tsx
      LoginPage.tsx
      BrowsePage.tsx         # Listings grid with search/filter
      ListingDetailPage.tsx  # Single listing + message thread
      CreateListingPage.tsx
      MyListingsPage.tsx     # User's own listings (update status)
      MessagesPage.tsx       # All conversations
    components/
      Layout.tsx             # Navbar, footer, main wrapper
      Navbar.tsx
      ListingCard.tsx
      MessageThread.tsx
      ProtectedRoute.tsx
      SearchBar.tsx
      ImageUpload.tsx
    styles/
      global.css
      variables.css          # YU colors: red #E31837, white, dark grey
    types/
      index.ts               # TypeScript interfaces: User, Listing, Message, etc.
    utils/
      validators.ts          # Email domain check, form helpers
  package.json
  tsconfig.json
  .env.example               # REACT_APP_API_URL=http://localhost:8000
```

---

## 2. Database Schema

### `users`
| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PK, autoincrement |
| email | VARCHAR(255) | UNIQUE, NOT NULL, must be @my.yorku.ca or @yorku.ca |
| password_hash | VARCHAR(255) | NOT NULL (bcrypt) |
| name | VARCHAR(100) | NOT NULL |
| is_verified | BOOLEAN | NOT NULL, DEFAULT FALSE |
| created_at | DATETIME | NOT NULL, DEFAULT now |

### `verification_codes`
| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PK, autoincrement |
| user_id | INTEGER | FK -> users.id, NOT NULL |
| code | VARCHAR(6) | NOT NULL (random 6-digit) |
| expires_at | DATETIME | NOT NULL (created_at + 15 min) |
| used | BOOLEAN | NOT NULL, DEFAULT FALSE |

### `listings`
| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PK, autoincrement |
| seller_id | INTEGER | FK -> users.id, NOT NULL |
| title | VARCHAR(200) | NOT NULL |
| description | TEXT | optional |
| price | DECIMAL(10,2) | NOT NULL |
| category | VARCHAR(50) | optional (e.g. "Textbooks", "Electronics", "Furniture") |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'active' (active/sold/removed) |
| created_at | DATETIME | NOT NULL, DEFAULT now |
| updated_at | DATETIME | NOT NULL, DEFAULT now, auto-update |

### `images`
| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PK, autoincrement |
| listing_id | INTEGER | FK -> listings.id, CASCADE delete |
| file_path | VARCHAR(500) | NOT NULL (relative path under uploads/) |
| position | INTEGER | NOT NULL, DEFAULT 0 |

### `messages`
| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PK, autoincrement |
| listing_id | INTEGER | FK -> listings.id, NOT NULL |
| sender_id | INTEGER | FK -> users.id, NOT NULL |
| receiver_id | INTEGER | FK -> users.id, NOT NULL |
| content | TEXT | NOT NULL |
| created_at | DATETIME | NOT NULL, DEFAULT now |

**Indexes:** `listings.seller_id`, `listings.status`, `messages.listing_id`, `messages.sender_id`, `messages.receiver_id`

---

## 3. API Contract

Auth-protected endpoints require `Authorization: Bearer <token>`.

### Auth
| Method | Endpoint | Auth | Request | Success | Errors |
|--------|----------|------|---------|---------|--------|
| POST | /auth/register | No | `{email, password, name}` | 201 `{message, user_id}` | 400 bad domain, 409 duplicate |
| POST | /auth/verify | No | `{email, code}` | 200 `{message}` | 400 invalid/expired |
| POST | /auth/login | No | `{email, password}` | 200 `{access_token, token_type, user}` | 401 bad creds, 403 not verified |

### Listings
| Method | Endpoint | Auth | Request | Success |
|--------|----------|------|---------|---------|
| GET | /listings?search=&category=&status=active&page=1&limit=20 | Optional | query params | 200 `{listings[], total, page, limit}` |
| POST | /listings | Required | multipart/form-data: title, description, price, category, images[] | 201 full listing object |
| GET | /listings/{id} | Optional | - | 200 full listing with images + seller |
| PATCH | /listings/{id} | Required (owner) | `{status?, title?, description?, price?}` | 200 updated listing |

### Messages
| Method | Endpoint | Auth | Request | Success |
|--------|----------|------|---------|---------|
| POST | /listings/{id}/messages | Required | `{content}` | 201 message object |
| GET | /listings/{id}/messages | Required (participant) | - | 200 `{messages[]}` |

---

## 4. Phase-by-Phase Implementation

### Phase 1: Foundation (Auth + DB + Setup)

**Backend tasks:**
1. **B1.1** Create folder structure, `requirements.txt`, `.env.example`, `main.py` (CORS, lifespan) — *Mickey*
2. **B1.2** Implement `config.py`, `database.py` (engine, session, Base) — *Mickey*
3. **B1.3** Implement User and VerificationCode ORM models — *Mickey*
4. **B1.4** Implement auth schemas (RegisterRequest, VerifyRequest, LoginRequest, TokenResponse) — *Daniel*
5. **B1.5** Implement `security.py` (password hashing, JWT create/decode) — *Daniel*
6. **B1.6** Implement `dependencies.py` (get_db, get_current_user) — *Daniel*
7. **B1.7** Implement `auth_service.py` + `email_service.py` (with console dev mode) — *Daniel*
8. **B1.8** Implement `routers/auth.py` (register, verify, login endpoints) — *Daniel*
9. **B1.9a** Write `conftest.py` (test DB fixtures) — *Mickey*
10. **B1.9b** Write `test_auth.py` — *Daniel*
11. **B1.10** Set up GitHub Actions CI — *Raj*

**Frontend tasks:**
1. **F1.1** Scaffold React app with `create-react-app --template typescript` — *Mai*
2. **F1.2** Set up Axios client with JWT interceptor — *Mai*
3. **F1.3** Create TypeScript types (`src/types/index.ts`) — *Harnaindeep*
4. **F1.4** Implement AuthContext + ProtectedRoute — *Harnaindeep*
5. **F1.5** Implement RegisterPage, VerifyPage, LoginPage — *Mai*
6. **F1.6** Set up React Router in App.tsx — *Mai*
7. **F1.7** Create Layout + Navbar components (YU branding) — *Harnaindeep*
8. **F1.8** Create `src/api/auth.ts` — *Mai*
9. **F1.9** Global CSS with YU color variables (red #E31837) — *Harnaindeep*

**Checkpoint:** User can register, verify (code logged to console), and log in. JWT stored, Navbar shows logged-in state.

---

### Phase 2: Listings

**Backend tasks:**
1. **B2.1** Implement Listing and Image ORM models — *Mickey*
2. **B2.2** Implement listing schemas (ListingCreate, ListingOut, ListingUpdate, PaginatedListings) — *Lakshan*
3. **B2.3** Implement `listing_service.py` (create with images, get paginated, get by id, update) — *Lakshan*
4. **B2.4** Image upload handling (save to `uploads/` with UUID filenames, serve via StaticFiles) — *Lakshan*
5. **B2.5** Implement `routers/listings.py` — *Lakshan*
6. **B2.6** Write `test_listings.py` — *Lakshan*

**Frontend tasks:**
1. **F2.1** Create `src/api/listings.ts` — *Mai*
2. **F2.2** Implement ListingCard component — *Harnaindeep*
3. **F2.3** Implement BrowsePage (grid of cards) — *Harnaindeep*
4. **F2.4** Implement ListingDetailPage (images, details, contact button) — *Mai*
5. **F2.5** Implement CreateListingPage (form + ImageUpload component) — *Mai*
6. **F2.6** Implement MyListingsPage (own listings, status toggle) — *Harnaindeep*
7. **F2.7** Add listing routes to App.tsx — *Mai*

**Checkpoint:** Users can create listings with images, browse all listings, view details, and update their own listing status.

---

### Phase 3: Messaging + Search/Filter + Polish

**Backend tasks:**
1. **B3.1** Implement Message ORM model — *Mickey*
2. **B3.2** Implement message schemas (MessageCreate, MessageOut) — *Raj*
3. **B3.3** Implement `message_service.py` (send message, get thread, get user threads) — *Raj*
4. **B3.4** Implement `routers/messages.py` — *Raj*
5. **B3.5** Add search/filter to GET /listings (search, category, min/max price) — *Lakshan*
6. **B3.6** Write `test_messages.py` — *Raj*

**Frontend tasks:**
1. **F3.1** Create `src/api/messages.ts` — *Mai*
2. **F3.2** Implement MessageThread component — *Mai*
3. **F3.3** Add messaging UI to ListingDetailPage — *Mai*
4. **F3.4** Implement MessagesPage (all threads by listing) — *Harnaindeep*
5. **F3.5** Implement SearchBar (text + category dropdown + price range) — *Harnaindeep*
6. **F3.6** Integrate SearchBar into BrowsePage — *Harnaindeep*
7. **F3.7a** UI polish on own pages (loading spinners, empty states, error handling) — *Mai* (RegisterPage, VerifyPage, LoginPage, ListingDetailPage, CreateListingPage)
8. **F3.7b** UI polish on own pages (loading spinners, empty states, error handling) — *Harnaindeep* (BrowsePage, MyListingsPage, MessagesPage)
9. **F3.8a** Responsive design pass on own pages — *Mai* (RegisterPage, VerifyPage, LoginPage, ListingDetailPage, CreateListingPage)
10. **F3.8b** Responsive design pass on own pages and components — *Harnaindeep* (BrowsePage, MyListingsPage, MessagesPage, Layout, Navbar, SearchBar)

**Checkpoint:** Full user flow works: register -> verify -> login -> create listing -> browse/search -> message seller -> view conversations.

---

### Phase 4: Testing + Deployment

1. End-to-end manual testing of all flows — *all 6*
2. Fix integration bugs — *all 6*
3. Increase backend test coverage — *Mickey, Daniel, Lakshan, Raj*
4. Add frontend component tests — *Mai, Harnaindeep*
5. Finalize GitHub Actions CI — *Raj + Mai*
6. Write README with setup instructions — *Raj*
7. Final bug bash and demo preparation — *all 6*

---

## 5. Key Technical Patterns

### Dev Workflow
- Backend: `uvicorn app.main:app --reload` on `http://localhost:8000`
- Frontend: `npm start` on `http://localhost:3000`
- FastAPI auto-docs at `http://localhost:8000/docs` for backend testing
- Email verification logs code to console in dev mode (`EMAIL_BACKEND=console` env var)

### Dependencies (in order)
- `requirements.txt`: fastapi, uvicorn, sqlalchemy, pydantic, python-jose, passlib[bcrypt], python-multipart, python-dotenv, aiosmtplib, pytest, httpx
- `package.json`: react, react-dom, react-router-dom, axios, typescript, @testing-library/react

### Architecture Principles
- **Service layer pattern**: Routers -> Services -> DB. Routers handle HTTP, services handle business logic.
- **Sync SQLAlchemy**: No async needed for SQLite course project.
- **JWT in localStorage**: Axios interceptor auto-attaches token and handles 401 redirects.
- **Multipart form** for listing creation (images), JSON for everything else.
- **Message threading by listing**: All messages between two users about a specific listing = one thread.

---

## 6. Scaffolding Status

All stub files have been created with detailed TODO comments describing the implementation requirements. Each file includes its assigned team member and the phase it belongs to. **No implementation code has been written yet** — every file is a stub with instructions.

What has been scaffolded:
1. Full backend folder structure with all `__init__.py` files, `requirements.txt`, `.env.example`
2. Core backend files: `main.py`, `config.py`, `database.py`, `dependencies.py`, `security.py`
3. All ORM models and Pydantic schemas (as TODO stubs)
4. Router and service stubs with detailed endpoint specifications
5. Test scaffolding with `conftest.py` and test files with listed test cases
6. Frontend folder structure: `api/`, `context/`, `hooks/`, `pages/`, `components/`, `styles/`, `types/`
7. All frontend component, page, and utility stubs with TODO instructions

What still needs to be done manually:
- Frontend scaffolding with `npx create-react-app frontend --template typescript` (will generate `package.json`, `tsconfig.json`, etc. — then move our stub files into the generated `src/`)
- `.gitignore` at project root
- GitHub Actions CI workflow (B1.10, assigned to Raj)

---

## 7. Verification

After implementation:
- `cd backend && pip install -r requirements.txt && uvicorn app.main:app --reload` should start without errors
- `cd frontend && npm install && npm start` should show the React app
- `http://localhost:8000/docs` should show the FastAPI OpenAPI docs
- `pytest backend/tests/` should discover and run all tests
