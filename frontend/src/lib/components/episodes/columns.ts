import { createRawSnippet } from "svelte";

import type { ColumnDef } from "@tanstack/table-core";
import type { Episode } from "client";

import { renderSnippet } from "../ui/data-table/render-helpers";

export const columns: ColumnDef<Episode>[] = [
  {
    accessorKey: "title",
    header: "Títol",
  },
  {
    accessorKey: "description",
    header: "Descripció",
    size: 200,
    cell: ({ row }) => {
      const descriptionCellSnippet = createRawSnippet(() => ({
        render: () => `<div>${row.original.description}</div>`,
      }));
      return renderSnippet(descriptionCellSnippet, row.original.description);
    },
  },
  {
    accessorKey: "published_at",
    header: "Data de publicació",
  },
];
