# Python 核心面试题

## 可变对象与不可变对象

不可变对象：int、str、tuple、frozenset —— 创建后不能修改内容。
可变对象：list、dict、set —— 可以原地修改。

```python
a = [1, 2]
b = a
b.append(3)
print(a)  # [1, 2, 3]  因为 a 和 b 指向同一对象
```

## GIL 全局解释器锁

Python 的 GIL 确保同一时刻只有一个线程执行 Python 字节码。
因此多线程不适合 CPU 密集型任务（用 multiprocessing 代替），
但适合 I/O 密集型任务（网络请求、文件读写）。

## 装饰器

装饰器是一个接受函数、返回函数的可调用对象。用于在不修改原函数的情况下添加功能。

```
def log(func):
    def wrapper(*args, **kwargs):
        print(f"调用 {func.__name__}")
        return func(*args, **kwargs)
    return wrapper
```