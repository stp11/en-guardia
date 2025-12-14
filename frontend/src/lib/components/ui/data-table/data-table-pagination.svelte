<script lang="ts" generics="TData">
  import { ChevronLeft, ChevronRight, ChevronsLeft, ChevronsRight } from "@lucide/svelte";
  import type { Table } from "@tanstack/table-core";

  import { Button } from "lib/components/ui/button";
  import { Select, SelectContent, SelectItem, SelectTrigger } from "lib/components/ui/select";

  let { table }: { table: Table<TData> } = $props();
  const pageCount = $derived(table.getPageCount() || 1);
  const currentPage = $derived(table.getState().pagination.pageIndex + 1);
  const pageSize = $derived(table.getState().pagination.pageSize);
</script>

<div class="flex items-center space-x-6 lg:space-x-8 justify-end">
  <div class="flex items-center space-x-2">
    <p class="text-sm font-medium">Episodis per pàgina</p>
    <Select
      allowDeselect={false}
      type="single"
      value={`${pageSize}`}
      onValueChange={(value) => {
        if (value) {
          table.setPageSize(Number(value));
        }
      }}
    >
      <SelectTrigger class="h-8 w-[70px]">
        {String(pageSize)}
      </SelectTrigger>
      <SelectContent side="top">
        {#each [10, 20, 30, 40, 50] as pageSizeOption (pageSizeOption)}
          <SelectItem value={`${pageSizeOption}`}>
            {pageSizeOption}
          </SelectItem>
        {/each}
      </SelectContent>
    </Select>
  </div>
  <div class="flex w-[105px] items-center justify-center text-sm font-medium">
    Pàgina {currentPage} de {pageCount}
  </div>
  <div class="flex items-center space-x-2">
    <Button
      variant="outline"
      class="hidden size-8 p-0 lg:flex"
      onclick={() => table.setPageIndex(0)}
      disabled={!table.getCanPreviousPage()}
    >
      <span class="sr-only">Anar a la primera pàgina</span>
      <ChevronsLeft class="h-4 w-4" />
    </Button>
    <Button
      variant="outline"
      class="size-8 p-0"
      onclick={() => table.previousPage()}
      disabled={!table.getCanPreviousPage()}
    >
      <span class="sr-only">Anar a la pàgina anterior</span>
      <ChevronLeft class="h-4 w-4" />
    </Button>
    <Button
      variant="outline"
      class="size-8 p-0"
      onclick={() => table.nextPage()}
      disabled={!table.getCanNextPage()}
    >
      <span class="sr-only">Anar a la següent pàgina</span>
      <ChevronRight class="h-4 w-4" />
    </Button>
    <Button
      variant="outline"
      class="hidden size-8 p-0 lg:flex"
      onclick={() => table.setPageIndex(table.getPageCount() - 1)}
      disabled={!table.getCanNextPage()}
    >
      <span class="sr-only">Anar a la última pàgina</span>
      <ChevronsRight class="h-4 w-4" />
    </Button>
  </div>
</div>
