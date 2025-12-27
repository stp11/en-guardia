<script lang="ts">
  import { browser } from "$app/environment";
  import Footer from "$lib/components/app-footer.svelte";
  import Header from "$lib/components/app-header.svelte";
  import { QueryClient, QueryClientProvider } from "@tanstack/svelte-query";
  import "src/routes/layout.css";

  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        enabled: browser,
        gcTime: 5 * 60 * 1000, // 5 minutes - cache garbage collection
        refetchOnWindowFocus: false, // Don't refetch on window focus
        retry: 1,
      },
    },
  });

  let { children } = $props();
</script>

<QueryClientProvider client={queryClient}>
  <div
    class="absolute top-0 z-[-1] w-full gradient-background h-[300px] bg-gradient-to-b from-primary-yellow/15 to-transparent"
  ></div>
  <Header />
  <div class="flex flex-col min-h-dvh">
    <main class="flex flex-col flex-grow pt-2 p-6 md:pt-6">
      {@render children()}
    </main>
    <!-- <div class="relative">
      <div
        class="absolute bottom-0 left-0 z-[-1] w-full gradient-background-bottom h-[300px]
        bg-gradient-to-t from-primary-yellow/15 to-transparent
        "
      ></div>
      <Footer />
    </div> -->
    <Footer />
  </div>
</QueryClientProvider>
