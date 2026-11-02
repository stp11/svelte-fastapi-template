<script lang="ts">
  import ApiStatus from "#lib/components/api-status.svelte";
  import ThemeToggle from "#lib/components/theme-toggle.svelte";
  import { page } from "$app/state";

  const links = [{ href: "/demo", label: "Demo" }];

  const apiUrl = import.meta.env.VITE_API_URL;
</script>

<header
  class="sticky top-0 z-10 border-b border-zinc-200 bg-white/80 backdrop-blur dark:border-zinc-800 dark:bg-zinc-950/80"
>
  <div class="mx-auto flex h-14 max-w-5xl items-center gap-6 px-6">
    <a href="/" class="flex items-center gap-2 text-sm font-semibold tracking-tight">
      <span class="size-5 rounded-md bg-linear-to-br from-orange-500 to-teal-500" aria-hidden="true"
      ></span>
      Svelte + FastAPI
    </a>

    <nav class="flex items-center gap-1 text-sm">
      {#each links as link (link.href)}
        <a
          href={link.href}
          aria-current={page.url.pathname === link.href ? "page" : undefined}
          class="rounded-md px-2.5 py-1.5 text-zinc-500 transition-colors hover:text-zinc-900 aria-[current=page]:bg-zinc-100 aria-[current=page]:text-zinc-900 dark:hover:text-zinc-100 dark:aria-[current=page]:bg-zinc-800 dark:aria-[current=page]:text-zinc-100"
        >
          {link.label}
        </a>
      {/each}
      <a
        href="{apiUrl}/api/docs"
        target="_blank"
        rel="noreferrer"
        class="rounded-md px-2.5 py-1.5 text-zinc-500 transition-colors hover:text-zinc-900 dark:hover:text-zinc-100"
      >
        API docs
      </a>
    </nav>

    <div class="ml-auto flex items-center gap-3 text-xs text-zinc-500">
      <ApiStatus />
      <span class="h-4 w-px bg-zinc-200 dark:bg-zinc-800" aria-hidden="true"></span>
      <ThemeToggle />
    </div>
  </div>
</header>
