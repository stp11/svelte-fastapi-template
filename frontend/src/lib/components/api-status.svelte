<script lang="ts">
  import { healthCheck } from "#client";
  import { createQuery } from "@tanstack/svelte-query";

  const health = createQuery(() => ({
    queryKey: ["health"],
    queryFn: async () => (await healthCheck({ throwOnError: true })).data,
  }));

  const apiUrl = import.meta.env.VITE_API_URL;

  const label = $derived(
    health.isPending ? "Connecting…" : health.isSuccess ? "API online" : "API offline"
  );
</script>

<span
  class="inline-flex items-center gap-2"
  title={health.isError ? `Can't reach the API at ${apiUrl}` : `API at ${apiUrl}`}
>
  <span
    class={[
      "size-2 rounded-full",
      health.isPending && "animate-pulse bg-zinc-400",
      health.isSuccess && "bg-emerald-500",
      health.isError && "bg-red-500",
    ]}
  ></span>
  <span class="max-sm:sr-only">{label}</span>
</span>
