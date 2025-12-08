<script lang="ts">
  import Footer from "$lib/components/app-footer.svelte";
  import Episodes from "$lib/components/episodes/index.svelte";
  import { QueryClient, QueryClientProvider } from "@tanstack/svelte-query";

  const queryClient = new QueryClient();
</script>

<QueryClientProvider client={queryClient}>
  <div class="flex flex-col min-h-dvh">
    <main class="p-10 flex-grow">
      <!-- TODO add episode id to iframe -->
      <!-- <iframe
          title="audio 99546"
          src="https://www.3cat.cat/3cat/audio/99546/embed/"
          allowfullscreen
          scrolling="no"
          frameborder="0"
          width="500px"
          height="281px"
        ></iframe> -->
      <Episodes />
    </main>
    <Footer />
  </div>
</QueryClientProvider>
