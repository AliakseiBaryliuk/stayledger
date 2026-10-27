# StayLedger — Git workflow

> Этот документ — рабочий процесс Git для проекта StayLedger. Он дополняет
> [`.cline/rules/02-git-workflow.md`](../.cline/rules/02-git-workflow.md) и
> [`docs/architecture.md`](architecture.md); спецификации — в
> `openspec/specs/<capability>/spec.md`.

Интеграционная ветка — `master` (`origin/master`). `origin/main` legacy, на неё не нацеливаемся.

## Ветвление

- Никогда не коммитим и не пушим напрямую в `master`.
- Поток: ответвляемся от `master` → коммиты → пуш ветки → pull request → мержим.
- Именование веток: `<type>/<short-topic>` (`feature/booking-calendar`, `fix/...`, `chore/...`).
- Каждая ветка реализует **одну** задачу / мини-сценарий.

## Коммитные сообщения

Каждый субъект начинается с тега задачи и краткого описания на английском:

```
[NO_TASK] <краткое описание>
[<task-number>] <краткое описание>
```

- `[NO_TASK]` — нет трекер-задачи (например, работа только над OpenSpec-изменением, или мини-сценарий, у которого `package-info.java` не содержит task id).
- `[<task-number>]` — id задачи из трекера ровно как есть (`[1234]`, `[SL-42]`). Должен совпадать с id, записанным в `package-info.java` мини-сценария, который затронут коммитом (см. [`docs/architecture.md`](architecture.md)). Никогда не придумываем номера.
- Описание: короткое, повелительное наклонение, без воды («some fixes», «WIP»), без точки в конце.
- Коммитные сообщения пишем на английском — как и весь остальной репозиторий.
- Необязательное тело: почему нужен изменение. Кратко.

Примеры, привязанные к мини-сценариям StayLedger:

```
[NO_TASK] add git workflow rules
[NO_TASK] reject overlapping bookings
[1234] add booking-calendar core-api port
[SL-42] implement inventory postgres_adapter
```

Коммиты, сделанные до введения этого правила (`init app`, `define config`), остаются как есть; новые коммиты используют тег.

## Squash перед пушем

Ветка может содержать промежуточные коммиты во время разработки. Перед пушем
сжимаем **только новые** коммиты этой ветки (не коммиты, уже существующие в `master`)
в один коммит с тегом и описанием:

```
[<task-number>] <feature summary>
[NO_TASK] <feature summary>
```

Используем `git rebase -i` или `git reset --soft` onto `master`, затем один коммит.

## Rebase перед каждым пушем

```bash
git fetch origin
git switch master
git rebase origin/master        # или: git pull --ff-only
git switch <my-branch>
git rebase master               # подтягиваем master в рабочую ветку
# решаем конфликты, прогоняем тесты (см. docs/architecture.md)
git push --force-with-lease     # никогда просто --force / -f
```

Повторяем этот цикл **перед каждым** пушем, не только первым. После мержа pull request'а удаляем ветку и начинаем следующую от свежего `master`.

## Конфликты

- Разрешаем конфликты в рабочей ветке; никогда не переписываем и не разрешаем внутри `master`.
- Перед пушем прогоняем тесты: unit для мапперов/фабрик, integration для портов, MockWebServer для Telegram HTTP, e2e happy path в конце мини-сценария.

## Локальные настройки (один раз на машину)

```bash
git config --global pull.rebase true
git config --global rerere.enabled true
git config --global branch.autoSetupRebase always
```

## Pre-push хук (рекомендуется)

Версийный скрипт `hooks/pre-push` автоматически контролирует дисциплину веток.
Устанавливаем один раз на клон:

```bash
git config core.hooksPath hooks
chmod +x hooks/pre-push   # на Windows: Git Bash или `attrib +R hooks/pre-push`
```

Хук проверяет:
- Текущая ветка — не `master`
- Ровно 1 коммит впереди от `origin/master` (сжатый)
- Субъект последнего коммита соответствует `[<task-number>] <summary>` или `[NO_TASK] <summary>`

Байпас возможен через `--no-verify` (намеренное переопределение, не по умолчанию).

## Привязка к мини-сценариям StayLedger

Каждый коммит должен затрагивать конкретный мини-сценарий, реализованный как
`core-api` + `core-impl` + адаптеры (`_infra`). Структура:

```
_core/src/main/java/com/stayledger/<mini-scenario>/
  <state>/
    port/incoming/   ...In
    port/outgoing/   ...Out
    mapper/          AToBMapper
    factory/         BFactory
_infra/src/main/java/com/stayledger/<mini-scenario>/
  <adapter>/
_ms/src/main/resources/
  application.yaml
```

`package-info.java` верхнего пакета мини-сценария должен ссылаться на
спецификацию OpenSpec: `openspec/specs/<capability>/spec.md`.

### Карта capability (из `docs/architecture.md`)

| Мини-сценарий | Capability (`openspec/specs/<id>`) | Типичные адаптеры |
|---|---|---|
| `telegram-order-intake` | `telegram-order-intake` | `telegram_adapter` |
| `ai-client-replies` | `ai-client-replies` | `ai_adapter` |
| `booking-calendar` | `booking-calendar` | `postgres_adapter` |
| `inventory` | `inventory` | `postgres_adapter` |
| `damage-and-prepayment` | `damage-and-prepayment` | `postgres_adapter` |

При добавлении нового мини-сценария добавляем строку в эту таблицу.
