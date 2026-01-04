<script lang="ts">
  import { ChevronDownIcon } from "@lucide/svelte";
  import { createVirtualizer } from "@tanstack/svelte-virtual";

  import type { CategoryType } from "client";

  import Button from "lib/components/ui/button/button.svelte";
  import Checkbox from "lib/components/ui/checkbox/checkbox.svelte";
  import {
    Command,
    CommandEmpty,
    CommandInput,
    CommandItem,
    CommandList,
  } from "lib/components/ui/command";
  import { Popover, PopoverContent, PopoverTrigger } from "lib/components/ui/popover";
  import { cn, getCategoryStyles, getCheckboxStyles } from "lib/utils";

  type FilterProps = {
    label: string;
    items: { value: string; label: string }[];
    onSelect: (categories: string[]) => void;
    type: CategoryType;
    selectedCategories?: string[];
  };

  let { label, items, onSelect, type, selectedCategories = [] }: FilterProps = $props();

  let localSelectedCategories = $derived<string[]>(selectedCategories);

  let searchQuery = $state("");
  const filteredItems = $derived(
    searchQuery.trim()
      ? items.filter((item) => item.label.toLowerCase().includes(searchQuery.trim().toLowerCase()))
      : items
  );

  const handleSelect = (value: string) => {
    if (localSelectedCategories.includes(value)) {
      localSelectedCategories.splice(localSelectedCategories.indexOf(value), 1);
    } else {
      localSelectedCategories.push(value);
    }
    onSelect([...localSelectedCategories]);
  };

  let parentRef = $state<HTMLElement | null>(null);
  let shouldVirtualize = $derived(items.length > 50);

  const rowVirtualizer = $derived(
    shouldVirtualize && parentRef
      ? createVirtualizer({
          count: filteredItems.length,
          getScrollElement: () => parentRef,
          estimateSize: () => 32,
          overscan: 5,
        })
      : null
  );

  // Scroll to first item when search query changes
  let prevSearchQuery = $state("");

  $effect(() => {
    // Only scroll if search query actually changed and virtualizer is ready
    if (rowVirtualizer && filteredItems.length > 0 && searchQuery !== prevSearchQuery) {
      prevSearchQuery = searchQuery;

      // Use queueMicrotask to ensure virtualizer is fully initialized after filteredItems update
      queueMicrotask(() => {
        // eslint-disable-next-line
        if (rowVirtualizer && $rowVirtualizer) {
          try {
            $rowVirtualizer.scrollToIndex(0, { align: "start" });
          } catch (e) {
            // Silently fail if virtualizer isn't ready yet
            console.debug("Virtualizer not ready for scrolling", e);
          }
        }
      });
    }
  });
</script>

<Popover>
  <PopoverTrigger>
    {#snippet child({ props })}
      <Button variant="outline" {...props} class="justify-between font-light" role="combobox">
        {label}
        {#if localSelectedCategories.length > 0}
          <span
            class={cn(
              "text-xs rounded-full size-4.5 p-1 flex items-center justify-center",
              getCategoryStyles(type)
            )}
          >
            {localSelectedCategories.length}
          </span>
        {/if}
        <ChevronDownIcon />
      </Button>
    {/snippet}
  </PopoverTrigger>
  <PopoverContent class="w-fit min-w-3xs p-0">
    <Command>
      {#if shouldVirtualize}
        <CommandInput placeholder="Cerca..." bind:value={searchQuery} />
      {:else}
        <CommandInput placeholder="Cerca..." />
      {/if}
      <CommandList bind:ref={parentRef}>
        <CommandEmpty class="py-2">No s'han trobat resultats.</CommandEmpty>
        {#if filteredItems.length > 0}
          {#if shouldVirtualize && rowVirtualizer}
            <!-- Virtualized rendering for large lists -->
            <div class="text-foreground overflow-hidden p-1">
              <div class="relative w-full" style="height: {$rowVirtualizer!.getTotalSize()}px;">
                {#each $rowVirtualizer!.getVirtualItems() as virtualItem (virtualItem.key)}
                  {@const item = filteredItems[virtualItem.index]}
                  <div
                    class="absolute top-0 left-0 w-full"
                    style="height: {virtualItem.size}px; transform: translateY({virtualItem.start}px);"
                  >
                    <CommandItem value={item.label} onSelect={() => handleSelect(item.value)}>
                      <Checkbox
                        id={item.value}
                        class={cn(getCheckboxStyles(type), "[&_svg]:stroke-white [&_svg]:stroke-3")}
                        checked={localSelectedCategories.includes(item.value)}
                      />
                      <span
                        class="text-ellipsis overflow-hidden whitespace-nowrap max-w-xs"
                        title={item.label}
                      >
                        {item.label}
                      </span>
                    </CommandItem>
                  </div>
                {/each}
              </div>
            </div>
          {:else}
            <div class="text-foreground overflow-hidden p-1">
              {#each filteredItems as item (item.value)}
                <CommandItem value={item.label} onSelect={() => handleSelect(item.value)}>
                  <Checkbox
                    id={item.value}
                    class={cn(getCheckboxStyles(type), "[&_svg]:stroke-white [&_svg]:stroke-3")}
                    checked={localSelectedCategories.includes(item.value)}
                  />
                  {item.label}
                </CommandItem>
              {/each}
            </div>
          {/if}
        {/if}
      </CommandList>
    </Command>
  </PopoverContent>
</Popover>
