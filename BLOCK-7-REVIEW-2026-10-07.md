# Block 7 — SmartFX space/time

Authored numeric spatial and temporal workflows added to existing SDK-reviewed
SmartFX contract: half-open ROI, halo, actual origin/stride, max bounds independent
of ROI, downsample/PAR policy, checkout IDs and rational times, empty/error distinction.
Pixel chapter adds calibrated output scope and exceptional-float comparison policy.
Source basis retained: SDK 25.6 AE_Effect.h SmartFX declarations and SmartyPants;
numerical examples are design examples, not vendor sample execution.

Known boundaries: time-remap/motion-blur scheduling not inferred; actual buffer size
not inferred from requested rect; scalar math not a compiled SDK dispatcher.
No new native/AE runtime result. Full-frame/ROI, missing input and cancellation
scenarios are product test specifications, not successful test records.
