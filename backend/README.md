# Routebook 后端

> 项目总说明见仓库根 `README.md`，文档集入口见 `docs/README.md`。本文件只讲**后端怎么跑**。

## 前置

- Python 3.12（由 uv 管理，见 `.python-version`）· uv · Docker Desktop

## 启动

`.env` 放在**仓库根目录**（不是 `backend/`）。`core/config.py` 按**绝对路径**加载它，
所以在哪个目录执行命令都能读到，不需要先 `cd` 到根目录。

```bash
# 1. 基础设施（仓库根执行）
docker compose -f deploy/docker-compose.dev.yml up -d

# 2. 后端（backend/ 执行，或任意目录）
uv sync
uv run uvicorn routebook.main:app --reload --port 8000
```

## 自检

```bash
uv run ruff check .     # 代码规范
uv run mypy src         # 类型检查
uv run pytest           # 测试（M1 起有真实用例）
```

## 路由约定

**所有后端路由都在 `/api` 下**，前端 dev server 的代理**不做路径重写**：

| 用途 | 路径 |
|---|---|
| 健康探针 | `/api/health` |
| Swagger（仅 DEBUG） | `/api/docs` |
| OpenAPI（M2 生成前端类型用） | `/api/openapi.json` |
| 业务接口 | `/api/v1/*` |

## 目录约定

```
src/routebook/
├── main.py        FastAPI 应用入口（唯一）
├── core/          配置、日志、依赖注入
├── db/            会话与迁移（M1）
├── models/        SQLAlchemy ORM（M1）
├── schemas/       Pydantic
├── repositories/  SQL 只写在这里
├── services/      业务逻辑
├── api/v1/        路由
├── ai/            LLM / RAG（M5 起）
└── tasks/         Celery（M8 起）
```
