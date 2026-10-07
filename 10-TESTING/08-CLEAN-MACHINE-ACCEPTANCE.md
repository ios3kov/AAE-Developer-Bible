# Clean-machine release acceptance

The final product must be tested as a customer receives it, not from the developer build directory.

## What "clean" means

A clean-machine test should avoid hidden dependencies from development:

- no source tree dependency;
- no locally built libraries on PATH/DYLD paths;
- no manually copied debug plug-in;
- no dev signing exception required;
- no stale previous version unless testing upgrade;
- no environment variables that customers do not have.

A fresh VM snapshot or dedicated test machine is ideal.

## Fresh install

Test:

1. obtain the exact release candidate package;
2. verify package hash/signature;
3. install with documented permissions;
4. confirm installed files/path;
5. launch supported AE version;
6. verify load;
7. run smoke scenario;
8. quit/relaunch and repeat critical operation.

## Upgrade

Test at least one supported previous version:

```text
install N-1
 -> create/save representative state
 -> install N
 -> launch AE
 -> verify migration/state
 -> verify feature
 -> uninstall/repair if supported
```

Upgrade must not silently delete user presets, license state or projects unless explicitly designed.

## Multiple AE versions

When installer policy targets shared MediaCore locations, verify behavior with more than one installed AE version.

Record which hosts discover the plug-in and whether that matches the published compatibility matrix.

## Uninstall

Verify:

- owned binaries removed;
- unrelated Adobe plug-ins untouched;
- user data policy respected;
- restart/relaunch state is clean;
- reinstall succeeds.

## macOS acceptance

Check:

- package signature;
- Developer ID signature;
- notarization/Gatekeeper path;
- architecture slices;
- no quarantine/signature error in normal install path;
- load in supported native architecture mode.

## Windows acceptance

Check:

- installer signature;
- plug-in/helper Authenticode signatures;
- expected runtime dependencies;
- SmartScreen/trust behavior as applicable;
- registry/path resolution;
- load in supported architecture.

## Offline behavior

If the product includes account/licensing/update logic, test:

- first launch offline if supported;
- normal offline grace behavior;
- server unavailable;
- DNS/network timeout;
- license server error;
- update server unavailable.

Render behavior should not become nondeterministic because an update/licensing endpoint is temporarily unreachable.

## Permissions

Test expected non-admin/admin paths.

The installer should fail clearly when privileges are insufficient; the plug-in should not attempt privileged writes during ordinary AE rendering.

## Release-candidate identity

The artifact that passes clean-machine acceptance becomes the release candidate identity.

Any change after that — even a tiny binary patch — creates a new candidate and invalidates the previous package-level acceptance.

## Acceptance report

Concrete design routes: [macOS owned-bundle upgrade/rollback](../08-MACOS/06-INSTALLATION-PACKAGING.md)
and [Windows owned-file upgrade/rollback](../09-WINDOWS/06-INSTALLATION-PACKAGING.md).
The [filled plan](../13-TEMPLATES/examples/gain-evidence-plan.json) deliberately has
no candidate or observed hashes. Populate candidate/prior/installed/restored hashes
only from actual artifacts; report recovery separately from failed candidate smoke.
If prior files are unmanaged or changed unexpectedly, the expected result is a
visible conflict, not deletion of all MediaCore or user presets.

Record:

```text
package hash
signature/notarization verification
install result
installed paths
AE load result
smoke-test result
upgrade result
uninstall result
rollback result
known limitations
```

Only after these checks should the release checklist mark clean-machine installation as passed.
