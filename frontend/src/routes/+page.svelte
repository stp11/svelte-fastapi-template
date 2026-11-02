<script lang="ts">
  const apiUrl = import.meta.env.VITE_API_URL;

  const links = [
    {
      title: "SvelteKit",
      description: "Routing, layouts and loading data in the frontend.",
      href: "https://svelte.dev/docs/kit",
    },
    {
      title: "FastAPI",
      description: "Path operations, dependencies and validation.",
      href: "https://fastapi.tiangolo.com/",
    },
    {
      title: "SQLModel",
      description: "Models that are both Pydantic schemas and tables.",
      href: "https://sqlmodel.tiangolo.com/",
    },
    {
      title: "TanStack Query",
      description: "Fetching, caching and mutating server state.",
      href: "https://tanstack.com/query/latest/docs/framework/svelte/overview",
    },
  ];
</script>

<div class="mx-auto flex w-full max-w-5xl flex-1 flex-col px-6 py-10 sm:py-16">
  <section class="flex flex-1 flex-col items-center justify-center py-16 text-center sm:py-24">
    <h1 class="text-4xl font-semibold tracking-tight sm:text-6xl">
      <span class="text-orange-600 dark:text-orange-500">Svelte</span>
      <span class="text-zinc-400">+</span>
      <span class="text-teal-600 dark:text-teal-400">FastAPI</span>
    </h1>
    <p class="mt-4 max-w-xl text-balance text-lg text-zinc-600 dark:text-zinc-400">
      A minimal full-stack template: SvelteKit, Tailwind and TanStack Query in front; FastAPI,
      SQLModel, Postgres and Alembic behind, with a typed client generated from the API.
    </p>
    <div class="mt-8 flex flex-wrap justify-center gap-3">
      <a
        href="{apiUrl}/api/docs"
        target="_blank"
        rel="noreferrer"
        class="rounded-full bg-zinc-900 px-5 py-2.5 text-sm font-medium text-white transition-colors hover:bg-zinc-700 dark:bg-white dark:text-zinc-900 dark:hover:bg-zinc-200"
      >
        Open API docs
      </a>
      <a
        href="/demo"
        class="rounded-full border border-zinc-300 px-5 py-2.5 text-sm font-medium transition-colors hover:bg-zinc-100 dark:border-zinc-700 dark:hover:bg-zinc-900"
      >
        Try the demo
      </a>
    </div>
  </section>

  <nav class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
    {#each links as link (link.href)}
      <a
        href={link.href}
        target="_blank"
        rel="noreferrer"
        class="group rounded-xl border border-transparent px-4 py-3 transition-colors hover:border-zinc-200 hover:bg-zinc-50 dark:hover:border-zinc-800 dark:hover:bg-zinc-900"
      >
        <h3 class="font-semibold">
          {link.title}
          <span class="inline-block transition-transform group-hover:translate-x-1">→</span>
        </h3>
        <p class="mt-1 text-sm text-zinc-600 dark:text-zinc-400">{link.description}</p>
      </a>
    {/each}
  </nav>
</div>
