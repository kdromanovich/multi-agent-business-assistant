# Multi-Agent Business Assistant

[![CI](https://github.com/kdromanovich/multi-agent-business-assistant/actions/workflows/ci.yml/badge.svg)](https://github.com/kdromanovich/multi-agent-business-assistant/actions/workflows/ci.yml)

Мультиагентный reference-backend на **LangGraph** с supervisor-агентом, специализированными агентами, human-in-the-loop и отдельным **MCP v2** сервером инструментов.

## Что есть внутри

- Supervisor определяет тип запроса.
- Research Agent работает с базой знаний.
- Document Agent анализирует переданный текст.
- Data Agent обрабатывает аналитические/числовые задачи.
- Action Agent только готовит действие и переводит запуск в `pending_approval`.
- Все запуски сохраняются в локальный audit store.
- MCPServer публикует typed tools для внешних AI-клиентов.
- Integration-тест проверяет API, сохранение запуска и approval flow.

## Проверка в CI

GitHub Actions запускает тесты в детерминированном `DEMO_MODE=true`: проверяется API-key защита, маршрутизация supervisor, сохранение состояния, переход в `pending_approval` и явное подтверждение действия. Отдельно выполняются unit-тесты routing и tools.

## Запуск

```bash
cp .env.example .env
docker compose up --build
```

По умолчанию включен `DEMO_MODE=true`, поэтому проект можно показать без ключа OpenAI. Для live LLM-режима укажите ключ и переключите demo mode.

## Статус проекта

Это portfolio/reference implementation, а не заявление о работающем customer production deployment. Demo-режим специально сделан воспроизводимым для проверки архитектуры и API.
