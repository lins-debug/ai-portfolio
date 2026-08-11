# MLOps 基础

## 什么是 MLOps

MLOps 是将 DevOps 实践应用于机器学习。目标：自动化模型训练、部署、监控的整个生命周期。解决从 Jupyter Notebook 到生产环境的鸿沟。

## 核心组件

实验追踪：MLflow、Weights & Biases 记录参数和指标
模型注册：版本化的模型存储，方便回滚和对比
特征存储：统一管理特征的版本和时效性
管道编排：Airflow、Prefect 调度训练和推理任务
模型服务：FastAPI、Triton Inference Server

## LLM 运维特点

与传统 ML 不同：推理成本高（GPU）、prompt 管理取代特征工程、评估依赖 LLM-as-judge。重点关注延迟优化（缓存、流式输出）和成本控制（token 预算、模型降级）。
