# AEGP project and render automation

## Native vs scripting

Начинать с вопроса: нужен ли AEGP действительно?

ExtendScript проще для:
- создать comp/layers;
- расставить keyframes;
- add to render queue;
- batch project operations.

AEGP оправдан, если нужен:
- native performance;
- API, отсутствующий в scripting;
- hooks/events;
- тесная связь с другим C++ plug-in;
- controlled native service layer.

## Undo

Любое изменение project state должно иметь понятную undo model. Если suite предоставляет begin/end undo group — использовать корректно.

## Invalidations

После операций add/remove:
- не продолжать использовать handles, которые docs объявляют invalidated;
- reacquire by stable host-supported identity, где возможно;
- unit-test wrapper state machine отдельно.

## UI thread assumptions

Не переносить host calls на произвольный background thread, если API не говорит, что это допустимо. Background compute отделять от host mutation.
