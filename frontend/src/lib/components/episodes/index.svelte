<script lang="ts">
  import { writable } from "svelte/store";

  import { Search } from "@lucide/svelte";
  import { createQuery } from "@tanstack/svelte-query";
  import { getCoreRowModel } from "@tanstack/table-core";
  import { getEpisodesApiEpisodesGet } from "client";

  import { FlexRender, createSvelteTable } from "lib/components/ui/data-table/index.js";
  import Input from "lib/components/ui/input.svelte";
  import * as Table from "lib/components/ui/table/index.js";
  import { debounce } from "lib/hooks/use-debounce";

  import { columns } from "./columns";

  const searchQuery = writable("");

  const debouncedSearch = debounce((value: string) => {
    searchQuery.set(value as string);
  }, 300);

  $: query = createQuery({
    queryKey: ["episodes", $searchQuery],
    queryFn: async () =>
      await getEpisodesApiEpisodesGet({
        query: {
          search: $searchQuery,
        },
      }),
  });

  $: table = createSvelteTable({
    data: $query?.data?.data?.items ?? [],
    columns,
    getCoreRowModel: getCoreRowModel(),
    defaultColumn: {
      size: 300,
      minSize: 150,
    },
  });
</script>

<div class="relative">
  <Input
    type="search"
    class="mb-4 w-1/3 pl-8"
    placeholder="Cerca un episodi"
    oninput={(e) => debouncedSearch(e.currentTarget.value)}
  />
  <div class="absolute left-0 top-1/2 -translate-y-1/2 pl-2">
    <Search class="w-4 h-4" />
  </div>
</div>
<div class="overflow-hidden rounded-md border">
  <Table.Root>
    <Table.Header>
      {#each table.getHeaderGroups() as headerGroup (headerGroup.id)}
        <Table.Row>
          {#each headerGroup.headers as header (header.id)}
            <Table.Head colspan={header.colSpan} style={`width: ${header.getSize()}px`}>
              {#if !header.isPlaceholder}
                <FlexRender
                  content={header.column.columnDef.header}
                  context={header.getContext()}
                />
              {/if}
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
