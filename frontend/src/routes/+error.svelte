<script lang="ts">
  import { page } from "$app/state";

  import { Button } from "lib/components/ui/button";
</script>

<div class="flex flex-1 items-center justify-center">
  <div class="space-y-4 text-center max-w-md mx-auto">
    <h1 class="text-xl font-bold">
      Error {page.status}.
    </h1>
    {#if page.status === 404}
      <p class="text-gray-800">
        Alguna cosa ha anat malament i t'has perdut en un moment indeterminat de la història.
      </p>
      <Button variant="link" href="/">Torna al present</Button>
    {:else}
      <p class="text-gray-800">Alguna cosa ha anat malament</p>
      <Button variant="link" href="/">Torna a la pàgina principal</Button>
    {/if}
  </div>
</div>
