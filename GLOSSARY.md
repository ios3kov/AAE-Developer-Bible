# Glossary

- **Effect plug-in** — native C/C++ effect loaded by AE; receives command selectors and renders image/audio output.
- **AEGP** — After Effects General Plug-in; broad host integration using PICA suites and registered hooks.
- **AEIO** — import/export plug-in implemented as an AEGP specialization.
- **Artisan** — custom renderer for AE 3D layer environment; advanced and rarely appropriate.
- **PICA suite** — versioned group of host callbacks/functions acquired from After Effects.
- **PiPL** — Plug-In Property List; resource metadata used by Adobe hosts when discovering/loading native plug-ins.
- **SmartFX** — effect rendering model that supports smarter region requests and 32-bpc workflows.
- **MFR** — Multi-Frame Rendering; AE can render multiple frames concurrently.
- **Compute Cache** — SDK mechanism for caching expensive computations safely across renders.
- **PF_EffectWorld** — pixel buffer descriptor used by effects.
- **sequence_data** — per-effect-instance state, with strict lifecycle/threading rules.
- **global_data** — plug-in-global state managed through global setup/setdown.
- **Drawbot** — Adobe drawing abstraction used for custom effect UI.
- **ExtendScript** — Adobe's legacy JavaScript dialect/runtime used for AE scripting.
- **ScriptUI** — UI toolkit available to ExtendScript scripts.
- **CEP** — Chromium/HTML/JS-based Creative Cloud extensibility platform; legacy and on a retirement path.
- **UXP** — Adobe's newer extensibility platform replacing CEP over time.
- **Universal binary** — macOS binary containing Intel x86_64 and Apple Silicon arm64 slices.
- **MFR-safe** — implementation proven safe under concurrent frame rendering, not merely one that compiles with the flag enabled.

## Ownership, persistence и геометрия

- **Borrowed** — доступ без права уничтожения; срок задаёт API, а не наличие pointer.
- **Owned** — caller отвечает за соответствующий dispose/checkin или явную передачу.
- **Adoption** — successful API передаёт объект host/project; прежний caller больше не dispose-ит его.
- **Receipt** — токен ограниченного доступа к rendered frame/cache value; не собственность на world/value.
- **Disk ID** — стабильная identity сохраняемого параметра; UI index и arbitrary type ID отдельны.
- **Flatten** — перевод state в сохраняемые bytes; legacy sequence flatten и independent flattened copy имеют разные ownership transitions.
- **Wire schema** — explicit encoding/version/length/range policy, не ABI layout C++ struct.
- **Snapshot** — неизменяемый набор значений для операции; borrowed pointers не становятся long-lived копиями.
- **ROI** — requested region; не фактический allocation и не max output extent.
- **Halo** — соседние input samples, нужные для output ROI пространственного kernel.
- **Origin** — начало coordinate space буфера относительно layer/output; не byte stride.
- **Rowbytes/stride** — переход между строками памяти; может отличаться от dense pixel width.
- **PAR** — pixel aspect ratio; display geometry и buffer indexing различаются.
- **Comp time / layer time** — разные timebases; `A_Time` хранит rational value/scale, не универсальный frame index.
- **Premultiplied / straight alpha** — RGB содержит/не содержит multiplication by alpha; file export representation проверяется отдельно от effect world.
- **Separated dimensions** — leader/follower streams; follower и leader не interchangeable handles.

## Проверки и публикация

- **Artifact identity** — bytes/hash + build metadata; source commit сам не идентифицирует установленный binary.
- **Loaded-image identity** — реально загруженный module path/UUID/symbol identity; install intent не доказательство загрузки.
- **Calibration** — контроль всей observation/output цепочки известным input до оценки алгоритма.
- **Bitwise parity** — equality представления; signed zero/NaN policy отличается от numerical tolerance.
- **Matched-toolchain control** — unchanged source rebuilt с matching settings; отдельное сравнение от original artifact.
- **BLOCKED / NOT_RUN** — prerequisites мешают test / test не выполнен; ни один статус не PASS.
- **PROJECT-REPORTED / USER-REPORTED** — результат из named project record / сообщения пользователя, не независимый Bible runtime.
- **Non-reproduction** — failure не повторён в указанной серии; не causal fix и не broad stability proof.
- **Undo group / compensation** — grouping history / explicit обратные операции; grouping не atomic rollback.
- **Generation / correlation ID** — freshness version / привязка ответа к запросу; совпадение ID само не обеспечивает идемпотентность mutation.
- **Freeze** — фиксируемая редакция с reviewed source и reproducible generated outputs; не product host certification.
- **Eligibility / execution failure** — backend допустим для выбора / уже начатая операция отказала; второе не гарантирует автоматический CPU retry.
- **Source content digest** — hash paths/bytes исходников без generated outputs; не commit SHA и не installed binary identity.
- **Candidate / submitted / final artifact** — этапы release bytes; signing/stapling/repackaging могут менять hash, поэтому цепочка сохраняется отдельно.
- **Confidence / status / disposition** — достоверность вывода / результат проверки / принятое решение; accepted risk не превращает FAIL в PASS.
- **FIXED / NOT_PLANNED** — подтверждённое исправление с regression evidence / решение не исправлять; non-reproduction само не FIXED.
