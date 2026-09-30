#include "AEConfig.h"
#include "entry.h"
#include "AE_GeneralPlug.h"
#include "AEGP_SuiteHandler.h"

struct ToolState {
    SPBasicSuite* pica = nullptr;
    AEGP_PluginID plugin_id = 0;
    AEGP_Command command = 0;
};

static A_Err DoWork(ToolState* s) {
    AEGP_SuiteHandler suites(s->pica);
    suites.UtilitySuite6()->AEGP_ReportInfo(s->plugin_id, "AE Developer Bible menu tool is alive.");
    return A_Err_NONE;
}

static A_Err CommandHook(
    AEGP_GlobalRefcon plugin_refcon,
    AEGP_CommandRefcon,
    AEGP_Command command,
    AEGP_HookPriority,
    A_Boolean already_handledB,
    A_Boolean* handledPB)
{
    auto* s = reinterpret_cast<ToolState*>(plugin_refcon);
    if (!s || already_handledB || command != s->command) {
        return A_Err_NONE;
    }

    A_Err err = DoWork(s);
    if (!err && handledPB) {
        *handledPB = TRUE;
    }
    return err;
}


static A_Err DeathHook(AEGP_GlobalRefcon plugin_refcon, AEGP_DeathRefcon) {
    auto* s = reinterpret_cast<ToolState*>(plugin_refcon);
    delete s;
    return A_Err_NONE;
}

static A_Err UpdateMenuHook(AEGP_GlobalRefcon plugin_refcon, AEGP_UpdateMenuRefcon, AEGP_WindowType) {
    auto* s = reinterpret_cast<ToolState*>(plugin_refcon);
    if (!s) return A_Err_NONE;
    AEGP_SuiteHandler suites(s->pica);
    return suites.CommandSuite1()->AEGP_EnableCommand(s->command);
}

extern "C" DllExport
A_Err EntryPointFunc(
    SPBasicSuite* pica_basicP,
    A_long,
    A_long,
    AEGP_PluginID aegp_plugin_id,
    AEGP_GlobalRefcon* global_refconP)
{
    auto* s = new ToolState{};
    s->pica = pica_basicP;
    s->plugin_id = aegp_plugin_id;

    AEGP_SuiteHandler suites(pica_basicP);
    A_Err err = suites.CommandSuite1()->AEGP_GetUniqueCommand(&s->command);
    if (!err) {
        err = suites.CommandSuite1()->AEGP_InsertMenuCommand(
            s->command,
            "Bible Native Tool",
            AEGP_Menu_WINDOW,
            AEGP_MENU_INSERT_SORTED);
    }
    if (!err) {
        err = suites.RegisterSuite5()->AEGP_RegisterCommandHook(
            aegp_plugin_id,
            AEGP_HP_BeforeAE,
            s->command,
            CommandHook,
            reinterpret_cast<AEGP_CommandRefcon>(s));
    }
    if (!err) {
        err = suites.RegisterSuite5()->AEGP_RegisterUpdateMenuHook(
            aegp_plugin_id,
            UpdateMenuHook,
            nullptr);
    }
    if (!err) {
        err = suites.RegisterSuite5()->AEGP_RegisterDeathHook(
            aegp_plugin_id,
            DeathHook,
            nullptr);
    }

    if (err) {
        delete s;
        return err;
    }
    *global_refconP = reinterpret_cast<AEGP_GlobalRefcon>(s);
    return A_Err_NONE;
}
