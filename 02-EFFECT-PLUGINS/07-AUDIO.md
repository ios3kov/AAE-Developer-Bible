# Audio effects

Обновлено **2026-10-01** по Adobe After Effects SDK **25.6 build 61**.

В присланной поставке audio contract объявлен в `AE_Effect.h`, но source search не нашёл bundled C/C++ effect sample, который реально dispatch-ит `PF_Cmd_AUDIO_RENDER`. Поэтому эта глава отделяет **documented contract** от DSP-рекомендаций и не притворяется проверенным reference implementation.

Source review: [GPU, audio and Custom UI / Drawbot](../18-SDK-HEADER-TOOLS/15-GPU-AUDIO-CUSTOM-UI-SDK25.6.md).

## 1. Audio — отдельный selector path

SDK определяет:

- `PF_Cmd_AUDIO_SETUP`;
- `PF_Cmd_AUDIO_RENDER`;
- `PF_Cmd_AUDIO_SETDOWN`.

Это не «PF_Cmd_RENDER, только dataP указывает на samples».

Для audio commands `PF_InData` и `PF_OutData` имеют отдельные sample ranges/worlds.

## 2. Как объявить тип audio effect

В Global Setup есть отдельные semantics flags:

### AUDIO_EFFECT_TOO

Effect обрабатывает video и также фильтрует audio.

### AUDIO_EFFECT_ONLY

Effect только audio.

### AUDIO_FLOAT_ONLY

Просит только `PF_SIGNED_FLOAT`; требует один из двух audio-effect flags выше.

### AUDIO_IIR

Output текущего времени зависит от предыдущего output. Это принципиальное отличие stateful filter от stateless block transform.

### I_SYNTHESIZE_AUDIO

Effect может генерировать звук даже из silence.

Нельзя включать эти flags «для совместимости»: они описывают реальную семантику host scheduling.

## 3. PF_SoundWorld

В 25.6 SoundWorld содержит:

```text
format info:
  rate
  mono/stereo
  PCM/float format
  sample size

num_samples
data pointer
```

Declared formats включают unsigned PCM, signed PCM и signed float; sample-size enum содержит 1/2/4 bytes; channel enum — mono/stereo.

Это формат буфера, а не high-level audio file format.

## 4. Audio checkout

Interact callback family включает:

```text
checkout_layer_audio(...)
checkin_layer_audio(...)
get_audio_data(...)
```

Checkout запрашивает:

- parameter/layer index;
- start time;
- duration;
- time scale;
- rate;
- bytes/sample;
- channels;
- signedness.

Полученный layer audio нужно checkin по соответствующему API.

Нельзя сохранять raw audio pointer за пределами его documented lifetime.

## 5. Random access важнее привычного streaming мышления

After Effects — timeline host. Нельзя предполагать:

```text
sample 0
then sample 1
then sample 2
...
```

Host может:

- прыгать во времени;
- повторно запрашивать диапазон;
- отменять расчёт;
- менять preview/render order.

Stateless DSP должен зависеть только от declared input range/parameters.

Для stateful IIR/delay нужен отдельный design под host scheduling. Сам флаг AUDIO_IIR не является реализацией history management.

## 6. Setup / render / setdown responsibility

Рекомендуемое разделение:

```text
AUDIO_SETUP
  derive requested range / format policy
  prepare command-local or lifecycle state

AUDIO_RENDER
  validate format/range
  process exactly requested samples
  report produced range/world

AUDIO_SETDOWN
  release audio-command resources
```

Точные поля надо брать из target SDK при реализации. Эта глава не заменяет compiler-checked sample.

## 7. Numerical policy

До кода определить:

- float scale;
- clipping/saturation;
- NaN/Inf handling для float;
- integer conversion/rounding;
- mono↔stereo policy;
- silence representation;
- denormal/subnormal policy;
- deterministic behavior after seeks.

Не переносите pixel clamp rules в audio автоматически.

## 8. Stateful DSP

Для filter/delay/reverb задайте явно:

- сколько history нужно;
- от какого timeline interval оно зависит;
- как переживается random seek;
- что происходит при parameter change;
- какой state persistent, какой per-request;
- как state синхронизируется при concurrent requests.

Если алгоритм может быть рассчитан из расширенного input window без hidden previous-output state, это часто проще для deterministic host integration. Но конкретная стратегия зависит от API и алгоритма.

## 9. Test matrix

Минимум:

- mono/stereo;
- declared sample rates;
- each supported sample format;
- silence;
- impulse;
- sine with known amplitude/frequency;
- empty/short range;
- odd sample counts;
- random seeks;
- repeated same range;
- parameter automation around block boundary;
- cancellation;
- save/reopen if persistent state exists.

Для IIR отдельно сравнивать sequential и non-linear timeline requests.

## 10. Что SDK 25.6 здесь не подтверждает

В поставке не найден bundled audio effect implementation, поэтому source review **не подтверждает**:

- конкретный AUDIO_SETUP field algorithm;
- production IIR state strategy;
- actual host block size;
- sequencing guarantees;
- sample-perfect behavior after seek;
- MFR/audio relationship.

Эти пункты требуют compiler/host fixture.

## Verification boundary

Новый audio effect не создавался и AE audio render не выполнялся. Gate 6/7 остаются открытыми.
