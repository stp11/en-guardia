<script lang="ts" generics="TData, TValue">
  import { ChevronDown, ChevronUp } from "@lucide/svelte";
  import type { Header, Table } from "@tanstack/table-core";

  import { cn } from "lib/utils";

  import FlexRender from "./flex-render.svelte";

  let { table, header }: { table: Table<TData>; header: Header<TData, TValue> } = $props();

  const isSorted = $derived(header.column.getIsSorted());
</script>

<div>
  {#if header.column.getCanSort()}
    <button
      class="flex items-center gap-2"
      onclick={() => table.setSorting([{ id: header.column.id, desc: isSorted === "asc" }])}
    >
      <FlexRender content={header.column.columnDef.header} context={header.getContext()} />
      <div class="flex flex-col">
        <ChevronUp class={cn("!size-3", isSorted === "desc" && "opacity-30")} />
        <ChevronDown class={cn("!size-3", isSorted === "asc" && "opacity-30")} />
      </div>
    </button>
  {:else}
    <FlexRender content={header.column.columnDef.header} context={header.getContext()} />
  {/if}
</div>
