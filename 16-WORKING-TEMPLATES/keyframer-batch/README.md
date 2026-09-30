# Keyframer batch pattern

Status: **API recipe** for an AEGP based on the official `Easy Cheese` sample.

For many keyframes, do not call independent insert operations in a loop if the batch API fits. Use the Keyframe Suite transaction pattern:

```text
AEGP_StartUndoGroup
  AEGP_StartAddKeyframes(stream)
    for each desired time/value:
      AEGP_AddKeyframes(...time... -> new_index)
      AEGP_SetAddKeyframe(...new_index, value...)
  AEGP_EndAddKeyframes(...)
AEGP_EndUndoGroup
```

This avoids repeatedly pushing the whole stream through undo/update machinery and is the correct architectural starting point for a Keyframe Assistant tool.

Before modifying:
- verify the selected stream is keyframe-able;
- read expression state if it matters to the product;
- avoid retaining stream handles across structural project changes.
