import { createRawSnippet } from "svelte";

import type { ColumnDef } from "@tanstack/table-core";

import type { Episode } from "client";

import { renderSnippet } from "../ui/data-table/render-helpers";

export const columns: ColumnDef<Episode>[] = [
  {
    accessorKey: "title",
    header: "Títol",
    enableSorting: false,
  },
  {
    accessorKey: "description",
    header: "Descripció",
    size: 768,
    enableSorting: false,
    cell: ({ row }) => {
      const descriptionCellSnippet = createRawSnippet(() => ({
        render: () => `<div class="line-clamp-2 pr-8">${row.original.description}</div>`,
      }));
      return renderSnippet(descriptionCellSnippet, row.original.description);
    },
  },
  {
    accessorKey: "published_at",
    header: "Data de publicació",
    size: 150,
    enableSorting: true,
    cell: ({ row }) => {
      if (!row.original.published_at) return null;
      const date = new Intl.DateTimeFormat("ca", {
        year: "numeric",
        month: "long",
        day: "numeric",
      }).format(new Date(row.original.published_at));

      const publishedAtCellSnippet = createRawSnippet(() => ({
        render: () => `<div>${date}</div>`,
      }));
      return renderSnippet(publishedAtCellSnippet, date);
    },
  },
];
