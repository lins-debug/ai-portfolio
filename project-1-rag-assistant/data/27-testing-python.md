# Python 测试

## 测试金字塔

单元测试：测单个函数/类，快、多
集成测试：测多个模块协作
端到端测试：测完整用户流程，慢、少

## pytest 常用用法

```python
def test_add():
    assert add(2, 3) == 5

@pytest.mark.parametrize("a,b,expected", [(1,2,3), (0,0,0)])
def test_add_param(a, b, expected):
    assert add(a, b) == expected
```

fixture：管理测试前置条件和清理
mock：用 unittest.mock 替换外部依赖（API、数据库）
conftest.py：共享 fixture 的配置文件

## 覆盖率

pytest --cov 生成覆盖率报告。关注分支覆盖率而非行覆盖率。关键路径必须有测试，工具代码可以适当放宽。
