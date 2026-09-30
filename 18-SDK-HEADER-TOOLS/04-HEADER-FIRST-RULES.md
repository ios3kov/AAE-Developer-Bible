# Header-first rules

1. Exact function name/signature → **build SDK header**.
2. Ownership/lifecycle → header comments + official sample + guide.
3. Host availability → suite/version macro + release notes + runtime acquisition test.
4. Public HTML guide полезен для контекста, но найденные расхождения фиксируются в `14-NATIVE-INTEGRATIONS/13-DOCS-ERRATA.md`.
5. Никогда не «исправлять» вызов так, чтобы он совпал с HTML, если compiler/header говорит обратное.
6. Никогда не кастовать неподходящую suite generation только ради компиляции.
7. Если `AcquireSuite` не дал нужную version — graceful fallback или понятная ошибка, но не dereference `nullptr`.
