#!/usr/bin/env python3

from cmk.agent_based.v2 import (
    CheckPlugin,
    CheckResult,
    startswith,
    DiscoveryResult,
    Result,
    Service,
    SimpleSNMPSection,
    SNMPTree,
    State,
    StringTable,
)


def parse_hikvision(string_table):
    return {}

def discover_hikvision(section):
    for line in section:
        yield Service(item=line[1])

def check_hikvision(section):
    yield Result(state=State.OK, summary="Everything is fine")


snmp_section_hikvision_base = SimpleSNMPSection(
    name = "hikvision_base_config",
    parse_function = parse_hikvision,
    detect = startswith(".1.3.6.1.2.1.1.1.0", "Hikvision company products"),
    fetch = SNMPTree(base='1.3.6.1.4.1.50001.1', oids=['1.0','2.0','3.0']),
)


check_plugin_hikvision = CheckPlugin(
    name = "Hikvision_Check",
    sections = [ "hikvision_base_config" ],
    service_name = "Hikvision Check",
    discovery_function = discover_hikvision,
    check_function = check_hikvision,
)