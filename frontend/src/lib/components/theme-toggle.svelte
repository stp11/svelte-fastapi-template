<script lang="ts">
  import { MoonIcon, SunIcon } from "@lucide/svelte";

  // app.html sets the initial class; this only reads and flips it.
  let dark = $state(document.documentElement.classList.contains("dark"));

  function toggle() {
    dark = !dark;
    document.documentElement.classList.toggle("dark", dark);
    try {
      localStorage.setItem("theme", dark ? "dark" : "light");
    } catch {
      // Storage blocked: the choice just lasts until reload.
    }
  }
</script>

<button
  class="p-1 text-zinc-500 transition-colors hover:text-zinc-900 dark:hover:text-zinc-100"
  aria-label="Switch to {dark ? 'light' : 'dark'} mode"
  onclick={toggle}
>
  {#if dark}
    <SunIcon class="size-3.5" />
  {:else}
    <MoonIcon class="size-3.5" />
  {/if}
</button>
