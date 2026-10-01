# After Effects → AEGP

AEGP modules register capabilities/hooks during initialization, then After Effects calls those registered callbacks as host events occur.

## Initialization

The supplied SDK 25.6 current header defines the AEGP plug-in initializer in the shape:

~~~cpp
A_Err EntryPointFunc(
    SPBasicSuite* pica_basicP,
    A_long major_version,
    A_long minor_version,
    AEGP_PluginID plugin_id,
    AEGP_GlobalRefcon* global_refcon);
~~~

Use the exact typedef/header from the SDK being compiled.

The supplied archive also contains historical sample code with an older initializer shape. Sample workflow is useful evidence; the current header remains the ABI signature source of truth.

## Initialization responsibilities

Typical work:

- validate required input pointers;
- store plug-in ID;
- resolve required suites;
- register hooks/specializations;
- allocate product global state;
- publish global refcon only when its lifetime is safe;
- establish shutdown/death cleanup.

Avoid unrelated heavy work such as network login or expensive project scans during initialization.

## Host callbacks

Depending on registered capability, AE can later call:

- command hook;
- update-menu hook;
- idle hook;
- death hook;
- notification hooks;
- panel callbacks;
- AEIO callbacks;
- Artisan callbacks;
- other documented specialization callbacks.

Each callback has its own parameter, ownership and threading contract.

Do not write one generic callback assumption for all AEGP APIs.

## Global refcon

The global refcon is a convenient pointer-sized product state connection between initialization and callbacks.

Its safety rules:

- state must exist before callbacks use it;
- partially registered callbacks must not point at freed state;
- shutdown must stop users before deleting state;
- no worker may retain it after teardown;
- C++ exception must not cross the callback ABI.

## Partial registration is a real state

Consider:

~~~text
death hook registered
→ menu command inserted
→ command hook registration fails
~~~

If there is no documented unregister path for earlier steps, deleting state immediately can create a use-after-free later.

Design initialization as a state machine with explicit partial-failure policy.

The Bible MenuTool keeps valid state for already-registered callbacks and disables the command when later registration fails.

## Suite use

AEGP callbacks usually access host services through PICA suites.

Rules:

- exact suite name/version;
- check acquisition/access result;
- release where the acquisition contract requires it;
- do not keep pointers beyond host/suite lifetime;
- do not assume all suite functions are thread-safe.

Use the supplied SDK header for suite generation.

## Load-order rule for third-party providers

AE does not promise a convenient load order for independently shipped plug-ins.

If another module publishes a PICA suite:

~~~text
consumer initialization
→ provider may not yet be available
~~~

For optional dependencies, acquire on use and degrade gracefully.

For required dependencies, detect absence explicitly and show a precise diagnostic/recovery path.

Do not dereference a cached null provider table.

## Thread boundary

Project/UI mutations should be treated as host/main-thread work unless a specific API explicitly documents otherwise.

One documented Utility Suite function may be safe from another thread; that does not make the whole suite safe.

See [threading boundaries](08-THREADING-BOUNDARIES.md).

## Error boundary

Each callback should:

1. validate refcon/inputs;
2. acquire resources;
3. perform operation;
4. cleanup;
5. return A_Err.

C++ exceptions stay inside the module.

Use a consistent callback guard/error mapping where appropriate.

## Shutdown

Death/shutdown path should:

~~~text
stop accepting new work
→ signal/cancel product workers
→ release product-owned host resources
→ release provider acquisitions
→ destroy state
~~~

No static destructor should call AE after host suite teardown.

## Testing

- initialization success;
- missing required suite;
- optional suite absent;
- hook-registration failure at each step;
- callback with missing/invalid state;
- repeated command/idle callback;
- project close/open;
- provider missing;
- AE shutdown;
- worker active during shutdown;
- restart.

## Verification boundary

This chapter describes the reviewed AEGP lifecycle, including a known legacy/current initializer version boundary. Exact callbacks and suite versions must still be compiled and tested against the declared target SDK/AE host.
