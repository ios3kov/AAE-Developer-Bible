#pragma once
using SPErr = int;
struct SPBasicSuite {
    SPErr (*AcquireSuite)(const char*, long, const void**);
    SPErr (*ReleaseSuite)(const char*, long);
};
