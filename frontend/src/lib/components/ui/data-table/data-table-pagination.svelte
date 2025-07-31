<script lang="ts" generics="TData">
  import { ChevronLeft, ChevronRight } from "@lucide/svelte";
  import type { Table } from "@tanstack/table-core";

  import { Button } from "lib/components/ui/button";

  let { table }: { table: Table<TData> } = $props();
  const pageCount = $derived(table.getPageCount() || 1);
  const currentPage = $derived(table.getState().pagination.pageIndex + 1);
</script>

<div class="flex items-center justify-end gap-2">
  <div class="flex items-center gap-2">
    Pàgina {currentPage} de {pageCount}
    <div class="flex items-center gap-1 [&>button]:size-8">
      <Button
        onclick={() => table.previousPage()}
        disabled={!table.getCanPreviousPage()}
        variant="outline"
        size="icon"
        aria-label="Previous Page"
      >
        <ChevronLeft class="h-4 w-4" />
      </Button>
      <Button
        onclick={() => table.nextPage()}
        disabled={!table.getCanNextPage()}
        variant="outline"
        size="icon"
        aria-label="Next Page"
      >
        <ChevronRight class="h-4 w-4" />
      </Button>
    </div>
  </div>
</div>
