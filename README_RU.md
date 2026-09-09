# Multi-Agent Business Assistant

Мультиагентный backend на **LangGraph** с supervisor-агентом, специализированными агентами, human-in-the-loop и отдельным **MCP v2** сервером инструментов.

## Что есть внутри

- Supervisor определяет тип запроса.
- Research Agent работает с базой знаний.
- Document Agent анализирует переданный текст.
- Data Agent обрабатывает аналитические/числовые задачи.
- Action Agent только готовит действие и переводит запуск в `pending_approval`.
- Все запуски сохраняются в локальный audit store.
- MCPServer публикует typed tools для внешних AI-клиентов.

## Запуск

```bash
cp .env.example .env
docker compose up --build
```

По умолчанию включен `DEMO_MODE=true`, поэтому проект можно показать без ключа OpenAI. Для реального LLM-режима укажите ключ и переключите demo mode.
