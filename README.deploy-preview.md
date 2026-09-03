# Deploying a shareable preview (Render)

`render.yaml` in the repo root defines a free Render Blueprint: a Postgres
database, the Django/Channels API, and the Vite/React static site, wired
together automatically. This is for showing someone a working link - see
the caveats at the bottom before treating it as a real production deploy.

## One-time setup

1. Sign up at [render.com](https://render.com) (GitHub sign-in is fine, no
   credit card needed for the free tier).
2. **New +** → **Blueprint** → pick the `academia-platform` GitHub repo →
   **Apply**.
3. Render creates all three resources and deploys them. The first deploy
   takes a few minutes (installs Python/Node deps, runs migrations, seeds
   demo content and a demo account).
4. Once green, the frontend is live at:
   `https://academia-frontend.onrender.com`

Send that link. Log in with:

- **Username:** `employer_demo`
- **Password:** `Kanoon@2026Demo`

(A separate `admin_demo` / `Kanoon@2026Admin` account also exists, for the
Django admin at `/admin/` on the backend URL.)

## What's seeded automatically

Every deploy re-runs `python manage.py seed_preview_content`, which:
- creates the two demo accounts above (idempotent - won't duplicate)
- loads the 11 shop products and 5 gallery images captured from the live
  site (`data/preview/*.json` + `data/preview/media/`)

## Caveats - this is a preview, not the real deployment

- **The free Postgres database expires 30 days after creation** (with a
  14-day grace period), then Render deletes it. Fine for a demo link that's
  looked at once; if you want this to stay up long-term, upgrade the
  database to a paid instance in the Render dashboard before it expires.
- **The free web service spins down after ~15 minutes idle** and takes
  20-60s to wake back up on the next request - the first click after a
  while looks slow, not broken.
- **AI chat won't work** - `GOOGLE_API_KEY` / `LLM_API_KEY` aren't set (they
  live only in the real production `.env`, never committed). Every other
  feature (shop, gallery, courses, exams, panel) works.
- **Payments are sandboxed** - Zibal's `merchant=zibal` test mode, not the
  real merchant account.
- Two separate Render services means two separate origins; this is a
  deliberate deploy shape (see `AUTH_COOKIE_DOMAIN` and `BACKEND_BASE_URL`
  in `render.yaml`) and doesn't reflect how the real
  `ariantafazolizadeh.ir` deployment is set up (one shared domain).

## Updating the preview

Render auto-deploys on every push to `main` by default. To pick up new
preview content, refresh `data/preview/*.json` and `data/preview/media/`
(see the note at the top of `shop/management/commands/seed_preview_content.py`)
and push - the next deploy re-seeds automatically.
