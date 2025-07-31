<script lang="ts">
  import { derived, writable } from "svelte/store";

  import { ChevronLeft, ChevronRight, Search } from "@lucide/svelte";
  import { createQuery } from "@tanstack/svelte-query";
  import {
    type SortingState,
    type Updater,
    getCoreRowModel,
    getSortedRowModel,
  } from "@tanstack/table-core";

  import { getEpisodesApiEpisodesGet } from "client";

  import { Button } from "lib/components/ui/button";
  import { FlexRender, createSvelteTable } from "lib/components/ui/data-table";
  import Input from "lib/components/ui/input.svelte";
  import * as Table from "lib/components/ui/table";
  import { debounce } from "lib/hooks/use-debounce";

  import DataTableHeader from "../ui/data-table/data-table-header.svelte";
  import { columns } from "./columns";

  const searchQuery = writable("");
  const page = writable(1);
  const sorting = writable<SortingState>([]);
  const order = derived(sorting, ($sorting) => {
    const column = $sorting.find((v) => v.id === "published_at");
    if (!column) return "desc";
    return column.desc ? "desc" : "asc";
  });

  const pageSize = 25;

  const debouncedSearch = debounce((value: string) => {
    searchQuery.set(value as string);
    page.set(1); // Reset page when search changes
  }, 300);

  $: query = createQuery({
    queryKey: ["episodes", $searchQuery, $page, $order],
    queryFn: () =>
      getEpisodesApiEpisodesGet({
        query: {
          search: $searchQuery,
          page: $page,
          size: pageSize,
          order: $order ? $order : undefined,
        },
      }),
  });

  $: table = createSvelteTable({
    data: $query?.data?.data?.items ?? [],
    columns,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    manualSorting: true,
    onSortingChange: handleSortingChange,
    state: { sorting: $sorting },
    defaultColumn: {
      size: 300,
      minSize: 150,
    },
  });

  const handleNextPage = () => page.set($page + 1);
  const handlePreviousPage = () => page.set($page - 1);
  const handleSortingChange = (state: Updater<SortingState>) => sorting.set(state as SortingState);
</script>

<div class="2xl:max-w-screen-2xl 2xl:mx-auto">
  <div class="flex justify-between items-center mb-4">
    <div class="relative">
      <Input
        type="search"
        class="min-w-md pl-8"
        placeholder="Cerca un episodi"
        oninput={(e) => debouncedSearch(e.currentTarget.value)}
      />
      <div class="absolute left-0 top-1/2 -translate-y-1/2 pl-2">
        <Search class="w-4 h-4" />
      </div>
    </div>
    <div class="flex items-center gap-2">
      <Button onclick={handlePreviousPage} disabled={$page === 1} variant="ghost" size="sm">
        <ChevronLeft class="w-4 h-4" />
        Anterior
      </Button>
      <Button
        onclick={handleNextPage}
        disabled={$page === $query?.data?.data?.pages}
        variant="ghost"
        size="sm"
      >
        Següent
        <ChevronRight class="w-4 h-4" />
      </Button>
    </div>
  </div>
  <div class="overflow-hidden rounded-md border">
    <Table.Root>
      <Table.Header>
        {#each table.getHeaderGroups() as headerGroup (headerGroup.id)}
          <Table.Row>
            {#each headerGroup.headers as header (header.id)}
              <Table.Head colspan={header.colSpan} style={`width: ${header.getSize()}px`}>
                <DataTableHeader {table} {header} />
              </Table.Head>
            {/each}
          </Table.Row>
        {/each}
      </Table.Header>
      <Table.Body>
        {#each table.getRowModel().rows as row (row.id)}
          <Table.Row data-state={row.getIsSelected() && "selected"}>
            {#each row.getVisibleCells() as cell (cell.id)}
              <Table.Cell style={`width: ${cell.column.getSize()}px`}>
                <FlexRender content={cell.column.columnDef.cell} context={cell.getContext()} />
              </Table.Cell>
            {/each}
          </Table.Row>
        {:else}
          <Table.Row>
            <Table.Cell colspan={columns.length} class="h-24 text-center">
              No s'han trobat resultats.
            </Table.Cell>
          </Table.Row>
        {/each}
      </Table.Body>
    </Table.Root>
  </div>
</div>
