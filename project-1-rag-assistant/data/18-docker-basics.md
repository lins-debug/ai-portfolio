# Docker 基础

## 什么是容器

容器是轻量级的虚拟化技术，将应用和依赖打包在一起。与虚拟机不同，容器共享宿主机内核，启动更快（秒级 vs 分钟级），占用资源更小。

## Docker 核心概念

镜像：只读模板，包含运行环境和代码
容器：镜像的运行实例，可读写
Dockerfile：构建镜像的脚本
Docker Compose：编排多容器应用

## 常用命令

docker build -t name .：用当前目录的 Dockerfile 构建镜像
docker run -p 8080:80 name：运行容器并映射端口
docker ps：查看运行中的容器
docker exec -it container bash：进入容器交互式终端
docker-compose up -d：后台启动所有服务

## 镜像优化技巧

用 .dockerignore 排除无关文件
合并 RUN 命令减少层数
用 alpine 基础镜像减小体积
多阶段构建：编译和运行分两个阶段
