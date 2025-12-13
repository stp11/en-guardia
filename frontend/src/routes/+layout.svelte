<script lang="ts">
  import Footer from "$lib/components/app-footer.svelte";
  import { QueryClient, QueryClientProvider } from "@tanstack/svelte-query";
  import "src/routes/layout.css";

  const queryClient = new QueryClient();
  let { children } = $props();
</script>

<QueryClientProvider client={queryClient}>
  <div class="flex flex-col min-h-dvh">
    <main class="flex flex-col flex-grow p-6 md:p-10">
      {@render children()}
    </main>
    <Footer />
  </div>
</QueryClientProvider>
