#!/usr/bin/env python3
# Copyright (c) 2020 LunarG, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Author: Mike Weiblen <mikew@lunarg.com>

"""
VulkanVersionUtils.py
Utilities for manipulating Vulkan version data.
A 3-tuple is the native Python representation of a Vulkan vers.
"""

import re
import sys

#############################################################################

def GetVulkanHeaderVersion(filename):
    '''
    Scan a Vulkan header file to extract its complete (major.minor.patch) version.
    Returns the version as a 3-tuple, or None if the header does not contain necessary info.
    Will assert if the file's version data is not formatted as expected.
    '''
    with open(filename) as file:
        regex1 = re.compile(r'\bVK_HEADER_VERSION\s+(\d+)')
        regex2 = re.compile(r'\bVK_HEADER_VERSION_COMPLETE\s+VK_MAKE_VERSION\((\d+),\s*(\d+),\s*(\w+)\)')
        regex3 = re.compile(r'\bVK_API_VERSION_(\d+)_(\d+)\s+VK_MAKE_VERSION\((\d+),\s*(\d+),\s*(\d+)\)')
        patch_version = None
        version_complete = None
        api_version = None

        for line in file:
            if line.startswith('#define'):
                m = regex1.search(line)
                if m:
                    assert not patch_version
                    patch_version = int(m.group(1))
                    continue

                m = regex2.search(line)
                if m:
                    assert not version_complete
                    assert m.group(3) == 'VK_HEADER_VERSION'
                    version_complete = (int(m.group(1)), int(m.group(2)))
                    continue

                m = regex3.search(line)
                if m:
                    assert m.group(3) == m.group(1)
                    assert m.group(4) == m.group(2)
                    assert m.group(5) == '0'
                    x = (int(m.group(3)), int(m.group(4)))
                    if not api_version or x > api_version:
                        api_version = x
                    continue

    result = None
    if not patch_version:
        pass
    elif version_complete:
        result = version_complete + (patch_version,)
    elif api_version:
        result = api_version + (patch_version,)

    return result

# conversions between several representations ###############################

def VulkanVersionFromStr(str_value):
    '''TODO : from '1.2.3' dotted str to tuple'''
    return (0,0,0)

def VulkanVersionToStr(ver):
    '''from tuple to '1.2.3' dotted str'''
    return "%d.%d.%d" % ver

def VulkanVersionFromInt(int_value):
    '''TODO : from int32 to tuple'''
    return (0,0,0)

def VulkanVersionToInt(int_value):
    '''TODO : from tuple to int32'''
    return 0x12345678

# testing ###################################################################

def test():
    ver = GetVulkanHeaderVersion('/home/mikew/repos/gits/github.com/KhronosGroup/Vulkan-Headers/include/vulkan/vulkan_core.h')
    print("tuple:", ver)
    print("dotted: %d.%d.%d" % ver)

    ver = GetVulkanHeaderVersion(sys.argv[0])
    if not ver: ver = (0,0,0)
    print("tuple:", ver)
    print("dotted: %d.%d.%d" % ver)

    ver = GetVulkanHeaderVersion('non-exist.txt')
    print("tuple:", ver)
    print("dotted: %d.%d.%d" % ver)

# main ######################################################################

def main():
    assert len(sys.argv) == 2, "usage: %s [filename]" % sys.argv[0]
    ver = GetVulkanHeaderVersion(sys.argv[1])
    if not ver:
        ver = (0,0,0)
    print(VulkanVersionToStr(ver))

if __name__ == '__main__':
    main()

# vim: set sw=4 ts=8 et ic ai:
