#include <iostream>

#include <dcmtk/config/osconfig.h>

int main()
{
    std::cout << "dcmtk version: " << PACKAGE_VERSION;
    return 0;
}
