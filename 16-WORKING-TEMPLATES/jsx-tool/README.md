# Standalone JSX tool

Status: **source supplied / After Effects host test pending**.

rename-selected-layers.jsx is a complete Script-menu source example.

Integration:

1. place it in the appropriate After Effects Scripts folder for the target installation/user setup;
2. restart AE if required by that script location;
3. open a composition;
4. select one or more layers;
5. run the script.

Pattern demonstrated:

- validate project/composition/selection before mutation;
- open one undo group only around the mutation;
- keep the command logic independent of persistent global state;
- contain errors at the script entry boundary.

The source is intended to be directly runnable, but the repository does not call it host-verified until an actual AE/OS execution is recorded.
