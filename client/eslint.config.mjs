import eslint from '@eslint/js'
import tseslint from 'typescript-eslint'
import globals from "globals"

export default [
  {
    ignores: ['dist', '.eslintrc.cjs', '**/.astro/**'],
  },

  eslint.configs.recommended,

  // TypeScript: recommended config
  ...tseslint.configs.recommended,

  {
    files: ['**/*.ts', '**/*.cts', '**/*.mts', '**/*.tsx'],
    languageOptions: {
      parser: tseslint.parser,
      parserOptions: {
        ecmaVersion: 2020,
        sourceType: 'module',
      },
      globals: {
        node: true,
        es6: true,
        ...globals.browser,
      }
    },
    rules: {
      '@typescript-eslint/no-explicit-any': 'off',
      '@typescript-eslint/no-unused-vars': 'off',
      '@typescript-eslint/triple-slash-reference': 'off',
    },
  },

  {
    files: [
      '**/*.config.{js,cjs,mjs,ts}',
      'astro.config.mjs',
      'postcss.config.cjs',
      'vite.config.{js,ts,mjs,cjs}',
      'tailwind.config.{js,ts,cjs,mjs}',
    ],
    languageOptions: {
      ecmaVersion: 2020,
      sourceType: 'module',
      globals: {
        ...globals.node,   // defines process, module, __dirname, etc.
      },
    },
    // If some of these are CJS, ESLint handles them fine; if needed,
    // add parserOptions.sourceType per-file.
    rules: {},
  }
]