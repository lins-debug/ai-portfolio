# API 设计与 RESTful

## RESTful 原则

资源用名词复数：/users 而非 /getUsers
HTTP 方法表示操作：GET 查询、POST 创建、PUT 更新、DELETE 删除
状态码语义正确：201 创建成功、204 无内容、422 参数校验失败

## 常见设计模式

分页：?page=1&page_size=20，返回 total 字段
过滤排序：?status=active&sort=-created_at
版本控制：URL 前缀 /v1/ 或 Header Accept: application/vnd.api+json;version=1
错误响应：统一格式 {"error": {"code": "NOT_FOUND", "message": "..."}}

## 安全实践

用 HTTPS 加密传输。JWT + Refresh Token 做身份认证。速率限制防止滥用。输入校验防止注入。敏感信息走环境变量。
