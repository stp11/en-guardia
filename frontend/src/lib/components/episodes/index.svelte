<script lang="ts">
  import { onMount } from "svelte";

  import { Search } from "@lucide/svelte";
  import { getCoreRowModel } from "@tanstack/table-core";
  import { type Episode, getEpisodesApiEpisodesGet } from "client";

  import { FlexRender, createSvelteTable } from "lib/components/ui/data-table/index.js";
  import Input from "lib/components/ui/input.svelte";
  import * as Table from "lib/components/ui/table/index.js";

  import { columns } from "./columns";

  let episodes: Episode[] = [];

  onMount(async () => {
    const { data } = await getEpisodesApiEpisodesGet();
    episodes = data?.items ?? [];
  });

  $: table = createSvelteTable({
    data: episodes,
    columns,
    getCoreRowModel: getCoreRowModel(),
    defaultColumn: {
      size: 300,
      minSize: 150,
    },
  });
</script>

<div class="relative">
  <Input type="search" class="mb-4 w-1/3 pl-8" placeholder="Cerca un episodi" />
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
