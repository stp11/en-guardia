<script lang="ts">
  import Footer from "lib/components/app-footer.svelte";
  import Header from "lib/components/app-header.svelte";
  import Episodes from "lib/components/episodes/index.svelte";
  import Hero from "lib/components/hero.svelte";
</script>

<Header />
<main class="px-10 pb-10">
  <Hero />
  <Episodes />
</main>
<Footer />
