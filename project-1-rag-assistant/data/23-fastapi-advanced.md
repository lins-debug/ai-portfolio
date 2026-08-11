# FastAPI 进阶

## 依赖注入

用 Depends() 注入共享逻辑（数据库连接、认证检查、参数校验）。依赖可嵌套、可缓存。

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users")
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()
```

## 中间件

拦截所有请求/响应，统一处理日志、CORS、性能监控。用 @app.middleware 注册。

## 后台任务

BackgroundTasks 处理耗时操作（发邮件、生成报告），不阻塞响应。Celery 用于更复杂的异步任务队列。

## 流式响应

StreamingResponse 实现 LLM 的流式输出。配合 Server-Sent Events 或 WebSocket 实时推送内容。提升用户体验，秒级首字响应。
