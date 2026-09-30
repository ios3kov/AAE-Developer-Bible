#include "AEConfig.h"
#include "entry.h"
#include "AE_GeneralPlug.h"
#include "AEGP_SuiteHandler.h"
#include "../../19-NATIVE-CODE-FOUNDATION/code/HostCallbackGuard.h"
#include <memory>

struct ToolState {
    SPBasicSuite* pica = nullptr;
    AEGP_PluginID plugin_id = 0;
    AEGP_Command command = 0;
};

static A_Err DoWork(ToolState* s) {
    AEGP_SuiteHandler suites(s->pica);
    return suites.UtilitySuite6()->AEGP_ReportInfo(s->plugin_id, "AE Developer Bible menu tool is alive.");
}

static A_Err CommandHook(
    AEGP_GlobalRefcon plugin_refcon,
    AEGP_CommandRefcon,
    AEGP_Command command,
    AEGP_HookPriority,
    A_Boolean already_handledB,
    A_Boolean* handledPB)
{
    return GuardAeHostCallback([&]() -> A_Err {
    auto* s = reinterpret_cast<ToolState*>(plugin_refcon);
    if (!s || !s->command || already_handledB || command != s->command) {
        return A_Err_NONE;
    }

    A_Err err = DoWork(s);
    if (!err && handledPB) {
        *handledPB = TRUE;
    }
    return err;
    }, A_Err_GENERIC);
}


static A_Err DeathHook(AEGP_GlobalRefcon plugin_refcon, AEGP_DeathRefcon) {
    return GuardAeHostCallback([&]() -> A_Err {
    auto* s = reinterpret_cast<ToolState*>(plugin_refcon);
    delete s;
    return A_Err_NONE;
    }, A_Err_GENERIC);
}

static A_Err UpdateMenuHook(AEGP_GlobalRefcon plugin_refcon, AEGP_UpdateMenuRefcon, AEGP_WindowType) {
    return GuardAeHostCallback([&]() -> A_Err {
    auto* s = reinterpret_cast<ToolState*>(plugin_refcon);
    if (!s || !s->command) return A_Err_NONE;
    AEGP_SuiteHandler suites(s->pica);
    return suites.CommandSuite1()->AEGP_EnableCommand(s->command);
    }, A_Err_GENERIC);
}

extern "C" DllExport
A_Err EntryPointFunc(
    SPBasicSuite* pica_basicP,
    A_long,
    A_long,
    AEGP_PluginID aegp_plugin_id,
    AEGP_GlobalRefcon* global_refconP)
{
    return GuardAeHostCallback([&]() -> A_Err {
    if (!pica_basicP || !global_refconP) return A_Err_PARAMETER;
    *global_refconP = nullptr;
    auto owner = std::make_unique<ToolState>();
    auto* s = owner.get();
    s->pica = pica_basicP;
    s->plugin_id = aegp_plugin_id;

    AEGP_SuiteHandler suites(pica_basicP);
    // Resolve throwing acquisitions before registration. Keep state alive after
    // registering any callback: AE offers no general unregister-hooks rollback.
    auto* registration = suites.RegisterSuite5();
    auto* commands = suites.CommandSuite1();
    auto* utility = suites.UtilitySuite6();
    A_Err err = registration->AEGP_RegisterDeathHook(aegp_plugin_id, DeathHook, nullptr);
    if (err) return err;
    *global_refconP = reinterpret_cast<AEGP_GlobalRefcon>(owner.release());
    err = commands->AEGP_GetUniqueCommand(&s->command);
    if (!err) {
        err = commands->AEGP_InsertMenuCommand(
            s->command,
            "Bible Native Tool",
            AEGP_Menu_WINDOW,
            AEGP_MENU_INSERT_SORTED);
    }
    if (!err) {
        err = registration->AEGP_RegisterCommandHook(
            aegp_plugin_id,
            AEGP_HP_BeforeAE,
            s->command,
            CommandHook,
            nullptr);
    }
    if (!err) {
        err = registration->AEGP_RegisterUpdateMenuHook(
            aegp_plugin_id,
            UpdateMenuHook,
            nullptr);
    }
    if (err) {
        // Retain a valid global refcon for hooks already registered. Keep the
        // partially initialized plug-in resident so DeathHook owns cleanup.
        if (s->command) (void)commands->AEGP_DisableCommand(s->command);
        s->command = 0;
        (void)utility->AEGP_ReportInfo(aegp_plugin_id,
            "Bible Native Tool initialization failed; command disabled.");
        return A_Err_NONE;
    }
    *global_refconP = reinterpret_cast<AEGP_GlobalRefcon>(s);
    return A_Err_NONE;
    }, A_Err_GENERIC);
}
