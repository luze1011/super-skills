# Super Testing - 全栈测试技能

> 一个统一的测试技能，覆盖 Python 测试、Web 自动化测试、测试策略设计和 E2E 测试框架。

---

## 📋 目录

1. [快速决策指南](#快速决策指南)
2. [Python 测试模式](#python-测试模式-pytest)
3. [Web 应用测试](#web-应用测试-playwright)
4. [测试策略设计](#测试策略设计)
5. [E2E 测试框架](#e2e-测试框架-vitest--midscene)
6. [常用命令速查表](#常用命令速查表)
7. [最佳实践](#最佳实践)

---

## 🎯 快速决策指南

```
需要测试什么？
├── 纯 Python 代码逻辑？
│   └── pytest + mock + coverage
│
├── Web 应用 UI 自动化？
│   ├── 需要跨浏览器？ → Playwright
│   └── 需要 AI 辅助定位？ → Vitest + Midscene
│
├── API 接口测试？
│   └── pytest + requests + responses
│
└── 完整 E2E 流程？
    ├── 传统方式 → Playwright
    └── 自然语言用例 → Vitest + Midscene
```

### 测试类型选择

| 测试类型 | 推荐工具 | 执行速度 | 维护成本 |
|---------|---------|---------|---------|
| 单元测试 | pytest | ⚡⚡⚡ 极快 | 💰 低 |
| 集成测试 | pytest + fixtures | ⚡⚡ 快 | 💰💰 中 |
| API 测试 | pytest + requests | ⚡⚡ 快 | 💰💰 中 |
| E2E 测试 | Playwright / Midscene | ⚡ 较慢 | 💰💰💰 高 |

---

## 🐍 Python 测试模式 (pytest)

### 基础测试结构

```python
# test_example.py

def test_basic_assertion():
    """最简单的测试"""
    assert 1 + 1 == 2

def test_string_operations():
    """字符串操作测试"""
    text = "hello"
    assert text.upper() == "HELLO"
    assert "ll" in text

class TestCalculator:
    """使用类组织相关测试"""
    
    def test_add(self):
        assert 2 + 3 == 5
    
    def test_subtract(self):
        assert 5 - 3 == 2
    
    def test_multiply(self):
        assert 4 * 3 == 12
```

**运行命令**：
```bash
# 运行所有测试
pytest

# 运行指定文件
pytest test_example.py

# 运行指定类
pytest test_example.py::TestCalculator

# 运行指定测试方法
pytest test_example.py::TestCalculator::test_add

# 显示详细输出
pytest -v

# 显示打印输出
pytest -s
```

---

### Fixtures 依赖注入

```python
# conftest.py - 共享 fixtures
import pytest
from database import Database
from app import create_app

@pytest.fixture
def db():
    """数据库 fixture"""
    database = Database(":memory:")
    database.create_tables()
    yield database
    database.close()

@pytest.fixture
def app():
    """Flask 应用 fixture"""
    app = create_app(testing=True)
    yield app

@pytest.fixture
def client(app):
    """测试客户端 fixture"""
    return app.test_client()

@pytest.fixture
def sample_user(db):
    """示例用户 fixture"""
    user = db.create_user(
        username="testuser",
        email="test@example.com"
    )
    yield user
    db.delete_user(user.id)

# test_user.py
def test_user_creation(sample_user):
    """测试用户创建"""
    assert sample_user.username == "testuser"
    assert sample_user.email == "test@example.com"

def test_user_update(db, sample_user):
    """测试用户更新"""
    db.update_user(sample_user.id, username="newname")
    updated = db.get_user(sample_user.id)
    assert updated.username == "newname"
```

**Fixture 作用域**：
```python
@pytest.fixture(scope="function")  # 每个测试函数执行一次（默认）
def func_scope():
    pass

@pytest.fixture(scope="class")  # 每个测试类执行一次
def class_scope():
    pass

@pytest.fixture(scope="module")  # 每个模块执行一次
def module_scope():
    pass

@pytest.fixture(scope="session")  # 整个测试会话执行一次
def session_scope():
    pass
```

---

### 参数化测试

```python
import pytest

# 单参数化
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
    (10, 20),
])
def test_double(input, expected):
    assert input * 2 == expected

# 多参数化
@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (5, 5, 10),
    (-1, 1, 0),
])
def test_add(a, b, expected):
    assert a + b == expected

# 嵌套参数化
@pytest.mark.parametrize("x", [1, 2])
@pytest.mark.parametrize("y", [10, 20])
def test_multiply(x, y):
    assert x * y in [10, 20, 40]

# 参数化 + ID
@pytest.mark.parametrize(
    "input,expected",
    [
        pytest.param("hello", "HELLO", id="lowercase"),
        pytest.param("HELLO", "HELLO", id="uppercase"),
        pytest.param("HeLLo", "HELLO", id="mixed"),
    ]
)
def test_upper(input, expected):
    assert input.upper() == expected
```

---

### Mock 和 Patch

```python
import pytest
from unittest.mock import Mock, patch, MagicMock, call
from myapp import ExternalService, UserService

# 使用 Mock 对象
def test_mock_basic():
    mock = Mock()
    mock.method.return_value = 42
    assert mock.method() == 42
    mock.method.assert_called_once()

# 使用 patch 装饰器
@patch('myapp.requests.get')
def test_with_patch_decorator(mock_get):
    mock_get.return_value.json.return_value = {"data": "test"}
    service = ExternalService()
    result = service.fetch_data()
    assert result == {"data": "test"}
    mock_get.assert_called_once_with("https://api.example.com/data")

# 使用 patch 上下文管理器
def test_with_patch_context():
    with patch('myapp.Database') as MockDB:
        mock_db = MockDB.return_value
        mock_db.query.return_value = [{"id": 1}]
        
        service = UserService(mock_db)
        users = service.get_users()
        
        assert users == [{"id": 1}]
        mock_db.query.assert_called_once()

# 部分对象 Mock
class TestPartialMock:
    @patch.object(ExternalService, 'fetch_data')
    def test_partial_mock(self, mock_fetch):
        mock_fetch.return_value = {"mocked": True}
        service = ExternalService()
        assert service.fetch_data() == {"mocked": True}

# 验证调用
def test_call_verification():
    mock = Mock()
    mock.method(1, 2, key="value")
    
    mock.method.assert_called_with(1, 2, key="value")
    mock.method.assert_called_once()
    
    # 验证调用参数
    assert mock.method.call_args == call(1, 2, key="value")
    assert mock.method.call_args_list == [call(1, 2, key="value")]

# side_effect - 动态返回值或异常
def test_side_effect():
    mock = Mock()
    
    # 返回序列
    mock.side_effect = [1, 2, 3]
    assert mock() == 1
    assert mock() == 2
    assert mock() == 3
    
    # 抛出异常
    mock.side_effect = ValueError("error")
    with pytest.raises(ValueError):
        mock()
    
    # 使用函数
    mock.side_effect = lambda x: x * 2
    assert mock(5) == 10
```

---

### 异步测试

```python
import pytest
import asyncio

# pytest-asyncio 插件
@pytest.mark.asyncio
async def test_async_function():
    result = await some_async_function()
    assert result == expected_value

@pytest.mark.asyncio
async def test_async_with_fixture(async_client):
    response = await async_client.get("/api/data")
    assert response.status_code == 200

# 异步 fixture
@pytest.fixture
async def async_db():
    db = await AsyncDatabase.connect()
    yield db
    await db.close()

@pytest.mark.asyncio
async def test_async_db(async_db):
    result = await async_db.query("SELECT 1")
    assert result is not None

# 同步测试中运行异步代码
def test_run_async_in_sync():
    async def async_task():
        await asyncio.sleep(0.1)
        return "done"
    
    result = asyncio.run(async_task())
    assert result == "done"
```

---

### 测试覆盖率

```bash
# 安装
pip install pytest-cov

# 运行并生成覆盖率报告
pytest --cov=myapp

# 指定覆盖率阈值
pytest --cov=myapp --cov-fail-under=80

# 生成 HTML 报告
pytest --cov=myapp --cov-report=html

# 生成 XML 报告（CI 使用）
pytest --cov=myapp --cov-report=xml

# 合并分支覆盖率
pytest --cov=myapp --cov-branch

# 排除文件
pytest --cov=myapp --cov-ignore-errors --omit="*/tests/*,*/migrations/*"
```

**配置文件** `.coveragerc`：
```ini
[run]
source = myapp
branch = True
omit = 
    */tests/*
    */migrations/*
    */__init__.py

[report]
precision = 2
exclude_lines =
    pragma: no cover
    def __repr__
    raise NotImplementedError
    if __name__ == .__main__.:
    @abstractmethod
fail_under = 80

[html]
directory = htmlcov

[xml]
output = coverage.xml
```

**pytest.ini 配置**：
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --cov=myapp --cov-report=term-missing
asyncio_mode = auto
```

---

## 🎭 Web 应用测试 (Playwright)

### 基础配置

```bash
# 安装
pip install playwright pytest-playwright
playwright install

# 或 npm
npm install @playwright/test
npx playwright install
```

**playwright.config.ts**：
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

---

### 页面操作

```typescript
import { test, expect } from '@playwright/test';

test('页面基础操作', async ({ page }) => {
  // 导航
  await page.goto('https://example.com');
  await page.goto('/login', { waitUntil: 'networkidle' });
  
  // 页面信息
  console.log(page.url());
  console.log(await page.title());
  
  // 等待
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(1000); // 不推荐，优先使用 waitFor
  await page.waitForURL('**/dashboard');
  
  // 截图
  await page.screenshot({ path: 'screenshot.png' });
  await page.screenshot({ path: 'full.png', fullPage: true });
  
  // PDF
  await page.pdf({ path: 'page.pdf' });
});

test('表单操作', async ({ page }) => {
  await page.goto('/form');
  
  // 输入文本
  await page.getByLabel('用户名').fill('testuser');
  await page.getByPlaceholder('请输入密码').fill('password123');
  
  // 清空后输入
  await page.getByLabel('搜索').clear();
  await page.getByLabel('搜索').fill('新搜索');
  
  // 勾选
  await page.getByLabel('同意条款').check();
  await expect(page.getByLabel('同意条款')).toBeChecked();
  
  // 选择
  await page.getByLabel('国家').selectOption('china');
  await page.getByLabel('城市').selectOption({ label: '北京' });
  
  // 上传文件
  await page.getByLabel('头像').setInputFiles('path/to/file.jpg');
  await page.getByLabel('文档').setInputFiles(['file1.pdf', 'file2.pdf']);
  
  // 点击
  await page.getByRole('button', { name: '提交' }).click();
  await page.getByRole('button', { name: '保存' }).click({ force: true });
  await page.getByText('详情').click({ button: 'right' });
  
  // 键盘操作
  await page.keyboard.press('Enter');
  await page.keyboard.type('Hello World');
  await page.getByLabel('内容').press('Control+A');
  await page.getByLabel('内容').press('Control+C');
  
  // 鼠标操作
  await page.mouse.click(100, 200);
  await page.mouse.dblclick(100, 200);
  await page.mouse.move(100, 200);
  await page.mouse.down();
  await page.mouse.move(200, 300);
  await page.mouse.up();
});

test('多页面/标签页', async ({ context }) => {
  // 打开新页面
  const page1 = await context.newPage();
  const page2 = await context.newPage();
  
  await page1.goto('https://example.com');
  await page2.goto('https://example.org');
  
  // 处理新标签页
  const [newPage] = await Promise.all([
    context.waitForEvent('page'),
    page1.getByText('打开新窗口').click(),
  ]);
  
  await newPage.waitForLoadState();
  console.log(await newPage.title());
});

test('对话框处理', async ({ page }) => {
  // 监听对话框
  page.on('dialog', async dialog => {
    console.log(dialog.message());
    await dialog.accept(); // 或 dismiss()
  });
  
  await page.getByText('删除').click();
});
```

---

### 元素定位

```typescript
import { test, expect } from '@playwright/test';

test('元素定位方式', async ({ page }) => {
  await page.goto('/');
  
  // 推荐方式 - 语义化定位
  await page.getByRole('button', { name: '登录' }).click();
  await page.getByLabel('用户名').fill('test');
  await page.getByPlaceholder('请输入邮箱').fill('test@example.com');
  await page.getByText('欢迎回来').click();
  await page.getByAltText('用户头像').click();
  await page.getByTitle('关闭').click();
  await page.getByTestId('submit-button').click();
  
  // CSS 选择器
  await page.locator('.btn-primary').click();
  await page.locator('#login-form').isVisible();
  await page.locator('div.card > h2.title').textContent();
  await page.locator('input[type="email"]').fill('test@example.com');
  
  // XPath
  await page.locator('xpath=//button[contains(text(), "提交")]').click();
  await page.locator('xpath=//div[@id="content"]//p').first().textContent();
  
  // 文本匹配
  await page.locator('text=登录').click();
  await page.locator('text=/登录|注册/').click();
  
  // 链式定位
  await page.locator('.sidebar').locator('.menu-item').first().click();
  await page.locator('form').getByRole('button').click();
  
  // 过滤
  await page.locator('.item').filter({ hasText: '活跃' }).click();
  await page.locator('.row').filter({ has: page.locator('.status.active') }).click();
  
  // 定位集合
  const items = page.locator('.list-item');
  await expect(items).toHaveCount(5);
  await items.first().click();
  await items.last().click();
  await items.nth(2).click();
  
  // 遍历
  const count = await items.count();
  for (let i = 0; i < count; i++) {
    console.log(await items.nth(i).textContent());
  }
});
```

---

### 断言验证

```typescript
import { test, expect } from '@playwright/test';

test('自动重试断言', async ({ page }) => {
  await page.goto('/');
  
  // 元素存在性
  await expect(page.getByRole('heading')).toBeVisible();
  await expect(page.getByText('加载中')).toBeHidden();
  await expect(page.getByTestId('loading')).not.toBeVisible();
  
  // 元素状态
  await expect(page.getByRole('button')).toBeEnabled();
  await expect(page.getByRole('button')).toBeDisabled();
  await expect(page.getByLabel('同意')).toBeChecked();
  await expect(page.getByRole('textbox')).toBeEditable();
  await expect(page.getByRole('textbox')).toBeEmpty();
  await expect(page.getByRole('link')).toBeFocused();
  
  // 文本内容
  await expect(page.getByRole('heading')).toHaveText('欢迎');
  await expect(page.getByRole('heading')).toContainText('欢迎');
  await expect(page.getByRole('heading')).toHaveText(/欢迎|你好/);
  
  // 属性值
  await expect(page.getByRole('link')).toHaveAttribute('href', '/home');
  await expect(page.getByRole('link')).toHaveAttribute('target', '_blank');
  await expect(page.getByRole('textbox')).toHaveValue('test');
  await expect(page.getByRole('img')).toHaveAttribute('src', /placeholder/);
  
  // CSS 属性
  await expect(page.getByRole('button')).toHaveCSS('color', 'rgb(0, 0, 255)');
  await expect(page.getByRole('button')).toHaveCSS('background-color', /rgb/);
  
  // 数量
  await expect(page.locator('.item')).toHaveCount(5);
  
  // 页面断言
  await expect(page).toHaveTitle(/首页/);
  await expect(page).toHaveURL('/dashboard');
  await expect(page).toHaveURL(/dashboard/);
  
  // 截图比对
  await expect(page).toHaveScreenshot('homepage.png');
  await expect(page.getByTestId('card')).toHaveScreenshot('card.png', {
    maxDiffPixels: 100,
  });
});

test('否定断言', async ({ page }) => {
  await page.goto('/');
  
  await expect(page.getByText('错误')).not.toBeVisible();
  await expect(page.getByRole('button')).not.toBeDisabled();
  await expect(page.locator('.item')).not.toHaveCount(0);
});

test('软断言（继续执行）', async ({ page }) => {
  await page.goto('/');
  
  await expect.soft(page.getByRole('heading')).toHaveText('欢迎');
  await expect.soft(page.getByRole('button')).toBeEnabled();
  // 即使上面失败也会继续执行
  await expect(page.getByTestId('content')).toBeVisible();
});

test('自定义断言', async ({ page }) => {
  const value = await page.getByRole('textbox').inputValue();
  expect(value).toHaveLength(10);
  expect(value).toMatch(/^[A-Z]/);
  
  const items = await page.locator('.item').allTextContents();
  expect(items).toContain('Item 1');
  expect(items).toHaveLength(5);
});
```

---

### 网络拦截

```typescript
import { test, expect } from '@playwright/test';

test('Mock API 响应', async ({ page }) => {
  // 拦截并 Mock 响应
  await page.route('**/api/users', async route => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify([
        { id: 1, name: 'User 1' },
        { id: 2, name: 'User 2' },
      ]),
    });
  });
  
  await page.goto('/users');
  await expect(page.getByText('User 1')).toBeVisible();
});

test('修改请求', async ({ page }) => {
  await page.route('**/api/data', async route => {
    const request = route.request();
    // 修改请求头
    const headers = {
      ...request.headers(),
      'Authorization': 'Bearer test-token',
    };
    await route.continue({ headers });
  });
  
  await page.goto('/dashboard');
});

test('阻断请求', async ({ page }) => {
  // 阻止图片加载
  await page.route('**/*.{png,jpg,jpeg,gif,webp}', route => route.abort());
  
  // 阻止第三方请求
  await page.route('**/analytics.js', route => route.abort());
  
  await page.goto('/');
});

test('等待网络请求', async ({ page }) => {
  await page.goto('/');
  
  // 等待特定请求完成
  const [response] = await Promise.all([
    page.waitForResponse('**/api/users'),
    page.getByRole('button', { name: '加载' }).click(),
  ]);
  
  expect(response.ok()).toBeTruthy();
  const data = await response.json();
  console.log(data);
});

test('记录网络请求', async ({ page }) => {
  const requests = [];
  
  page.on('request', request => {
    console.log('>>', request.method(), request.url());
    requests.push(request);
  });
  
  page.on('response', response => {
    console.log('<<', response.status(), response.url());
  });
  
  await page.goto('/');
});

test('模拟网络错误', async ({ page }) => {
  await page.route('**/api/data', route => route.abort('failed'));
  
  await page.goto('/');
  await expect(page.getByText('网络错误')).toBeVisible();
});

test('模拟慢速网络', async ({ page }) => {
  await page.route('**/api/data', async route => {
    await new Promise(f => setTimeout(f, 5000)); // 延迟 5 秒
    await route.continue();
  });
  
  await page.goto('/');
});
```

---

### 多浏览器测试

```typescript
import { test, expect } from '@playwright/test';

// 项目配置中已定义不同浏览器
// 使用 --project 参数运行特定浏览器

test('跨浏览器测试', async ({ page, browserName }) => {
  await page.goto('/');
  console.log(`Running on ${browserName}`);
  
  // 针对特定浏览器的逻辑
  if (browserName === 'webkit') {
    // Safari 特定处理
  }
});

// 移动端模拟
test('移动端视图', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 667 });
  await page.goto('/');
  
  // 或使用设备配置
  // 在 playwright.config.ts 中配置 devices['iPhone 12']
});

// 地理位置模拟
test('地理位置', async ({ context }) => {
  await context.grantPermissions(['geolocation']);
  await context.setGeolocation({ latitude: 52.52, longitude: 13.39 });
  
  const page = await context.newPage();
  await page.goto('/map');
});

// 主题/配色
test('暗黑模式', async ({ page }) => {
  await page.emulateMedia({ colorScheme: 'dark' });
  await page.goto('/');
  await expect(page.locator('body')).toHaveCSS('background-color', 'rgb(0, 0, 0)');
});

// 时区/语言
test('国际化', async ({ context }) => {
  await context.setLocale('zh-CN');
  await context.setTimezoneId('Asia/Shanghai');
  
  const page = await context.newPage();
  await page.goto('/');
});
```

**运行命令**：
```bash
# 运行所有浏览器
npx playwright test

# 运行指定浏览器
npx playwright test --project=chromium
npx playwright test --project=firefox
npx playwright test --project=webkit

# 运行多个项目
npx playwright test --project=chromium --project=firefox

# 调试模式
npx playwright test --debug

# UI 模式
npx playwright test --ui

# 查看报告
npx playwright show-report
```

---

## 📐 测试策略设计

### 测试金字塔原则

```
        /\
       /  \      E2E 测试 (10%)
      /    \     - 完整用户流程
     /------\    - 跨系统集成
    /        \   
   /----------\  集成测试 (20%)
  /            \ - API 测试
 /              \- 数据库集成
/----------------\
   单元测试 (70%)
   - 函数/方法测试
   - 组件测试
```

**分层策略**：

| 层级 | 比例 | 速度 | 成本 | 目标 |
|------|------|------|------|------|
| 单元测试 | 70% | ⚡⚡⚡ 毫秒级 | 低 | 验证逻辑正确性 |
| 集成测试 | 20% | ⚡⚡ 秒级 | 中 | 验证模块协作 |
| E2E 测试 | 10% | ⚡ 分钟级 | 高 | 验证用户流程 |

---

### 单元/集成/E2E 分层

#### 单元测试示例

```python
# 单元测试：测试单个函数
def test_calculate_discount():
    from myapp.utils import calculate_discount
    
    assert calculate_discount(100, 0.1) == 90
    assert calculate_discount(100, 0) == 100
    assert calculate_discount(0, 0.1) == 0

# 单元测试：测试单个类方法
class TestUserService:
    def test_create_user(self, mock_db):
        service = UserService(mock_db)
        user = service.create("test@example.com", "password")
        assert user.email == "test@example.com"
```

#### 集成测试示例

```python
# 集成测试：测试 API + 数据库
import pytest
from myapp import create_app, db

@pytest.fixture
def app():
    app = create_app(testing=True)
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

def test_user_api_integration(client, app):
    # 创建用户
    response = client.post('/api/users', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 201
    
    # 验证数据库
    with app.app_context():
        from myapp.models import User
        user = User.query.filter_by(email='test@example.com').first()
        assert user is not None
```

#### E2E 测试示例

```typescript
// E2E 测试：完整用户流程
test('用户注册登录流程', async ({ page }) => {
  // 注册
  await page.goto('/register');
  await page.getByLabel('邮箱').fill('test@example.com');
  await page.getByLabel('密码').fill('password123');
  await page.getByRole('button', { name: '注册' }).click();
  
  // 验证注册成功
  await expect(page).toHaveURL('/login');
  
  // 登录
  await page.getByLabel('邮箱').fill('test@example.com');
  await page.getByLabel('密码').fill('password123');
  await page.getByRole('button', { name: '登录' }).click();
  
  // 验证登录成功
  await expect(page).toHaveURL('/dashboard');
  await expect(page.getByText('欢迎')).toBeVisible();
});
```

---

### 测试数据管理

```python
# 工厂模式创建测试数据
import factory
from myapp.models import User

class UserFactory(factory.Factory):
    class Meta:
        model = User
    
    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    is_active = True

# 使用
def test_with_factory():
    user = UserFactory.create(username='testuser')
    assert user.email == 'testuser@example.com'
    
    # 批量创建
    users = UserFactory.create_batch(10)

# 使用 pytest fixture 管理数据
@pytest.fixture
def sample_users(db):
    users = [
        UserFactory.create(username=f'user{i}')
        for i in range(5)
    ]
    db.session.add_all(users)
    db.session.commit()
    return users

# Faker 生成假数据
from faker import Faker
fake = Faker()

def test_with_faker():
    user = UserFactory.create(
        username=fake.user_name(),
        email=fake.email(),
        phone=fake.phone_number()
    )
```

**测试数据库策略**：
```python
# conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    yield engine

@pytest.fixture
def db_session(db_engine):
    Session = sessionmaker(bind=db_engine)
    session = Session()
    yield session
    session.rollback()
    session.close()

# 使用事务回滚保持隔离
@pytest.fixture
def db_session_with_rollback(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()
```

---

### CI/CD 集成

**GitHub Actions**：
```yaml
# .github/workflows/test.yml
name: Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      
      - name: Run tests
        run: pytest --cov=myapp --cov-report=xml --cov-fail-under=80
      
      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          files: ./coverage.xml

  e2e-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Install Playwright
        run: npx playwright install --with-deps
      
      - name: Run E2E tests
        run: npx playwright test
      
      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 30
```

**GitLab CI**：
```yaml
# .gitlab-ci.yml
stages:
  - test
  - e2e

unit-tests:
  stage: test
  image: python:3.11
  script:
    - pip install -r requirements.txt
    - pip install pytest pytest-cov
    - pytest --cov=myapp --cov-report=xml --junitxml=report.xml
  coverage: '/(?i)total.*? (100(?:\.0+)?\%|[1-9]?\d(?:\.\d+)?\%)$/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml
      junit: report.xml

e2e-tests:
  stage: e2e
  image: mcr.microsoft.com/playwright:v1.40.0-focal
  script:
    - npm ci
    - npx playwright test
  artifacts:
    when: always
    paths:
      - playwright-report/
    expire_in: 30 days
```

**覆盖率门槛**：
```yaml
# codecov.yml
coverage:
  status:
    project:
      default:
        target: 80%
        threshold: 5%
    patch:
      default:
        target: 80%

comment:
  layout: "reach, diff, flags, files"
  require_changes: true
```

---

## 🤖 E2E 测试框架 (Vitest + Midscene)

### Midscene 简介

Midscene.js 是一个 AI 驱动的 E2E 测试框架，支持自然语言编写测试用例，自动生成页面交互代码。

```bash
# 安装
npm install @midscene/web vitest
```

### 配置

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    include: ['e2e/**/*.test.ts'],
    testTimeout: 60000,
    hookTimeout: 60000,
  },
});
```

### 自然语言测试用例

```typescript
import { test, expect } from 'vitest';
import { Page, midscene } from '@midscene/web';

test('用户登录流程', async () => {
  const page = new Page('https://example.com');
  
  // 自然语言描述测试步骤
  await midscene`
    打开登录页面
    在用户名输入框输入 "testuser"
    在密码输入框输入 "password123"
    点击登录按钮
    等待页面跳转到仪表板
    验证页面标题包含 "仪表板"
  `;
  
  // 验证
  await expect(page.url()).toContain('/dashboard');
});

test('搜索功能', async () => {
  const page = new Page('https://example.com');
  
  await midscene`
    在搜索框输入 "Playwright 教程"
    点击搜索按钮
    等待搜索结果加载
    验证搜索结果列表至少有 5 条
    点击第一条搜索结果
  `;
});
```

### AI 驱动 UI 测试

```typescript
import { test, expect } from 'vitest';
import { Page, ai } from '@midscene/web';

test('AI 自动定位元素', async () => {
  const page = new Page('https://example.com');
  
  // 使用自然语言描述元素，AI 自动定位
  const loginButton = await ai('登录按钮，位于页面右上角');
  await loginButton.click();
  
  // AI 理解上下文
  await ai('在用户名输入框输入测试账号').fill('test@example.com');
  await ai('密码输入框，在用户名输入框下方').fill('password');
  
  // AI 断言
  await ai('验证登录成功提示出现');
});

test('AI 自动修复定位器', async () => {
  const page = new Page('https://example.com');
  
  // 当 UI 变化时，AI 可以自动适应
  // 不再依赖脆弱的 CSS 选择器
  const element = await ai('提交订单按钮，可能是绿色或蓝色的');
  await element.click();
});

test('AI 生成测试数据', async () => {
  // AI 生成测试数据
  const testUser = await ai.generate('生成一个有效的用户注册信息，包含邮箱、密码、手机号');
  console.log(testUser);
  // { email: 'test123@example.com', password: 'Secure@123', phone: '13812345678' }
});
```

### 跨平台测试

```typescript
import { test, expect } from 'vitest';
import { Page, Device } from '@midscene/web';

// 移动端测试
test('移动端响应式测试', async () => {
  const mobilePage = new Page('https://example.com', {
    device: Device.iPhone12,
  });
  
  await midscene`
    验证移动端菜单按钮可见
    点击菜单按钮
    验证导航菜单展开
  `;
});

// 平板测试
test('平板布局测试', async () => {
  const tabletPage = new Page('https://example.com', {
    device: Device.iPadPro,
  });
  
  await midscene`
    验证侧边栏显示
    验证主内容区域宽度适配
  `;
});

// 多设备并行测试
test('多设备兼容性', async () => {
  const devices = [Device.iPhone12, Device.Pixel5, Device.iPadPro];
  
  await Promise.all(
    devices.map(async (device) => {
      const page = new Page('https://example.com', { device });
      await midscene`
        验证页面正常加载
        验证主要内容可见
        验证无布局错误
      `;
    })
  );
});
```

### 与 Playwright 集成

```typescript
import { test, expect } from '@playwright/test';
import { injectMidscene } from '@midscene/web';

test('Midscene + Playwright', async ({ page }) => {
  // 注入 Midscene 能力
  const mid = injectMidscene(page);
  
  await page.goto('https://example.com');
  
  // 使用自然语言
  await mid`在搜索框输入 "测试"`;
  await mid`点击搜索按钮`;
  
  // 使用传统 Playwright
  await expect(page.locator('.results')).toBeVisible();
  
  // 混合使用
  const resultCount = await mid`获取搜索结果数量`;
  console.log(resultCount);
});
```

---

## 📊 常用命令速查表

### pytest 命令

```bash
# 基础运行
pytest                           # 运行所有测试
pytest -v                        # 详细输出
pytest -vv                       # 更详细输出
pytest -x                        # 首次失败即停止
pytest --tb=short                # 简短回溯
pytest -q                        # 安静模式

# 选择性运行
pytest test_file.py              # 指定文件
pytest tests/unit/               # 指定目录
pytest -k "login"                # 关键词过滤
pytest -m "slow"                 # 标记过滤
pytest test_file.py::TestClass   # 指定类
pytest test_file.py::test_func   # 指定函数

# 并行运行
pytest -n auto                   # 自动并行
pytest -n 4                      # 4 个进程

# 覆盖率
pytest --cov=myapp               # 覆盖率报告
pytest --cov=myapp --cov-report=html  # HTML 报告
pytest --cov=myapp --cov-fail-under=80  # 门槛

# 调试
pytest --pdb                     # 失败时进入调试
pytest --pdb-trace               # 开始时进入调试
pytest -s                        # 显示打印输出

# 失败重试
pytest --lf                      # 只运行上次失败的
pytest --ff                      # 先运行上次失败的
pytest --reruns 3                # 失败重试 3 次
```

### Playwright 命令

```bash
# 运行测试
npx playwright test              # 运行所有测试
npx playwright test example.spec.ts  # 指定文件
npx playwright test --project=chromium  # 指定浏览器
npx playwright test --headed     # 有界面模式
npx playwright test --debug      # 调试模式
npx playwright test --ui         # UI 模式

# 代码生成
npx playwright codegen           # 录制代码
npx playwright codegen example.com  # 打开指定网站

# 报告
npx playwright show-report       # 显示报告
npx playwright show-trace trace.zip  # 显示 Trace

# 安装
npx playwright install           # 安装浏览器
npx playwright install chromium  # 安装指定浏览器

# 其他
npx playwright test --list       # 列出所有测试
npx playwright test --reporter=html  # HTML 报告
```

### Vitest 命令

```bash
# 运行测试
vitest                           # 运行所有测试
vitest run                       # 单次运行
vitest watch                     # 监听模式
vitest --coverage                # 覆盖率

# 选择性运行
vitest test-file.test.ts         # 指定文件
vitest --filter "login"          # 过滤

# UI 模式
vitest --ui                      # UI 界面
```

---

## ✨ 最佳实践

### 1. 测试命名规范

```python
# ✅ 好的命名
def test_user_can_login_with_valid_credentials():
    pass

def test_login_fails_with_invalid_password():
    pass

def test_user_cannot_delete_own_account():
    pass

# ❌ 不好的命名
def test_1():
    pass

def test_login():
    pass
```

### 2. AAA 模式（Arrange-Act-Assert）

```python
def test_user_creation():
    # Arrange - 准备
    user_data = {
        'username': 'testuser',
        'email': 'test@example.com'
    }
    service = UserService()
    
    # Act - 执行
    user = service.create(user_data)
    
    # Assert - 断言
    assert user.username == 'testuser'
    assert user.email == 'test@example.com'
    assert user.id is not None
```

### 3. 测试隔离

```python
# ✅ 每个测试独立
@pytest.fixture
def clean_db(db):
    db.query(Delete(User))
    yield db
    db.rollback()

def test_create_user(clean_db):
    # 测试使用干净的数据库
    pass

def test_delete_user(clean_db):
    # 测试使用干净的数据库
    pass

# ❌ 测试依赖其他测试
saved_user_id = None

def test_create_user():
    global saved_user_id
    user = create_user()
    saved_user_id = user.id  # 不推荐

def test_delete_user():
    delete_user(saved_user_id)  # 依赖上一个测试
```

### 4. Mock 边界

```python
# ✅ Mock 外部依赖
@patch('myapp.services.email.send_email')
def test_send_welcome_email(mock_send):
    service = EmailService()
    service.send_welcome('test@example.com')
    
    mock_send.assert_called_once_with(
        to='test@example.com',
        subject='Welcome!',
        body=ANY
    )

# ❌ Mock 自己的代码
@patch('myapp.utils.validate_email')
def test_register(mock_validate):
    # 不应该 Mock 自己要测试的逻辑
    pass
```

### 5. E2E 测试稳定性

```typescript
// ✅ 使用等待而非固定延迟
await expect(page.getByText('加载完成')).toBeVisible();
await page.waitForLoadState('networkidle');

// ❌ 固定延迟
await page.waitForTimeout(5000);

// ✅ 使用语义化定位器
await page.getByRole('button', { name: '提交' }).click();
await page.getByLabel('用户名').fill('test');

// ❌ 脆弱的 CSS 选择器
await page.locator('#btn-submit-123').click();
await page.locator('.input-field.name').fill('test');

// ✅ 重试逻辑
test('稳定测试', async ({ page }) => {
  await page.goto('/');
  
  for (let i = 0; i < 3; i++) {
    try {
      await expect(page.getByText('数据')).toBeVisible({ timeout: 5000 });
      break;
    } catch {
      if (i === 2) throw e;
      await page.reload();
    }
  }
});
```

### 6. 测试数据清理

```python
# ✅ 自动清理
@pytest.fixture
def temp_file():
    file_path = '/tmp/test_file.txt'
    with open(file_path, 'w') as f:
        f.write('test')
    yield file_path
    os.remove(file_path)  # 测试后自动清理

# ✅ 使用上下文管理器
@pytest.fixture
def db_session():
    session = Session()
    yield session
    session.close()
    session.rollback()
```

### 7. 测试覆盖率陷阱

```python
# ❌ 只关注覆盖率数字
def test_all_branches():
    # 覆盖了所有分支但没有验证
    if condition:
        pass
    else:
        pass

# ✅ 有意义的测试
def test_returns_true_when_valid():
    assert validate(True) is True

def test_returns_false_when_invalid():
    assert validate(False) is False
```

### 8. CI/CD 测试优化

```yaml
# ✅ 并行运行 + 缓存
jobs:
  test:
    strategy:
      matrix:
        shard: [1/4, 2/4, 3/4, 4/4]
    steps:
      - uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
      
      - run: pytest --shard ${{ matrix.shard }}
```

---

## 📚 参考资源

- [pytest 官方文档](https://docs.pytest.org/)
- [Playwright 官方文档](https://playwright.dev/)
- [Vitest 官方文档](https://vitest.dev/)
- [Midscene.js 官方文档](https://midscenejs.com/)
- [Testing JavaScript](https://testingjavascript.com/)

---

> 最后更新：2026-03-26