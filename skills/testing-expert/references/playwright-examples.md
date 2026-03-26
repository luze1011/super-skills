# Playwright Examples Reference

Comprehensive collection of Playwright testing patterns and examples.

## Table of Contents

1. [Setup & Configuration](#setup--configuration)
2. [Basic Interactions](#basic-interactions)
3. [Selectors & Locators](#selectors--locators)
4. [Assertions](#assertions)
5. [Page Objects](#page-objects)
6. [Authentication](#authentication)
7. [Network Handling](#network-handling)
8. [Visual Testing](#visual-testing)
9. [Mobile & Responsive](#mobile--responsive)
10. [Performance & Debugging](#performance--debugging)

---

## Setup & Configuration

### Basic Test Setup

```typescript
// playwright.config.ts
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
    video: 'retain-on-failure',
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
  ],

  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

### Test File Structure

```typescript
// tests/example.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Feature name', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should work correctly', async ({ page }) => {
    // Test code here
  });
});
```

---

## Basic Interactions

### Navigation

```typescript
test('navigation examples', async ({ page }) => {
  // Go to URL
  await page.goto('https://example.com');
  
  // Go back
  await page.goBack();
  
  // Go forward
  await page.goForward();
  
  // Reload
  await page.reload();
  
  // Wait for navigation
  await Promise.all([
    page.waitForURL('**/dashboard'),
    page.click('text=Go to Dashboard'),
  ]);
});
```

### Clicking Elements

```typescript
test('clicking examples', async ({ page }) => {
  // Basic click
  await page.click('button');
  
  // Click with text
  await page.click('text=Submit');
  
  // Double click
  await page.dblclick('.item');
  
  // Right click
  await page.click('.context-menu-trigger', { button: 'right' });
  
  // Click with modifiers
  await page.click('a', { modifiers: ['Control'] });
  
  // Force click (skip actionability checks)
  await page.click('.hidden-button', { force: true });
  
  // Click with timeout
  await page.click('button', { timeout: 5000 });
});
```

### Form Inputs

```typescript
test('form input examples', async ({ page }) => {
  // Text input
  await page.fill('input[name="username"]', 'testuser');
  
  // Clear and fill
  await page.fill('input[name="email"]', '');
  await page.fill('input[name="email"]', 'test@example.com');
  
  // Type character by character
  await page.type('input[name="search"]', 'playwright', { delay: 100 });
  
  // Select dropdown option
  await page.selectOption('select#country', 'Canada');
  await page.selectOption('select#colors', ['red', 'green']); // Multi-select
  
  // Checkbox
  await page.check('input[type="checkbox"]');
  await page.uncheck('input[type="checkbox"]');
  
  // Radio button
  await page.check('input[value="option1"]');
  
  // File upload
  await page.setInputFiles('input[type="file"]', 'path/to/file.pdf');
  
  // Multiple files
  await page.setInputFiles('input[type="file"]', ['file1.pdf', 'file2.pdf']);
});
```

### Keyboard & Mouse

```typescript
test('keyboard and mouse examples', async ({ page }) => {
  // Keyboard
  await page.keyboard.press('Enter');
  await page.keyboard.press('Control+A');
  await page.keyboard.type('Hello World');
  
  // Mouse
  await page.mouse.click(100, 200);
  await page.mouse.dblclick(100, 200);
  await page.mouse.move(100, 200);
  await page.mouse.down();
  await page.mouse.move(200, 300);
  await page.mouse.up();
  
  // Hover
  await page.hover('.menu-item');
  
  // Drag and drop
  await page.dragAndDrop('.source', '.target');
});
```

---

## Selectors & Locators

### Basic Selectors

```typescript
test('selector examples', async ({ page }) => {
  // CSS selector
  await page.click('.submit-button');
  await page.click('#login-form button');
  
  // Text selector
  await page.click('text=Welcome');
  await page.click('text=/Welcome/i'); // Regex
  
  // Attribute selector
  await page.click('[data-testid="submit"]');
  
  // Combined selectors
  await page.click('article >> text=Read more');
});
```

### Locators (Recommended)

```typescript
test('locator examples', async ({ page }) => {
  // Get by role (most reliable)
  const button = page.getByRole('button', { name: 'Submit' });
  const link = page.getByRole('link', { name: /dashboard/i });
  const heading = page.getByRole('heading', { name: 'Welcome', level: 1 });
  
  // Get by text
  const text = page.getByText('Welcome');
  const regexText = page.getByText(/welcome/i);
  
  // Get by label (for form inputs)
  const email = page.getByLabel('Email address');
  const password = page.getByLabel('Password');
  
  // Get by placeholder
  const search = page.getByPlaceholder('Search...');
  
  // Get by test id
  const submit = page.getByTestId('submit-button');
  
  // Get by alt text (for images)
  const logo = page.getByAltText('Company Logo');
  
  // Get by title
  const tooltip = page.getByTitle('Close');
  
  // Chain locators
  const menuItem = page.locator('.menu').getByRole('link', { name: 'Home' });
  
  // Filter locators
  const activeButton = page.getByRole('button').filter({ hasText: 'Active' });
});
```

### Locator Operations

```typescript
test('locator operations', async ({ page }) => {
  // Get multiple elements
  const buttons = page.getByRole('button');
  const count = await buttons.count();
  
  // Iterate over elements
  for (const button of await buttons.all()) {
    console.log(await button.textContent());
  }
  
  // Get specific element
  const firstButton = buttons.first();
  const lastButton = buttons.last();
  const nthButton = buttons.nth(2); // 0-indexed
  
  // Get inner locator
  const form = page.locator('form');
  const submitButton = form.getByRole('button');
});
```

---

## Assertions

### Basic Assertions

```typescript
test('assertion examples', async ({ page }) => {
  // Visibility
  await expect(page.locator('.loading')).toBeVisible();
  await expect(page.locator('.hidden')).toBeHidden();
  
  // Text content
  await expect(page.locator('.title')).toHaveText('Welcome');
  await expect(page.locator('.title')).toContainText('Wel');
  await expect(page.locator('.title')).toHaveText(/Welcome/i);
  
  // Value
  await expect(page.locator('input')).toHaveValue('test');
  await expect(page.locator('input')).toBeEmpty();
  
  // Attribute
  await expect(page.locator('a')).toHaveAttribute('href', '/home');
  
  // Class
  await expect(page.locator('button')).toHaveClass(/active/);
  
  // Count
  await expect(page.locator('.item')).toHaveCount(5);
  
  // Enabled/Disabled
  await expect(page.locator('button')).toBeEnabled();
  await expect(page.locator('button')).toBeDisabled();
  
  // Editable
  await expect(page.locator('input')).toBeEditable();
  
  // Focus
  await expect(page.locator('input')).toBeFocused();
  
  // Checked
  await expect(page.locator('input[type="checkbox"]')).toBeChecked();
  
  // URL
  await expect(page).toHaveURL('https://example.com');
  await expect(page).toHaveURL(/example\.com/);
  
  // Title
  await expect(page).toHaveTitle('Page Title');
});
```

### Soft Assertions

```typescript
test('soft assertions', async ({ page }) => {
  // Soft assertions don't stop on failure
  await expect.soft(page.locator('.title')).toHaveText('Welcome');
  await expect.soft(page.locator('.subtitle')).toHaveText('Hello');
  await expect.soft(page.locator('button')).toBeEnabled();
  
  // All assertions will run even if some fail
});
```

### Custom Assertions

```typescript
test('custom assertions', async ({ page }) => {
  const locator = page.locator('.status');
  
  // Custom timeout
  await expect(locator).toBeVisible({ timeout: 10000 });
  
  // Negation
  await expect(locator).not.toBeVisible();
  
  // Custom predicate
  await expect.poll(async () => {
    const text = await locator.textContent();
    return text?.includes('Success');
  }).toBeTruthy();
});
```

---

## Page Objects

### Basic Page Object

```typescript
// pages/LoginPage.ts
import { Locator, Page } from '@playwright/test';

export class LoginPage {
  readonly page: Page;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly loginButton: Locator;
  readonly errorMessage: Locator;

  constructor(page: Page) {
    this.page = page;
    this.emailInput = page.getByLabel('Email');
    this.passwordInput = page.getByLabel('Password');
    this.loginButton = page.getByRole('button', { name: 'Login' });
    this.errorMessage = page.locator('.error-message');
  }

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.loginButton.click();
  }

  async expectError(message: string) {
    await expect(this.errorMessage).toHaveText(message);
  }
}
```

### Using Page Objects

```typescript
// tests/login.spec.ts
import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';

test.describe('Login', () => {
  let loginPage: LoginPage;

  test.beforeEach(async ({ page }) => {
    loginPage = new LoginPage(page);
    await loginPage.goto();
  });

  test('successful login', async ({ page }) => {
    await loginPage.login('user@example.com', 'password');
    await expect(page).toHaveURL('/dashboard');
  });

  test('invalid credentials', async () => {
    await loginPage.login('wrong@example.com', 'wrongpassword');
    await loginPage.expectError('Invalid credentials');
  });
});
```

### Base Page Object

```typescript
// pages/BasePage.ts
import { Locator, Page } from '@playwright/test';

export abstract class BasePage {
  constructor(protected page: Page) {}

  protected locator(selector: string): Locator {
    return this.page.locator(selector);
  }

  protected async waitForNavigation(url: string) {
    await this.page.waitForURL(`**${url}`);
  }

  async takeScreenshot(name: string) {
    await this.page.screenshot({ path: `screenshots/${name}.png` });
  }
}

// pages/HomePage.ts
import { BasePage } from './BasePage';

export class HomePage extends BasePage {
  readonly welcomeMessage = this.locator('.welcome');
  readonly logoutButton = this.locator('button.logout');

  async expectWelcome(name: string) {
    await expect(this.welcomeMessage).toHaveText(`Welcome, ${name}!`);
  }
}
```

---

## Authentication

### Login Once for All Tests

```typescript
// auth.setup.ts
import { test as setup, expect } from '@playwright/test';

const authFile = 'playwright/.auth/user.json';

setup('authenticate', async ({ page }) => {
  await page.goto('/login');
  await page.fill('input[name="email"]', 'test@example.com');
  await page.fill('input[name="password"]', 'password');
  await page.click('button[type="submit"]');
  
  await expect(page).toHaveURL('/dashboard');
  
  // Save authentication state
  await page.context().storageState({ path: authFile });
});

// playwright.config.ts
export default defineConfig({
  projects: [
    { name: 'setup', testMatch: /.*\.setup\.ts/ },
    {
      name: 'chromium',
      use: {
        storageState: 'playwright/.auth/user.json',
      },
      dependencies: ['setup'],
    },
  ],
});
```

### API Authentication

```typescript
test('authenticate via API', async ({ page, request }) => {
  // Login via API
  const response = await request.post('/api/login', {
    data: {
      email: 'test@example.com',
      password: 'password',
    },
  });
  
  const { token } = await response.json();
  
  // Set token in localStorage
  await page.goto('/');
  await page.evaluate((token) => {
    localStorage.setItem('authToken', token);
  }, token);
  
  // Reload to apply auth
  await page.reload();
});
```

### Custom Authentication Fixture

```typescript
// fixtures/auth.ts
import { test as base } from '@playwright/test';

type AuthFixtures = {
  authenticatedPage: Page;
};

export const test = base.extend<AuthFixtures>({
  authenticatedPage: async ({ page }, use) => {
    await page.goto('/login');
    await page.fill('input[name="email"]', 'test@example.com');
    await page.fill('input[name="password"]', 'password');
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL('/dashboard');
    
    await use(page);
  },
});

// Use in tests
test('protected page', async ({ authenticatedPage }) => {
  await authenticatedPage.goto('/profile');
  await expect(authenticatedPage.locator('.user-name')).toBeVisible();
});
```

---

## Network Handling

### Intercept Requests

```typescript
test('intercept requests', async ({ page }) => {
  // Mock API response
  await page.route('**/api/users', async route => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify([
        { id: 1, name: 'Test User' },
      ]),
    });
  });
  
  await page.goto('/users');
  await expect(page.locator('.user-name')).toHaveText('Test User');
});
```

### Modify Requests

```typescript
test('modify requests', async ({ page }) => {
  await page.route('**/api/data', async route => {
    const response = await route.fetch();
    const data = await response.json();
    
    // Modify response
    data.extra = 'added by test';
    
    await route.fulfill({
      status: 200,
      body: JSON.stringify(data),
    });
  });
});
```

### Block Requests

```typescript
test('block requests', async ({ page }) => {
  // Block images
  await page.route('**/*.{png,jpg,jpeg,svg}', route => route.abort());
  
  // Block analytics
  await page.route('**/analytics*', route => route.abort());
  
  // Block third-party
  await page.route('**/third-party.com/**', route => route.abort());
  
  await page.goto('/');
});
```

### Wait for Requests

```typescript
test('wait for requests', async ({ page }) => {
  await page.goto('/');
  
  // Wait for specific request
  const responsePromise = page.waitForResponse('**/api/data');
  await page.click('button.refresh');
  const response = await responsePromise;
  
  // Check response
  expect(response.status()).toBe(200);
  const data = await response.json();
  expect(data).toBeDefined();
});
```

---

## Visual Testing

### Screenshots

```typescript
test('screenshots', async ({ page }) => {
  await page.goto('/');
  
  // Full page screenshot
  await page.screenshot({ path: 'full-page.png' });
  
  // Element screenshot
  await page.locator('.card').screenshot({ path: 'element.png' });
  
  // Full page with full width
  await page.screenshot({
    path: 'full-width.png',
    fullPage: true,
  });
});

test('visual comparison', async ({ page }) => {
  await page.goto('/');
  
  // Compare with baseline
  await expect(page).toHaveScreenshot('homepage.png');
  
  // Element comparison
  await expect(page.locator('.header')).toHaveScreenshot('header.png');
  
  // With threshold
  await expect(page).toHaveScreenshot('homepage.png', {
    maxDiffPixels: 100,
  });
});
```

### Snapshot Testing

```typescript
test('text snapshot', async ({ page }) => {
  await page.goto('/');
  
  // Text content snapshot
  await expect(page.locator('.article')).toMatchAriaSnapshot(`
    - heading "Welcome"
    - paragraph:
      - text: "This is the introduction"
    - list:
      - listitem: "Item 1"
      - listitem: "Item 2"
  `);
});
```

---

## Mobile & Responsive

### Mobile Emulation

```typescript
import { test, expect, devices } from '@playwright/test';

test.use(devices['iPhone 13']);

test('mobile view', async ({ page }) => {
  await page.goto('/');
  
  // Test mobile-specific elements
  await expect(page.locator('.mobile-menu')).toBeVisible();
  
  // Test touch interactions
  await page.tap('.button');
});
```

### Responsive Testing

```typescript
test('responsive design', async ({ page }) => {
  // Desktop
  await page.setViewportSize({ width: 1920, height: 1080 });
  await page.goto('/');
  await expect(page.locator('.desktop-nav')).toBeVisible();
  
  // Tablet
  await page.setViewportSize({ width: 768, height: 1024 });
  await expect(page.locator('.desktop-nav')).toBeHidden();
  await expect(page.locator('.tablet-nav')).toBeVisible();
  
  // Mobile
  await page.setViewportSize({ width: 375, height: 667 });
  await expect(page.locator('.mobile-nav')).toBeVisible();
});
```

---

## Performance & Debugging

### Tracing

```typescript
test('with trace', async ({ page }) => {
  await page.context().tracing.start({ screenshots: true, snapshots: true });
  
  await page.goto('/');
  await page.click('button');
  
  await page.context().tracing.stop({ path: 'trace.zip' });
});

// View trace: npx playwright show-trace trace.zip
```

### Debugging

```typescript
test('debug with page.pause', async ({ page }) => {
  await page.goto('/');
  
  // Opens Playwright Inspector
  await page.pause();
  
  await page.click('button');
});
```

### Console & Errors

```typescript
test('capture console', async ({ page }) => {
  const messages: string[] = [];
  page.on('console', msg => {
    messages.push(`${msg.type()}: ${msg.text()}`);
  });
  
  const errors: string[] = [];
  page.on('pageerror', error => {
    errors.push(error.message);
  });
  
  await page.goto('/');
  
  expect(errors).toHaveLength(0);
  console.log('Console messages:', messages);
});
```

### Performance Metrics

```typescript
test('performance', async ({ page }) => {
  await page.goto('/');
  
  // Get performance metrics
  const timing = await page.evaluate(() => {
    const perf = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;
    return {
      loadTime: perf.loadEventEnd - perf.startTime,
      domContentLoaded: perf.domContentLoadedEventEnd - perf.startTime,
    };
  });
  
  console.log('Load time:', timing.loadTime, 'ms');
  expect(timing.loadTime).toBeLessThan(3000);
});
```