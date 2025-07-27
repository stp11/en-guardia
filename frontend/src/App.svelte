<script lang="ts">
  import { QueryClient, QueryClientProvider } from "@tanstack/svelte-query";

  import Footer from "lib/components/app-footer.svelte";
  // import Header from "lib/components/app-header.svelte";
  import Episodes from "lib/components/episodes/index.svelte";

  // import Hero from "lib/components/hero.svelte";

  const queryClient = new QueryClient();
</script>

<QueryClientProvider client={queryClient}>
  <!-- <Header /> -->
  <main class="p-10">
    <!-- <Hero /> -->
    <Episodes />
  </main>
  <Footer />
</QueryClientProvider>
