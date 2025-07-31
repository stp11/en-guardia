<script lang="ts">
  import { derived, writable } from "svelte/store";

  import { Search } from "@lucide/svelte";
  import { createQuery } from "@tanstack/svelte-query";
  import {
    type PaginationState,
    type RowSelectionState,
    type SortingState,
    type Updater,
    getCoreRowModel,
    getSortedRowModel,
  } from "@tanstack/table-core";

  import { getEpisodesApiEpisodesGet } from "client";

  import { FlexRender, createSvelteTable } from "lib/components/ui/data-table";
  import Input from "lib/components/ui/input.svelte";
  import * as Table from "lib/components/ui/table";
  import { debounce } from "lib/hooks/use-debounce";

  import DataTableHeader from "../ui/data-table/data-table-header.svelte";
  import DataTablePagination from "../ui/data-table/data-table-pagination.svelte";
  import { columns } from "./columns";

  const searchQuery = writable("");
  const page = writable(1);
  const sorting = writable<SortingState>([]);
  const rowSelection = writable<RowSelectionState>({});
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
    manualPagination: true,
    enableRowSelection: true,
    onSortingChange: handleSortingChange,
    onPaginationChange: handlePaginationChange,
    onRowSelectionChange: handleRowSelectionChange,
    pageCount: $query?.data?.data?.pages ?? 0,
    state: {
      sorting: $sorting,
      pagination: { pageIndex: $page - 1, pageSize },
      rowSelection: $rowSelection,
    },
    defaultColumn: {
      size: 300,
      minSize: 150,
    },
  });

  const handlePaginationChange = (pagination: Updater<PaginationState>) => {
    const newPagination =
      typeof pagination === "function" ? pagination(table.getState().pagination) : pagination;
    page.set(newPagination.pageIndex + 1);
  };

  const handleSortingChange = (state: Updater<SortingState>) => {
    const newSorting = typeof state === "function" ? state(table.getState().sorting) : state;
    sorting.set(newSorting as SortingState);
  };

  const handleRowSelectionChange = (state: Updater<RowSelectionState>) => {
    const newRowSelection =
      typeof state === "function" ? state(table.getState().rowSelection) : state;
    rowSelection.set(newRowSelection as RowSelectionState);
  };
</script>

<div class="xl:max-w-screen-xl 2xl:mx-auto">
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
    <DataTablePagination {table} />
  </div>
  <div class="overflow-hidden rounded-md border shadow-xs">
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
          <Table.Row
            data-state={row.getIsSelected() && "selected"}
            onclick={() =>
              handleRowSelectionChange((prev) => ({ ...prev, [row.id]: !row.getIsSelected() }))}
          >
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
