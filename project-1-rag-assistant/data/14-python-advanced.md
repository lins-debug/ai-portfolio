# Python 进阶

## 生成器与迭代器

迭代器：实现 __iter__ 和 __next__ 的对象，惰性计算。
生成器：用 yield 关键字定义，比迭代器更简洁。按需生成数据，省内存。

```python
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


```

## 上下文管理器

用 with 语句管理资源，确保资源正确释放。实现 **enter** 和 **exit** 方法，或用 @contextmanager 装饰器。

```
with open("file.txt") as f:
    data = f.read()
# 自动关闭文件
```

## 协程与异步编程

async/await 是 Python 异步编程的核心。事件循环管理多个协程的切换，不会因为一个 I/O 操作阻塞整个程序。asyncio 是标准库的异步框架。

## 类型注解

```
def greet(name: str) -> str:
    return f"Hello, {name}"
```

Python 3.5+ 支持。用 mypy 做静态检查，提升大型项目的可维护性。
