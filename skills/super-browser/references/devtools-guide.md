# DevTools 调试指南

> Chrome DevTools 协议提供了丰富的浏览器调试能力，包括性能分析、网络监控、内存诊断等。

## 目录

1. [性能分析](#性能分析)
2. [网络调试](#网络调试)
3. [控制台调试](#控制台调试)
4. [内存分析](#内存分析)
5. [高级技巧](#高级技巧)

---

## 性能分析

### Performance API

通过 JavaScript 获取性能指标：

```javascript
// 页面加载性能
const timing = performance.timing;
const metrics = {
  // DNS 查询
  dns: timing.domainLookupEnd - timing.domainLookupStart,
  // TCP 连接
  tcp: timing.connectEnd - timing.connectStart,
  // 请求时间
  request: timing.responseStart - timing.requestStart,
  // 响应时间
  response: timing.responseEnd - timing.responseStart,
  // DOM 解析
  dom: timing.domComplete - timing.domLoading,
  // 总加载时间
  total: timing.loadEventEnd - timing.navigationStart
};
console.table(metrics);
```

### Performance Observer

监控性能事件：

```javascript
// 监控长任务
const observer = new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    console.log('长任务:', entry.duration, 'ms');
  }
});
observer.observe({ entryTypes: ['longtask'] });

// 监控资源加载
const resourceObserver = new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    console.log('资源:', entry.name, entry.duration, 'ms');
  }
});
resourceObserver.observe({ entryTypes: ['resource'] });
```

### Web Vitals

获取核心 Web 指标：

```javascript
// 使用 web-vitals 库
import { getCLS, getFID, getLCP, getFCP, getTTFB } from 'web-vitals';

getCLS(console.log);  // 累积布局偏移
getFID(console.log);  // 首次输入延迟
getLCP(console.log);  // 最大内容绘制
getFCP(console.log);  // 首次内容绘制
getTTFB(console.log); // 首字节时间
```

---

## 网络调试

### 拦截请求

```javascript
// 使用 Playwright 拦截
await page.route('**/*.jpg', route => route.abort());
await page.route('**/api/**', route => 
  route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: JSON.stringify({ mock: true })
  })
);
```

### 监控请求

```javascript
// 监听请求
page.on('request', request => {
  console.log('>>', request.method(), request.url());
});

// 监听响应
page.on('response', response => {
  console.log('<<', response.status(), response.url());
});
```

### 网络模拟

```javascript
// 离线模式
const client = await page.context().newCDPSession(page);
await client.send('Network.emulateNetworkConditions', {
  offline: true,
  latency: 0,
  downloadThroughput: 0,
  uploadThroughput: 0
});

// 慢速 3G
await client.send('Network.emulateNetworkConditions', {
  offline: false,
  latency: 100,
  downloadThroughput: 500 * 1024,
  uploadThroughput: 500 * 1024
});
```

---

## 控制台调试

### Console API

```javascript
// 基本输出
console.log('信息');
console.warn('警告');
console.error('错误');

// 表格输出
console.table([{ name: 'A', value: 1 }, { name: 'B', value: 2 }]);

// 分组
console.group('组名');
console.log('内容');
console.groupEnd();

// 计时
console.time('操作');
// ... 代码 ...
console.timeEnd('操作');

// 堆栈
console.trace('调用堆栈');
```

### Debugger

```javascript
// 断点
debugger;

// 条件断点
if (condition) debugger;
```

---

## 内存分析

### Memory API

```javascript
// 获取内存信息（仅 Chrome）
if (performance.memory) {
  console.log({
    used: Math.round(performance.memory.usedJSHeapSize / 1024 / 1024) + ' MB',
    total: Math.round(performance.memory.totalJSHeapSize / 1024 / 1024) + ' MB',
    limit: Math.round(performance.memory.jsHeapSizeLimit / 1024 / 1024) + ' MB'
  });
}
```

### 堆快照

在 DevTools 中：
1. 打开 Memory 面板
2. 选择 "Heap snapshot"
3. 拍摄快照
4. 比较快照查找内存泄漏

### 内存泄漏检测

```javascript
// 检测 detached DOM 节点
const detachedNodes = [];
const walk = (node) => {
  if (!node.isConnected) {
    detachedNodes.push(node);
  }
  for (const child of node.childNodes) {
    walk(child);
  }
};
```

---

## 高级技巧

### 覆盖地理位置

```javascript
// Playwright
await page.context().overridePermissions('https://example.com', ['geolocation']);
await page.setGeolocation({ latitude: 39.9042, longitude: 116.4074 });

// CDP
const client = await page.context().newCDPSession(page);
await client.send('Emulation.setGeolocationOverride', {
  latitude: 39.9042,
  longitude: 116.4074,
  accuracy: 100
});
```

### 覆盖 User-Agent

```javascript
// Playwright
await page.setUserAgent('Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) ...');

// CDP
await client.send('Network.setUserAgentOverride', {
  userAgent: 'Custom User Agent'
});
```

### 覆盖设备像素比

```javascript
await client.send('Emulation.setDeviceMetricsOverride', {
  width: 1920,
  height: 1080,
  deviceScaleFactor: 2,  // Retina
  mobile: false
});
```

### CPU 限速

```javascript
await client.send('Emulation.setCPUThrottlingRate', {
  rate: 4  // 4x 慢
});
```

### 截图特定元素

```javascript
const element = await page.$('#target');
await element.screenshot({ path: 'element.png' });
```

### 强制暗色模式

```javascript
await client.send('Emulation.setEmulatedMedia', {
  features: [{ name: 'prefers-color-scheme', value: 'dark' }]
});
```

---

## CDP 命令速查

| 命令 | 功能 |
|------|------|
| `Network.emulateNetworkConditions` | 网络限速 |
| `Emulation.setCPUThrottlingRate` | CPU 限速 |
| `Emulation.setDeviceMetricsOverride` | 设备模拟 |
| `Emulation.setGeolocationOverride` | 地理位置 |
| `Emulation.setEmulatedMedia` | 媒体特性 |
| `Network.setUserAgentOverride` | User-Agent |
| `Page.captureScreenshot` | 截图 |
| `Performance.enable` | 启用性能监控 |

---

## 参考链接

- Chrome DevTools Protocol: https://chromedevtools.github.io/devtools-protocol/
- Performance API: https://developer.mozilla.org/en-US/docs/Web/API/Performance
- Web Vitals: https://web.dev/vitals/