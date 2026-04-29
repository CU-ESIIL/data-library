import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  use: {
    baseURL: 'http://localhost:8000',
    headless: true
  },
  webServer: {
    command: 'python3 -m http.server 8000 --directory site',
    url: 'http://localhost:8000',
    reuseExistingServer: true,
    timeout: 30_000
  }
});
