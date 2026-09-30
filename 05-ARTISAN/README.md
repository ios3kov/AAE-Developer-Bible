# Artisan

Artisan — API для замены rendering behavior 3D layers в composition. Это не «просто 3D effect».

Adobe SDK Guide подчёркивает сложность и рекомендует идти сюда только при сильной необходимости.

## Use only if

- продукт действительно должен стать renderer'ом AE 3D scene;
- вам нужен render context для всей 3D composition semantics;
- effect-level rendering недостаточно концептуально.

## Do not use if

- нужно отрендерить собственную 3D-модель внутри одного effect;
- нужен GPU effect;
- нужен viewport overlay;
- нужен panel/tool для управления 3D assets.

## Engineering cost

Ожидать:
- большое количество scene semantics;
- камеры/свет/transform/material issues;
- interactive vs final rendering behavior;
- host version compatibility burden;
- отдельные massive test scenes.
