<script lang="ts">
  import Github from "lib/components/github.svelte";
  import { Button } from "lib/components/ui/button";
</script>

<footer class="px-6 md:px-10 text-sm">
  <div class="border-t py-4 flex justify-between items-center gap-4 xl:max-w-screen-xl 2xl:mx-auto">
    <div class="ml-auto">
      <Button
        variant="ghost"
        size="icon"
        href="https://github.com/stp11/en-guardia"
        target="_blank"
        rel="noopener noreferrer"
      >
        <Github />
      </Button>
    </div>
  </div>
</footer>
