import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

import type { CategoryType } from "client";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export type WithElementRef<T, U extends HTMLElement = HTMLElement> = T & { ref?: U | null };

export const capitalize = (str: string) => {
  return str.charAt(0).toUpperCase() + str.slice(1);
};

export const getCategoryStyles = (category: CategoryType | null) => {
  if (!category) return "";
  switch (category) {
    case "topic":
      return "bg-primary-violet/10 text-primary-violet";
    case "location":
      return "bg-primary-yellow/10 text-primary-yellow";
    case "character":
      return "bg-primary-orange/10 text-primary-orange";
    case "time_period":
      return "bg-primary-brown/10 text-primary-brown";
  }
};
