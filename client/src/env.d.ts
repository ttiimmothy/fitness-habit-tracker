/// <reference path="../.astro/types.d.ts" />
/// <reference types="vite/client" />

interface ImportMetaEnv {
  PUBLIC_API_URL: string;
  PUBLIC_GOOGLE_CLIENT_ID: string;
  PUBLIC_OTHER_KEY?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}