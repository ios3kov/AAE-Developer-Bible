# Host callback ABI boundary

C++ exception не должен пересечь C callback/entry point, который вызвал After Effects.

Граница:

```text
AE C ABI → noexcept wrapper → C++ implementation
```

Внутри можно использовать обычный C++, но верхний wrapper обязан поймать exception и вернуть валидный `A_Err`, выбранный проектом. `HostCallbackGuard.h` специально принимает fallback error извне и не придумывает SDK constant.
