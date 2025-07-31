<script lang="ts">
  import { QueryClient, QueryClientProvider } from "@tanstack/svelte-query";

  import Footer from "lib/components/app-footer.svelte";
  import Episodes from "lib/components/episodes/index.svelte";

  const queryClient = new QueryClient();
</script>

<QueryClientProvider client={queryClient}>
  <div class="flex flex-col min-h-dvh">
    <main class="p-10 flex-grow">
      <Episodes />
    </main>
    <Footer />
  </div>
</QueryClientProvider>
