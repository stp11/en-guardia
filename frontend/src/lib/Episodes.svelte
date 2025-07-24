<script lang="ts">
  import { getEpisodesApiEpisodesGet, type Episode } from 'client';
  import { onMount } from 'svelte';

  let episodes: Episode[] = [];

  onMount(async () => {
    const { data } = await getEpisodesApiEpisodesGet();
    episodes = data?.items ?? [];
  });
</script>

<div id="episodes">
  {#each episodes as episode}
    <div>
      <h2>{episode.title}</h2>
    </div>
  {/each}
</div>
