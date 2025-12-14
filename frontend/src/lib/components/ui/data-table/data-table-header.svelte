<script lang="ts" generics="TData, TValue">
  import { ArrowDown, ArrowUp } from "@lucide/svelte";
  import type { Header, Table } from "@tanstack/table-core";

  import { Button } from "lib/components/ui/button";
  import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
  } from "lib/components/ui/dropdown-menu";

  import FlexRender from "./flex-render.svelte";

  let { table, header }: { table: Table<TData>; header: Header<TData, TValue> } = $props();
  const isSorted = $derived(table.getState().sorting.find((s) => s.id === header.column.id));
</script>

<div>
  {#if header.column.getCanSort()}
    <DropdownMenu>
      <DropdownMenuTrigger>
        {#snippet child({ props })}
          <Button {...props} variant="ghost" size="sm" class="flex items-center gap-2">
            {#if header.column.columnDef.meta?.icon}
              {@const Icon = header.column.columnDef.meta.icon}
              <Icon class="shrink-0 size-3.5" />
            {/if}
            <FlexRender content={header.column.columnDef.header} context={header.getContext()} />
            {#if isSorted}
              {#if isSorted.desc}
                <ArrowDown />
              {:else}
                <ArrowUp />
              {/if}
            {/if}
          </Button>
        {/snippet}
      </DropdownMenuTrigger>
      <DropdownMenuContent>
        <DropdownMenuItem onclick={() => table.setSorting([{ id: header.column.id, desc: false }])}>
          <ArrowUp /> Asc
        </DropdownMenuItem>
        <DropdownMenuItem onclick={() => table.setSorting([{ id: header.column.id, desc: true }])}>
          <ArrowDown /> Desc
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  {:else}
    <div class="flex items-center gap-2">
      {#if header.column.columnDef.meta?.icon}
        {@const Icon = header.column.columnDef.meta.icon}
        <Icon class="shrink-0 size-4" />
      {/if}
      <FlexRender content={header.column.columnDef.header} context={header.getContext()} />
    </div>
  {/if}
</div>
