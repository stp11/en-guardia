import { createRawSnippet } from "svelte";

import type { ColumnDef } from "@tanstack/table-core";

import type { Episode } from "client";

import { renderSnippet } from "../ui/data-table/render-helpers";

export const columns: ColumnDef<Episode>[] = [
  {
    accessorKey: "title",
    header: "Títol",
    enableSorting: false,
    cell: ({ row }) => {
      const titleCellSnippet = createRawSnippet(() => ({
        render: () => `<div class="font-normal">${row.original.title}</div>`,
      }));
      return renderSnippet(titleCellSnippet, row.original.title);
    },
  },
  {
    accessorKey: "description",
    header: "Descripció",
    size: 768,
    enableSorting: false,
    cell: ({ row }) => {
      const descriptionCellSnippet = createRawSnippet(() => ({
        render: () =>
          `<div class="pr-8 ${!row.getIsSelected() && "line-clamp-2"}">${row.original.description ?? "No disponible"}</div>`,
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
        month: "short",
        day: "numeric",
      }).format(new Date(row.original.published_at));

      const publishedAtCellSnippet = createRawSnippet(() => ({
        render: () => `<div class="pr-2.5 text-right">${date}</div>`,
      }));
      return renderSnippet(publishedAtCellSnippet, date);
    },
  },
];
