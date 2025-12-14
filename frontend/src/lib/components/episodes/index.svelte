<script lang="ts">
  import { derived, writable } from "svelte/store";

  import { LoaderCircleIcon, Search, Trash2Icon } from "@lucide/svelte";
  import { createInfiniteQuery, createQuery } from "@tanstack/svelte-query";
  import {
    type PaginationState,
    type RowSelectionState,
    type SortingState,
    type Updater,
    getCoreRowModel,
    getSortedRowModel,
  } from "@tanstack/table-core";

  import {
    type Category,
    type CategoryType,
    getCategoriesApiCategoriesGet,
    getEpisodesApiEpisodesGet,
  } from "client";

  import AppHero from "lib/components/app-hero.svelte";
  import { Button } from "lib/components/ui/button";
  import { FlexRender, createSvelteTable } from "lib/components/ui/data-table";
  import DataTableHeader from "lib/components/ui/data-table/data-table-header.svelte";
  import DataTablePagination from "lib/components/ui/data-table/data-table-pagination.svelte";
  import Input from "lib/components/ui/input.svelte";
  import * as Table from "lib/components/ui/table";
  import { debounce } from "lib/hooks/use-debounce";

  import { columns } from "./columns";
  import Filter from "./filter.svelte";

  const searchQuery = writable("");
  const page = writable(1);
  const pageSize = writable(20);
  const categories = writable<Record<CategoryType, string[]>>({
    topic: [],
    character: [],
    location: [],
    time_period: [],
  });
  const sorting = writable<SortingState>([]);
  const rowSelection = writable<RowSelectionState>({});
  const order = derived(sorting, ($sorting) => {
    const column = $sorting.find((v) => v.id === "published_at");
    if (!column) return "desc";
    return column.desc ? "desc" : "asc";
  });

  const debouncedSearch = debounce((value: string) => {
    searchQuery.set(value as string);
    page.set(1); // Reset page when search changes
  }, 300);

  $: query = createQuery({
    queryKey: ["episodes", $searchQuery, $page, $pageSize, $order, $categories],
    queryFn: () =>
      getEpisodesApiEpisodesGet({
        query: {
          search: $searchQuery,
          page: $page,
          size: $pageSize,
          order: $order ? $order : undefined,
          categories: Object.values($categories).flat().join(","),
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
    pageCount: $query?.data?.data?.pages ?? 0,
    state: {
      sorting: $sorting,
      pagination: { pageIndex: $page - 1, pageSize: $pageSize },
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
    pageSize.set(newPagination.pageSize);
  };

  const handleSortingChange = (state: Updater<SortingState>) => {
    const newSorting = typeof state === "function" ? state(table.getState().sorting) : state;
    sorting.set(newSorting as SortingState);
  };

  const handleCategoriesChange = (type: CategoryType, newCategories: string[]) => {
    categories.update((prev) => ({
      ...prev,
      [type]: newCategories,
    }));
    page.set(1);
  };

  const clearCategories = () => {
    categories.set({ topic: [], character: [], location: [], time_period: [] });
    page.set(1);
  };

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const getNextPageParam = (lastPage: any) => {
    const data = lastPage.data;
    if (data.page && data.pages && data.page < data.pages) {
      return data.page + 1;
    }
    return undefined;
  };

  const locationsQuery = createInfiniteQuery({
    queryKey: ["locations"],
    queryFn: ({ pageParam }) =>
      getCategoriesApiCategoriesGet({ query: { type: "location", page: pageParam } }),
    getNextPageParam,
    initialPageParam: 1,
  });

  const topicsQuery = createInfiniteQuery({
    queryKey: ["topics"],
    queryFn: ({ pageParam }) =>
      getCategoriesApiCategoriesGet({ query: { type: "topic", page: pageParam } }),
    getNextPageParam,
    initialPageParam: 1,
  });

  const charactersQuery = createInfiniteQuery({
    queryKey: ["characters"],
    queryFn: ({ pageParam }) =>
      getCategoriesApiCategoriesGet({ query: { type: "character", page: pageParam } }),
    getNextPageParam,
    initialPageParam: 1,
  });

  const timePeriodsQuery = createInfiniteQuery({
    queryKey: ["timePeriods"],
    queryFn: ({ pageParam }) =>
      getCategoriesApiCategoriesGet({ query: { type: "time_period", page: pageParam } }),
    getNextPageParam,
    initialPageParam: 1,
  });

  const mapCategoriesDataToOptions = (category: Category[]) => {
    return category.map(({ id, name }) => ({ value: String(id), label: name }));
  };

  const locations = derived(
    locationsQuery,
    ($locationsQuery) =>
      $locationsQuery?.data?.pages.flatMap((page) =>
        mapCategoriesDataToOptions(page?.data?.items ?? [])
      ) ?? []
  );

  const topics = derived(
    topicsQuery,
    ($topicsQuery) =>
      $topicsQuery?.data?.pages.flatMap((page) =>
        mapCategoriesDataToOptions(page?.data?.items ?? [])
      ) ?? []
  );

  const characters = derived(
    charactersQuery,
    ($charactersQuery) =>
      $charactersQuery?.data?.pages.flatMap((page) =>
        mapCategoriesDataToOptions(page?.data?.items ?? [])
      ) ?? []
  );

  const timePeriods = derived(
    timePeriodsQuery,
    ($timePeriodsQuery) =>
      $timePeriodsQuery?.data?.pages.flatMap((page) =>
        mapCategoriesDataToOptions(page?.data?.items ?? [])
      ) ?? []
  );

  // Auto-fetch all pages when query loads
  $: if (
    $locationsQuery.data &&
    $locationsQuery.hasNextPage &&
    !$locationsQuery.isFetchingNextPage
  ) {
    $locationsQuery.fetchNextPage();
  }

  $: if ($topicsQuery.data && $topicsQuery.hasNextPage && !$topicsQuery.isFetchingNextPage) {
    $topicsQuery.fetchNextPage();
  }

  $: if (
    $charactersQuery.data &&
    $charactersQuery.hasNextPage &&
    !$charactersQuery.isFetchingNextPage
  ) {
    $charactersQuery.fetchNextPage();
  }

  $: if (
    $timePeriodsQuery.data &&
    $timePeriodsQuery.hasNextPage &&
    !$timePeriodsQuery.isFetchingNextPage
  ) {
    $timePeriodsQuery.fetchNextPage();
  }

  $: hasCategories = Object.values($categories).some((categories) => categories.length > 0);
</script>

<div class="xl:max-w-screen-xl 2xl:mx-auto">
  <AppHero />
  <div class="flex justify-between items-center mb-4">
    <div class="flex gap-2">
      <div class="relative">
        <Input
          type="search"
          class="w-xs pl-8"
          placeholder="Cerca un episodi"
          oninput={(e) => debouncedSearch(e.currentTarget.value)}
        />
        <div class="absolute left-0 top-1/2 -translate-y-1/2 pl-2">
          <Search class="w-4 h-4" />
        </div>
      </div>
      <Filter
        label="Temàtica"
        type="topic"
        items={$topics}
        selectedCategories={$categories.topic}
        onSelect={(newCategories) => handleCategoriesChange("topic", newCategories)}
      />
      <Filter
        label="Personatge"
        type="character"
        items={$characters}
        selectedCategories={$categories.character}
        onSelect={(newCategories) => handleCategoriesChange("character", newCategories)}
      />
      <Filter
        label="Localització"
        type="location"
        items={$locations}
        selectedCategories={$categories.location}
        onSelect={(newCategories) => handleCategoriesChange("location", newCategories)}
      />
      <Filter
        label="Època"
        type="time_period"
        items={$timePeriods}
        selectedCategories={$categories.time_period}
        onSelect={(newCategories) => handleCategoriesChange("time_period", newCategories)}
      />
      {#if hasCategories}
        <Button variant="ghost" onclick={clearCategories}>
          <Trash2Icon />
          Neteja filtres
        </Button>
      {/if}
    </div>
  </div>
  <div class="overflow-hidden rounded-md border shadow-xs mb-5">
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
        {#if $query?.isLoading}
          <Table.Row>
            <Table.Cell colspan={columns.length} class="h-24 text-center">
              <LoaderCircleIcon class="animate-spin text-accent-foreground/30 w-full" />
            </Table.Cell>
          </Table.Row>
        {:else}
          {#each table.getRowModel().rows as row (row.id)}
            <Table.Row data-state={row.getIsSelected() && "selected"} class="relative">
              {#each row.getVisibleCells() as cell (cell.id)}
                <Table.Cell style={`width: ${cell.column.getSize()}px`}>
                  <FlexRender content={cell.column.columnDef.cell} context={cell.getContext()} />
                </Table.Cell>
              {/each}
              <Table.Cell>
                <a
                  href={`/episodis/${row.original.id}/${row.original.slug}`}
                  aria-label="Ves a l'episodi"
                  class="absolute top-0 left-0 w-full h-full"
                >
                  <span class="sr-only">Ves a l'episodi</span>
                </a>
              </Table.Cell>
            </Table.Row>
          {:else}
            <Table.Row>
              <Table.Cell colspan={columns.length} class="h-24 text-center">
                No s'han trobat resultats.
              </Table.Cell>
            </Table.Row>
          {/each}
        {/if}
      </Table.Body>
    </Table.Root>
  </div>
  <DataTablePagination {table} />
</div>
