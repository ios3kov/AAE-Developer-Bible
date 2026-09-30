# Artisan — custom 3D renderer

Artisan — specialized AEGP, который может заменить rendering 3D layers композиции.

## Registration

AEGP entry point вызывает `AEGP_RegisterArtisan()` или interactive variant и передаёт `PR_ArtisanEntryPoints`.

## Contract

- After Effects владеет composition/project model;
- Artisan получает render context;
- через Artisan/AEGP suites извлекает scene information;
- возвращает rendered result по host contract.

## Почему это отдельный класс сложности

Effect работает на изображении/слое внутри graph. Artisan получает ответственность за **3D compositing/rendering scheme композиции**. Это архитектурно ближе к renderer integration, чем к обычному effect.

## Когда использовать

Только если продукт реально должен быть новым 3D renderer. Для 3D effect, particles, relighting одного слоя и т.п. сначала рассмотреть обычный Effect API/GPU.

Reference: Adobe SDK sample **Artie**.
