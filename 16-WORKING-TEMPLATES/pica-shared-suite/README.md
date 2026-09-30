# Published PICA suite contract

Status: **ABI template**; wire provider/registration calls using the current SDK Sweetie sample / SP suite APIs.

`SharedSuite.h` is intentionally C-ABI-shaped: no STL, no exceptions, explicit buffer ownership.

## Provider requirements

- register `BIBLE_CORE_SUITE_NAME`, version 1;
- function table must stay valid for the advertised lifetime;
- return integer error codes, never throw across call boundary;
- validate every pointer/size.

## Consumer requirements

- acquire by exact name+version through `SPBasicSuite`;
- if missing, disable dependent feature cleanly;
- release after use;
- never cache a pointer beyond the provider/suite lifetime guarantee.

Reference sample: Adobe SDK **Sweetie**, which demonstrates publishing a PICA function suite for other plug-ins.
