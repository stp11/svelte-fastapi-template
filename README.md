# Svelte + FastAPI template

- **Backend**: FastAPI, SQLModel, PostgreSQL, Alembic (repository → service → endpoint, wired with `Depends`)
- **Frontend**: SvelteKit (Svelte 5, static adapter), TailwindCSS v4, TanStack Query, API client generated with `@hey-api/openapi-ts`

## Development

Requirements: [Docker](https://www.docker.com/) and [Bun](https://bun.sh/).

```bash
make setup            # copy .env files, install frontend deps
make start-backend    # FastAPI + Postgres on http://localhost:8000 (docs at /api/docs)
make start-frontend   # SvelteKit on http://localhost:5173
```

Migrations run automatically when the backend starts.

## Common tasks

```bash
make migration m="add thing"   # autogenerate an Alembic revision after changing models.py
make generate-client           # regenerate frontend/src/client from the running backend
make test-backend              # pytest in a disposable database on the same server
make lint-frontend
make stop-backend              # the database volume is kept
```

## Deployment

The two halves deploy separately.

**Frontend.** SSR is off, so `bun run build` outputs a plain static site in `frontend/build`, ready for any static host: Cloudflare Pages, Netlify, Vercel, an S3 bucket… On Cloudflare Pages, for example:

| Setting                | Value                               |
| ---------------------- | ----------------------------------- |
| Root directory         | `frontend`                          |
| Build command          | `bun run build`                     |
| Build output directory | `build`                             |
| Environment variable   | `VITE_API_URL` = your API's URL     |

`VITE_API_URL` is baked in at build time, so changing it needs a rebuild. Unknown paths fall back to `index.html`, so client-side routes work on reload.

**Backend.** The root `Dockerfile` builds a production image (no dev dependencies) that runs migrations and then starts uvicorn on `$PORT`. Run it on any container host with `DATABASE_URL` set, and add the frontend's domain to `ALLOWED_ORIGINS`.
