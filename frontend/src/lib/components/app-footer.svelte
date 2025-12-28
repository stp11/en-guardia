<script lang="ts">
  import Github from "lib/components/github.svelte";
  import { Button } from "lib/components/ui/button";
</script>

<footer class="px-6 text-sm text-center flex w-full justify-center 2xl:mx-auto">
  <div class="border-t py-4 w-full flex justify-center items-center gap-2 xl:max-w-screen-xl">
    <div class="text-muted-foreground ml-auto">
      <small>© {new Date().getFullYear()} Arxiu En Guàrdia</small>
      &dash;
      <small>
        <a
          href="https://github.com/stp11/en-guardia/blob/main/LICENCE.txt"
          target="_blank"
          rel="noopener noreferrer"
          class="underline hover:text-foreground transition-colors"
        >
          Llicència MIT
        </a>
      </small>
    </div>
    <Button
      variant="ghost"
      size="icon"
      href="https://github.com/stp11/en-guardia"
      target="_blank"
      rel="noopener noreferrer"
      class="ml-auto"
    >
      <Github />
    </Button>
  </div>
</footer>
