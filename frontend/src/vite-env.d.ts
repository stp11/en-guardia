/// <reference types="vite/client" />
import type { Component } from "svelte";

declare module "@tanstack/table-core" {
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  interface ColumnMeta<TData, TValue> {
    icon?: Component;
  }
}
