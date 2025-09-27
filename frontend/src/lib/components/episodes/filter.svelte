<script lang="ts">
  import { ChevronDownIcon } from "@lucide/svelte";

  import type { CategoryType } from "client";

  import Button from "lib/components/ui/button/button.svelte";
  import Checkbox from "lib/components/ui/checkbox/checkbox.svelte";
  import {
    Command,
    CommandEmpty,
    CommandGroup,
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

  const handleSelect = (value: string) => {
    if (localSelectedCategories.includes(value)) {
      localSelectedCategories.splice(localSelectedCategories.indexOf(value), 1);
    } else {
      localSelectedCategories.push(value);
    }
    onSelect([...localSelectedCategories]);
  };
</script>

<Popover>
  <PopoverTrigger>
    {#snippet child({ props })}
      <Button variant="outline" {...props} class="justify-between font-normal" role="combobox">
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
  <PopoverContent class="w-[200px] p-0">
    <Command>
      <CommandInput placeholder="Cerca..." />
      <CommandList>
        <CommandEmpty class="py-2">No data found.</CommandEmpty>
        {#if items.length > 0}
          <CommandGroup>
            {#each items as item (item.value)}
              <CommandItem value={item.label} onSelect={() => handleSelect(item.value)}>
                <Checkbox
                  id={item.value}
                  class={cn(getCheckboxStyles(type), "[&_svg]:stroke-white [&_svg]:stroke-3")}
                  checked={localSelectedCategories.includes(item.value)}
                />
                {item.label}
              </CommandItem>
            {/each}
          </CommandGroup>
        {/if}
      </CommandList>
    </Command>
  </PopoverContent>
</Popover>
