import { defineConfig } from 'eslint/config';

export default defineConfig([
  {
    parser: '@typescript-eslint/parser',
    plugins: ['@typescript-eslint'],
    extends: [
      'eslint:recommended',
      'plugin:@typescript-eslint/eslint-recommended',
      'plugin:@typescript-eslint/recommended',
    ],
    rules: {
      '@typescript-eslint/no-namespace': 'off',
    },
    ignorePatterns: ['*.css'],
  },
]);
