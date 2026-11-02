<script lang="ts">
  import { createItem, deleteItem, getItems, updateItem } from "#client";
  import type { ItemPublic } from "#client";
  import { CheckIcon, InboxIcon, PencilIcon, PlusIcon, Trash2Icon, XIcon } from "@lucide/svelte";
  import { createMutation, createQuery, useQueryClient } from "@tanstack/svelte-query";

  const queryClient = useQueryClient();
  const invalidate = () => queryClient.invalidateQueries({ queryKey: ["items"] });

  const items = createQuery(() => ({
    queryKey: ["items"],
    queryFn: async () => (await getItems({ throwOnError: true })).data,
  }));

  const addItem = createMutation(() => ({
    mutationFn: async (body: { name: string; description: string | null }) =>
      (await createItem({ body, throwOnError: true })).data,
    onSuccess: invalidate,
  }));

  const editItem = createMutation(() => ({
    mutationFn: async (vars: { id: number; name: string; description: string | null }) =>
      (
        await updateItem({
          path: { id: vars.id },
          body: { name: vars.name, description: vars.description },
          throwOnError: true,
        })
      ).data,
    onSuccess: invalidate,
  }));

  const removeItem = createMutation(() => ({
    mutationFn: (id: number) => deleteItem({ path: { id }, throwOnError: true }),
    onSuccess: invalidate,
  }));

  let name = $state("");
  let description = $state("");

  function onsubmit(e: SubmitEvent) {
    e.preventDefault();
    if (!name.trim()) return;
    addItem.mutate(
      { name: name.trim(), description: description.trim() || null },
      {
        onSuccess: () => {
          name = "";
          description = "";
        },
      }
    );
  }

  let editingId = $state<number | null>(null);
  let editName = $state("");
  let editDescription = $state("");

  function startEdit(item: ItemPublic) {
    editItem.reset();
    editingId = item.id;
    editName = item.name;
    editDescription = item.description ?? "";
  }

  function cancelOnEscape(e: KeyboardEvent) {
    if (e.key === "Escape") editingId = null;
  }

  function saveEdit(e: SubmitEvent) {
    e.preventDefault();
    if (editingId === null || !editName.trim()) return;
    editItem.mutate(
      { id: editingId, name: editName.trim(), description: editDescription.trim() || null },
      { onSuccess: () => (editingId = null) }
    );
  }

  const relativeTime = new Intl.RelativeTimeFormat(undefined, { numeric: "auto" });

  // "just now", "5 minutes ago", "yesterday"…
  function timeAgo(iso: string) {
    const seconds = (new Date(iso).getTime() - Date.now()) / 1000;
    const units: [Intl.RelativeTimeFormatUnit, number][] = [
      ["day", 86400],
      ["hour", 3600],
      ["minute", 60],
    ];
    for (const [unit, size] of units) {
      if (Math.abs(seconds) >= size) return relativeTime.format(Math.round(seconds / size), unit);
    }
    return "just now";
  }

  const input =
    "min-w-0 rounded-lg border border-zinc-300 bg-white px-3 py-2 text-sm outline-none placeholder:text-zinc-400 focus:border-zinc-500 focus:ring-2 focus:ring-zinc-200 dark:border-zinc-700 dark:bg-zinc-950 dark:focus:ring-zinc-800";
  const iconButton =
    "shrink-0 rounded-md p-1.5 text-zinc-400 transition-colors hover:bg-zinc-100 hover:text-zinc-900 disabled:pointer-events-none disabled:opacity-50 dark:hover:bg-zinc-800 dark:hover:text-zinc-100";
</script>

<svelte:head>
  <title>Demo · Svelte + FastAPI</title>
</svelte:head>

