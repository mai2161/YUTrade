# YUTrade — Retrospective & Next Steps

## Project Summary

YUTrade is a campus marketplace for York University students, built over ~5 weeks (Feb 22 – Apr 1, 2026) by a team of 6. The project reached feature-complete status with 215 commits across a FastAPI + React TypeScript stack.

---

## What Went Well

- **Feature completeness** — All core marketplace features were delivered: auth with email verification, listing CRUD with image uploads, messaging, seller ratings, search/filtering/pagination, and account management.
- **Test coverage** — 254 backend tests covering auth, listings, messages, ratings, and cross-feature integration. Tests use in-memory SQLite for fast, isolated execution.
- **Clean architecture** — Backend follows a consistent Router → Service → DB layered pattern, making the codebase easy to navigate and extend. Frontend mirrors this with dedicated API modules, context-based state, and reusable components.
- **Team velocity** — 6 contributors shipped a full-stack app with deployment config, seed data, and documentation in a compressed timeline. Contributors: Daniel Chahine (82 commits), Rajendra (69), mai2161 (18), Lakshan (17), Harnain (15), Mickey (12).
- **Documentation** — README, implementation plan, 51KB project overview, architecture diagrams (Mermaid), and CLAUDE.md provide strong project context.

## What Could Be Improved

- **No CI pipeline for tests** — The only GitHub Action is a Discord push notification. Automated test runs on PRs would have caught regressions earlier (e.g., the `is_read` database schema mismatch).
- **Database migrations** — No migration tool (e.g., Alembic) is in place. Schema changes required manual DB recreation, which led to at least one schema drift issue (Message `is_read` column missing from the live DB).
- **Frontend testing** — Zero frontend tests despite the testing library being installed. All 254 tests are backend-only.
- **No real-time messaging** — Messaging is REST-based (fetch on page load). Users must refresh to see new messages.
- **Maps page is a stub** — The page exists but isn't fully integrated with real functionality.
- **SQLite in production** — Fine for a course project, but would not scale for concurrent users.

## Lessons Learned

1. **Set up CI early** — Even a simple `pytest` GitHub Action on PRs saves significant debugging time.
2. **Use a migration tool from day one** — Adding Alembic after the fact is harder than starting with it.
3. **Frontend tests matter** — Component tests (React Testing Library) catch UI regressions that backend tests cannot.
4. **Branch strategy worked** — Feature branches with PRs kept main stable and enabled code review.

---

## Next Steps (If Continued)

### High Priority

| # | Task | Effort | Impact |
|---|------|--------|--------|
| 1 | **Add Alembic migrations** — Fix `is_read` schema drift and prevent future mismatches | Medium | Critical |
| 2 | **CI/CD pipeline** — GitHub Actions to run `pytest` on PRs and deploy on merge to main | Low | High |
| 3 | **Frontend tests** — Add React Testing Library tests for auth flows, listing CRUD, and messaging | Medium | High |
| 4 | **WebSocket messaging** — Replace polling with real-time message delivery via FastAPI WebSockets | High | High |

### Medium Priority

| # | Task | Effort | Impact |
|---|------|--------|--------|
| 5 | **Image optimization** — Resize/compress uploads, serve via CDN instead of local `uploads/` dir | Medium | Medium |
| 6 | **Notifications** — Email or in-app notifications for new messages, listing status changes | Medium | Medium |
| 7 | **Maps integration** — Complete the maps page with campus meetup location selection | Medium | Medium |
| 8 | **Migrate to PostgreSQL** — Replace SQLite for production readiness and concurrent write support | Low | Medium |

### Future Enhancements

| # | Task | Effort | Impact |
|---|------|--------|--------|
| 9 | **Saved listings / watchlist** — Let users bookmark listings they're interested in | Low | Medium |
| 10 | **Admin dashboard** — Moderation tools for flagging/removing inappropriate listings | Medium | Medium |
| 11 | **Mobile responsive polish** — Audit and fix mobile UX across all pages | Low | Medium |
| 12 | **OAuth login** — "Sign in with York" if York provides SSO, or Google OAuth with domain restriction | High | Low |
| 13 | **Payment integration** — Optional in-app payment via Stripe for trusted transactions | High | Low |
| 14 | **Analytics** — Track listing views, search patterns, and user engagement metrics | Medium | Low |

---

## Final Assessment

YUTrade successfully delivers a working campus marketplace with all core features, strong backend test coverage, and clean architecture. For an EECS 4314 course project, the scope and quality are solid. The main gaps — no frontend tests, no CI, and no DB migrations — are common in time-boxed academic projects and would be the first priorities if development continues.
