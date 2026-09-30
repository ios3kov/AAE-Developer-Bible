# Minimal Artisan registrar

Status: **host-test-required**.

Artisan replaces parts of AE's 3D rendering path and has a much larger host contract than a normal Effect. Start from the SDK Artisan sample, preserve its registration/function-table plumbing, then replace scene/render code incrementally.

See `05-ARTISAN/README.md` and `14-NATIVE-INTEGRATIONS/09-ARTISAN.md` for lifecycle, callbacks and ownership. The Bible does not pretend that a registrar stub alone is a "working renderer".
