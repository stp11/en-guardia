<script lang="ts" generics="TData, TValue">
  import { ArrowDown, ArrowUp, ChevronsUpDown } from "@lucide/svelte";
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
</script>

<div>
  {#if header.column.getCanSort()}
    <DropdownMenu>
      <DropdownMenuTrigger>
        <Button variant="ghost" size="sm" class="flex items-center gap-1">
          <FlexRender content={header.column.columnDef.header} context={header.getContext()} />
          <ChevronsUpDown class="size-4" />
        </Button>
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
    <FlexRender content={header.column.columnDef.header} context={header.getContext()} />
  {/if}
</div>
