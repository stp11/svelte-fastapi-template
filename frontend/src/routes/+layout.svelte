<script lang="ts">
  import AppHeader from "#lib/components/app-header.svelte";
  import { browser } from "$app/env";
  import { QueryClient, QueryClientProvider } from "@tanstack/svelte-query";

  import "../app.css";

  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        enabled: browser,
        refetchOnWindowFocus: false,
        retry: 1,
      },
    },
  });

  let { children } = $props();
</script>

<QueryClientProvider client={queryClient}>
  <div
    class="flex min-h-dvh flex-col bg-white text-zinc-900 antialiased dark:bg-zinc-950 dark:text-zinc-100"
  >
    <AppHeader />
    <main class="flex flex-1 flex-col">
      {@render children()}
    </main>
  </div>
</QueryClientProvider>
