# Playwright Comprehensive Guide

## Installation

```bash
npm init playwright@latest
# or
npm install @playwright/test
npx playwright install
```

## Configuration

### playwright.config.ts

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'on-first-retry',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
  ],
  webServer: {
    command: 'npm run start',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

## Basic Tests

### Page Navigation

```typescript
import { test, expect } from '@playwright/test';

test('navigate to page', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveTitle(/Home/);
});

test('click link', async ({ page }) => {
  await page.goto('/');
  await page.click('text=About');
  await expect(page).toHaveURL(/about/);
});
```

### Locators

```typescript
// Text content
await page.locator('text=Login').click();

// CSS selector
await page.locator('#username').fill('user');

// Role-based (recommended for accessibility)
await page.getByRole('button', { name: 'Submit' }).click();
await page.getByRole('textbox', { name: 'Email' }).fill('test@example.com');

// Label
await page.getByLabel('Password').fill('secret');

// Placeholder
await page.getByPlaceholder('Enter email').fill('test@example.com');

// Test ID
await page.getByTestId('submit-button').click();

// Chain locators
await page.locator('.card').filter({ hasText: 'Product' }).getByRole('button').click();
```

### Assertions

```typescript
// Visibility
await expect(page.locator('.alert')).toBeVisible();
await expect(page.locator('.hidden')).toBeHidden();

// Text content
await expect(page.locator('.title')).toHaveText('Welcome');
await expect(page.locator('.title')).toContainText('Welcome');

// Value
await expect(page.locator('#email')).toHaveValue('test@example.com');

// URL
await expect(page).toHaveURL('/dashboard');
await expect(page).toHaveURL(/dashboard/);

// Count
await expect(page.locator('.item')).toHaveCount(5);

// Attribute
await expect(page.locator('#link')).toHaveAttribute('href', '/about');

// CSS classes
await expect(page.locator('.btn')).toHaveClass(/active/);

// Screenshot comparison
await expect(page).toHaveScreenshot('homepage.png');
```

## Interactions

### Form Inputs

```typescript
test('fill form', async ({ page }) => {
  await page.goto('/register');
  
  // Text input
  await page.getByLabel('Name').fill('John Doe');
  
  // Email input
  await page.getByLabel('Email').fill('john@example.com');
  
  // Password input
  await page.getByLabel('Password').fill('secret123');
  
  // Select dropdown
  await page.getByLabel('Country').selectOption('US');
  
  // Checkbox
  await page.getByLabel('I agree').check();
  await expect(page.getByLabel('I agree')).toBeChecked();
  
  // Radio button
  await page.getByLabel('Option A').check();
  
  // File upload
  await page.getByLabel('Avatar').setInputFiles('path/to/file.jpg');
  
  // Submit
  await page.getByRole('button', { name: 'Register' }).click();
});
```

### Keyboard & Mouse

```typescript
// Keyboard
await page.keyboard.press('Enter');
await page.keyboard.type('Hello World');
await page.keyboard.down('Shift');
await page.keyboard.press('KeyA');
await page.keyboard.up('Shift');

// Mouse
await page.mouse.click(100, 200);
await page.mouse.dblclick(100, 200);
await page.mouse.move(100, 200);
await page.mouse.down();
await page.mouse.up();

// Drag and drop
await page.locator('.source').dragTo(page.locator('.target'));

// Hover
await page.locator('.menu-item').hover();

// Focus
await page.locator('#input').focus();
```

### Waiting

```typescript
// Wait for selector
await page.waitForSelector('.loaded');

// Wait for URL
await page.waitForURL('/dashboard');

// Wait for request
await page.waitForRequest('/api/data');

// Wait for response
const response = await page.waitForResponse('/api/users');
const data = await response.json();

// Wait for function
await page.waitForFunction(() => document.readyState === 'complete');

// Auto-waiting (built-in)
await page.click('button'); // Waits for element to be clickable
```

## API Testing

```typescript
test('GET request', async ({ request }) => {
  const response = await request.get('/api/users');
  expect(response.ok()).toBeTruthy();
  
  const users = await response.json();
  expect(users).toBeInstanceOf(Array);
});

test('POST request', async ({ request }) => {
  const response = await request.post('/api/users', {
    data: {
      name: 'John',
      email: 'john@example.com',
    },
  });
  
  expect(response.status()).toBe(201);
  const user = await response.json();
  expect(user.name).toBe('John');
});

test('PUT request', async ({ request }) => {
  const response = await request.put('/api/users/1', {
    data: { name: 'Updated' },
  });
  expect(response.ok()).toBeTruthy();
});

test('DELETE request', async ({ request }) => {
  const response = await request.delete('/api/users/1');
  expect(response.status()).toBe(204);
});

test('with headers', async ({ request }) => {
  const response = await request.get('/api/protected', {
    headers: {
      'Authorization': 'Bearer token123',
    },
  });
  expect(response.ok()).toBeTruthy();
});
```

## Page Object Model

```typescript
// pages/LoginPage.ts
import { Page, Locator } from '@playwright/test';

export class LoginPage {
  readonly page: Page;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;
  readonly errorMessage: Locator;

  constructor(page: Page) {
    this.page = page;
    this.emailInput = page.getByLabel('Email');
    this.passwordInput = page.getByLabel('Password');
    this.submitButton = page.getByRole('button', { name: 'Sign In' });
    this.errorMessage = page.locator('.error-message');
  }

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }

  async getError() {
    return this.errorMessage.textContent();
  }
}
```

```typescript
// tests/login.spec.ts
import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';

test('login success', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.goto();
  await loginPage.login('user@test.com', 'password');
  await expect(page).toHaveURL('/dashboard');
});
```

## Fixtures

```typescript
// fixtures.ts
import { test as base } from '@playwright/test';
import { LoginPage } from './pages/LoginPage';

type MyFixtures = {
  loginPage: LoginPage;
  authenticatedPage: Page;
};

export const test = base.extend<MyFixtures>({
  loginPage: async ({ page }, use) => {
    await use(new LoginPage(page));
  },
  
  authenticatedPage: async ({ page }, use) => {
    // Login before test
    await page.goto('/login');
    await page.getByLabel('Email').fill('test@example.com');
    await page.getByLabel('Password').fill('password');
    await page.getByRole('button', { name: 'Sign In' }).click();
    await page.waitForURL('/dashboard');
    
    await use(page);
  },
});
```

```typescript
// Using custom fixtures
import { test, expect } from './fixtures';

test('protected page', async ({ authenticatedPage }) => {
  await authenticatedPage.goto('/profile');
  await expect(authenticatedPage.getByText('Welcome')).toBeVisible();
});
```

## Visual Testing

```typescript
test('visual regression', async ({ page }) => {
  await page.goto('/dashboard');
  
  // Full page
  await expect(page).toHaveScreenshot('dashboard.png');
  
  // Element
  await expect(page.locator('.chart')).toHaveScreenshot('chart.png');
  
  // With options
  await expect(page).toHaveScreenshot('dashboard.png', {
    maxDiffPixels: 100,
    threshold: 0.2,
  });
});
```

## Network Mocking

```typescript
test('mock API response', async ({ page }) => {
  await page.route('/api/users', async route => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify([
        { id: 1, name: 'Mock User' },
      ]),
    });
  });
  
  await page.goto('/users');
  await expect(page.getByText('Mock User')).toBeVisible();
});

test('intercept request', async ({ page }) => {
  await page.route('/api/**', route => {
    if (route.request().method() === 'POST') {
      console.log('POST request intercepted');
    }
    route.continue();
  });
});

test('abort request', async ({ page }) => {
  await page.route('**/analytics.js', route => route.abort());
});
```

## Best Practices

1. **Use role-based locators**
   ```typescript
   // Good: resilient to UI changes
   await page.getByRole('button', { name: 'Submit' }).click();
   
   // Bad: fragile CSS selectors
   await page.locator('#submit-btn-123').click();
   ```

2. **Use auto-waiting assertions**
   ```typescript
   // Good: auto-waits
   await expect(page.locator('.loading')).toBeHidden();
   
   // Bad: manual waits
   await page.waitForTimeout(5000);
   ```

3. **Use Page Object Model**
   ```typescript
   const loginPage = new LoginPage(page);
   await loginPage.login(email, password);
   ```

4. **Parallelize tests**
   ```typescript
   // In config
   workers: 4,
   fullyParallel: true,
   ```

5. **Use test hooks appropriately**
   ```typescript
   test.describe('User management', () => {
     test.beforeEach(async ({ page }) => {
       await page.goto('/login');
     });
     
     test.afterEach(async ({ page }) => {
       await page.click('text=Logout');
     });
   });
   ```