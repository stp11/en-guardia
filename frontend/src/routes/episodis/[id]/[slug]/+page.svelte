<script lang="ts">
  import { capitalize, getCategoryStyles } from "lib/utils";

  const { data } = $props();
</script>

{#if data.episode}
  {@const episode = data.episode}

  <article class="container mx-auto max-w-7xl pt-2 sm:pt-4 lg:pt-6">
    <div class="flex flex-col lg:flex-row items-start gap-8">
      <!-- Video section -->
      <div class="w-full lg:w-1/2 aspect-video rounded-xl overflow-hidden shadow-sm bg-black">
        <iframe
          title={`audio ${episode.id}`}
          src={`https://www.3cat.cat/3cat/audio/${episode.id}/embed/`}
          allowfullscreen
          scrolling="no"
          class="w-full h-full"
        ></iframe>
      </div>

      <!-- Content section -->
      <div class="flex-1 w-full lg:w-1/2 lg:max-w-prose space-y-2 md:space-y-4">
        <header class="space-y-2">
          <h1 class="text-2xl md:text-3xl font-spline-sans">
            {episode.title}
          </h1>

          {#if episode.published_at}
            <span class="text-sm text-gray-500">Publicat el </span>
            <time class="text-sm text-gray-500">
              {new Date(episode.published_at).toLocaleDateString("ca-ES", {
                year: "numeric",
                month: "long",
                day: "numeric",
              })}
            </time>
          {/if}
        </header>

        <hr class="border-gray-200" />

        {#if episode.description}
          <p class="text-base leading-relaxed text-gray-700">
            {episode.description}
          </p>
        {/if}

        {#if episode.categories && episode.categories.length > 0}
          <div class="flex flex-wrap gap-2">
            {#each episode.categories as category (category.id)}
              <span class="text-xs rounded-md px-2 py-0.5 {getCategoryStyles(category.type)}">
                {capitalize(category.name)}
              </span>
            {/each}
          </div>
        {/if}
      </div>
    </div>
  </article>
{/if}
