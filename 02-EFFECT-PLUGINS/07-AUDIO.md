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

### Анализ audio визуальным эффектом

**Public guide, 2026-10-08: DOCUMENTED / RUNTIME-NOT-CLAIMED.**

Для visual effect, который читает audio, но не изменяет его, guide выделяет
`PF_OutFlag_I_USE_AUDIO`. Модификация audio относится к `AUDIO_EFFECT_TOO` или
`AUDIO_EFFECT_ONLY`. [Источник](https://github.com/docsforadobe/after-effects-plugin-guide/blob/6d9b285d9755d1fbf8ead7680ba49de24f94b547/docs/audio/global-outflags.md)

**Рекомендация:** выбирать flag по результату эффекта, а не по самому наличию
checkout. Spectrum/level analysis и audio filter имеют разные output obligations.

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

### Requested samples не продлевают clip

Checkout/range negotiation не является API продления clip. Для слышимого хвоста
delay guide предлагает заранее продлить out point средствами host или time remap.
[Источник](https://github.com/docsforadobe/after-effects-plugin-guide/blob/6d9b285d9755d1fbf8ead7680ba49de24f94b547/docs/audio/accessing-audio-data.md)

**Рекомендация:** объяснить эту предпосылку пользователю эффекта. Запрос дополнительных
samples для расчёта и изменение доступной длительности output решают разные задачи;
не обещать tail за границей clip только из-за большего входного диапазона.

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

### Automation metadata и фактический audio format

`PF_FSliderDef` содержит audio-specific phase/curve-tolerance поля;
`PF_FSliderFlag_WANT_PHASE` запрашивает phase data. Это часть host automation,
не самостоятельный DSP sample clock. [Источник](https://github.com/docsforadobe/after-effects-plugin-guide/blob/6d9b285d9755d1fbf8ead7680ba49de24f94b547/docs/audio/audio-specific-float-slider-variables.md)

Sample rate и bit depth независимы, а выход после audio effect ещё может быть
преобразован host. Поэтому формат входного SoundWorld не описывает автоматически
финальный output file. [Источники](https://github.com/docsforadobe/after-effects-plugin-guide/blob/6d9b285d9755d1fbf8ead7680ba49de24f94b547/docs/audio/audio-considerations.md), [структуры](https://github.com/docsforadobe/after-effects-plugin-guide/blob/6d9b285d9755d1fbf8ead7680ba49de24f94b547/docs/audio/audio-data-structures.md)

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

Заявления о фактическом поведении продукта требуют отдельной compiler/host evidence; это не условие редакционной готовности главы.

## Bounded stateless DSP walkthrough

Concrete **DSP example**, not an AUDIO_RENDER dispatcher: gain=0.5, mono/stereo
interleaved float32 buffer, finite inputs only, output same channels/rate/count.
Validate format is PF_SIGNED_FLOAT, sample_size is **4 bytes**, count/channels and
overflow before accessing memory. Define sample index separately from channel:
`offset = frameIndex*channelCount + channelIndex`; at 48 kHz a 480-frame stereo
block contains 960 scalar components and 3840 bytes. Layout must match the exact
host audio-data contract, not merely this assumed DSP input representation.

For each scalar `out[i]=0.5f*in[i]`; no history, clipping, resampling or hidden previous
block. Silence remains zero; sine peak 0.8 becomes 0.4. Product chooses NaN/Inf
reject/sanitize/propagate policy explicitly. Output allocation and host borrowed
input are separate; layer-audio checkout is returned even when later processing
fails. Do not dispose host SoundWorld data as a product allocation.

Setup determines supported format/range from target declarations; render validates
actual input and processes bounded requested samples; setdown releases only owned
request state. Sample count is not seconds; start/duration use their specified
scale. This arithmetic lesson does not establish host block ordering, AUDIO_IIR
history, actual field wiring or sample-perfect automation. Those remain intentionally
limited because no matching bundled AUDIO_RENDER implementation was found.

## Verification boundary

Bible не заявляет собственный audio runtime result. Создание отдельного audio demo effect не является условием редакционной готовности главы.
