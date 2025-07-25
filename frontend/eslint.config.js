// eslint.config.js
// @ts-check
import js from "@eslint/js";
import prettier from "eslint-config-prettier";
import svelte from "eslint-plugin-svelte";
import globals from "globals";
import tseslint from "typescript-eslint";

import svelteConfig from "./svelte.config.js";

export default [
  // 1. Global ignores
  {
    ignores: ["build/", ".svelte-kit/", "dist/", "**/*.css", "src/client/**"],
  },

  js.configs.recommended,
  ...tseslint.configs.recommended,
  ...svelte.configs.recommended,

  // // 4. Svelte configuration for .svelte files
  // ...svelte.configs["flat/recommended"],
  // ...svelte.configs["flat/typescript"],
  {
    languageOptions: {
      globals: {
        ...globals.browser,
      },
    },
  },
  {
    files: ["**/*.svelte", "**/*.svelte.ts", "**/*.svelte.js"],
    languageOptions: {
      parserOptions: {
        projectService: true,
        extraFileExtensions: [".svelte"], // Add support for additional file extensions, such as .svelte
        parser: tseslint.parser,
        // We recommend importing and specifying svelte.config.js.
        // By doing so, some rules in eslint-plugin-svelte will automatically read the configuration and adjust their behavior accordingly.
        // While certain Svelte settings may be statically loaded from svelte.config.js even if you don’t specify it,
        // explicitly specifying it ensures better compatibility and functionality.
        svelteConfig,
      },
    },
  },

  // 5. Prettier configuration to disable formatting rules.
  // THIS MUST BE THE LAST ONE IN THE ARRAY.
  prettier,

  // 6. Your custom rule overrides
  {
    rules: {
      "@typescript-eslint/no-namespace": "off",
      // You can add more Svelte or TS rule overrides here
    },
  },
];