<div class="mx-auto w-full max-w-2xl px-6 py-10 sm:py-16">
  <h1 class="text-3xl font-semibold tracking-tight">Demo</h1>
  <p class="mt-2 text-sm text-zinc-600 dark:text-zinc-400">
    A small CRUD example: add, edit and remove items. Each change goes through the generated client
    to FastAPI and is stored in Postgres.
  </p>

  <div class="mt-10 mb-3 flex items-center gap-2">
    <h2 class="text-sm font-semibold">Items</h2>
    {#if items.isSuccess}
      <span
        class="rounded-full bg-zinc-100 px-2 py-0.5 text-xs font-medium text-zinc-600 tabular-nums dark:bg-zinc-800 dark:text-zinc-300"
      >
        {items.data.length}
      </span>
    {/if}
  </div>

  <div
    class="overflow-hidden rounded-xl border border-zinc-200 bg-white shadow-sm dark:border-zinc-800 dark:bg-zinc-900"
  >
    <form
      class="flex flex-col gap-2 border-b border-zinc-200 bg-zinc-50 p-4 sm:flex-row dark:border-zinc-800 dark:bg-zinc-900/50"
      {onsubmit}
    >
      <input
        class={[input, "flex-1"]}
        placeholder="Name"
        aria-label="Name"
        bind:value={name}
        maxlength="255"
      />
      <input
        class={[input, "flex-[1.5]"]}
        placeholder="Description (optional)"
        aria-label="Description"
        bind:value={description}
        maxlength="1000"
      />
      <button
        class="inline-flex items-center justify-center gap-1.5 rounded-lg bg-zinc-900 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-zinc-700 disabled:opacity-50 dark:bg-white dark:text-zinc-900 dark:hover:bg-zinc-200"
        disabled={addItem.isPending || !name.trim()}
      >
        <PlusIcon class="size-4" />
        Add
      </button>
    </form>

    {#if addItem.isError}
      <p
        class="border-b border-zinc-200 bg-red-50 px-4 py-2 text-sm text-red-700 dark:border-zinc-800 dark:bg-red-950/40 dark:text-red-400"
      >
        Couldn't add the item. Try again.
      </p>
    {/if}

    {#if items.isPending}
      <ul class="divide-y divide-zinc-200 dark:divide-zinc-800" aria-busy="true">
        {#each [1, 2, 3] as row (row)}
          <li class="flex items-center gap-4 px-4 py-3.5">
            <div class="h-4 w-1/3 animate-pulse rounded bg-zinc-200 dark:bg-zinc-800"></div>
            <div class="ml-auto h-3 w-16 animate-pulse rounded bg-zinc-200 dark:bg-zinc-800"></div>
          </li>
        {/each}
      </ul>
    {:else if items.isError}
      <p class="px-4 py-10 text-center text-sm text-red-600 dark:text-red-400">
        Couldn't load items. Is the backend running?
      </p>
    {:else if items.data.length === 0}
      <div class="flex flex-col items-center gap-2 px-4 py-12 text-center">
        <InboxIcon class="size-8 text-zinc-300 dark:text-zinc-700" />
        <p class="text-sm font-medium">No items yet</p>
        <p class="text-sm text-zinc-500">Add your first one above.</p>
      </div>
    {:else}
      <ul class="divide-y divide-zinc-200 dark:divide-zinc-800">
        {#each items.data as item (item.id)}
          {#if editingId === item.id}
            <li class="bg-zinc-50 px-4 py-3 dark:bg-zinc-900/50">
              <form class="flex flex-col gap-2 sm:flex-row sm:items-center" onsubmit={saveEdit}>
                <input
                  class={[input, "flex-1 py-1.5"]}
                  aria-label="Name"
                  bind:value={editName}
                  onkeydown={cancelOnEscape}
                  maxlength="255"
                  {@attach (el) => el.focus()}
                />
                <input
                  class={[input, "flex-[1.5] py-1.5"]}
                  placeholder="Description (optional)"
                  aria-label="Description"
                  bind:value={editDescription}
                  onkeydown={cancelOnEscape}
                  maxlength="1000"
                />
                <div class="flex justify-end gap-1">
                  <button
                    class={[iconButton, "text-emerald-600 dark:text-emerald-400"]}
                    aria-label="Save"
                    title="Save"
                    disabled={editItem.isPending || !editName.trim()}
                  >
                    <CheckIcon class="size-4" />
                  </button>
                  <button
                    type="button"
                    class={iconButton}
                    aria-label="Cancel"
                    title="Cancel (Esc)"
                    onclick={() => (editingId = null)}
                  >
                    <XIcon class="size-4" />
                  </button>
                </div>
              </form>
              {#if editItem.isError}
                <p class="mt-2 text-sm text-red-600 dark:text-red-400">
                  Couldn't save the changes. Try again.
                </p>
              {/if}
            </li>
          {:else}
            <li
              class={[
                "flex items-center gap-2 px-4 py-3 transition-opacity",
                removeItem.isPending && removeItem.variables === item.id && "opacity-40",
              ]}
            >
              <div class="min-w-0 flex-1">
                <p class="truncate text-sm font-medium">{item.name}</p>
                {#if item.description}
                  <p class="truncate text-sm text-zinc-500">{item.description}</p>
                {/if}
              </div>
              <time
                class="mr-2 shrink-0 text-xs text-zinc-500"
                datetime={item.created_at}
                title={new Date(item.created_at).toLocaleString()}
              >
                {timeAgo(item.created_at)}
              </time>
              <button
                class={iconButton}
                aria-label="Edit {item.name}"
                title="Edit"
                onclick={() => startEdit(item)}
              >
                <PencilIcon class="size-4" />
              </button>
              <button
                class={[
                  iconButton,
                  "hover:bg-red-50 hover:text-red-600 dark:hover:bg-red-950 dark:hover:text-red-400",
                ]}
                aria-label="Remove {item.name}"
                title="Remove"
                disabled={removeItem.isPending && removeItem.variables === item.id}
                onclick={() => removeItem.mutate(item.id)}
              >
                <Trash2Icon class="size-4" />
              </button>
            </li>
          {/if}
        {/each}
      </ul>
    {/if}
  </div>
</div>
