/// <reference path="../.astro/types.d.ts" />
/// <reference types="vite/client" />

interface ImportMetaEnv {
  PUBLIC_VITE_API_URL: string;
  PUBLIC_OTHER_KEY?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}