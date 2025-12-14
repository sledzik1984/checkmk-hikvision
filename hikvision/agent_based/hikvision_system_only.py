#!/usr/bin/env python3

from cmk.agent_based.v2 import (
    CheckPlugin,
    Result,
    Service,
    SimpleSNMPSection,
    SNMPTree,
    State,
    startswith,
)

###############################################################################
# SYSTEM ONLY . MINIMAL TEST PLUGIN
###############################################################################

def parse_hikvision_system(string_table):
    if not string_table:
        return {}

    row = string_table[0]
    return {
        "device_status": int(row[0]),
        "online": int(row[1]),
        "cpu_num": int(row[2]),
        "mem_usage": int(row[3]),
    }


snmp_section_hikvision_system = SimpleSNMPSection(
    name="hikvision_system_only",
    detect=startswith(".1.3.6.1.2.1.1.1.0", "Hikvision"),
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.50001.1",
        oids=[
            "230.0",  # hikDeviceStatus
            "102.0",  # hikOnline
            "200.0",  # hikCPUNum
            "221.0",  # hikMemoryUsage
        ],
    ),
    parse_function=parse_hikvision_system,
)


def discover_hikvision_system(section):
    yield Service()


def check_hikvision_system(section):
    if not section:
        return

    if section["online"] != 1:
        yield Result(State.CRIT, "Device offline")
        return

    yield Result(
        State.OK,
        summary=(
            f"Online, CPUs: {section['cpu_num']}, "
            f"Memory usage: {section['mem_usage']}%"
        ),
    )

    yield Result(
        State.OK,
        notice=f"Device status code: {section['device_status']}",
    )


check_plugin_hikvision_system = CheckPlugin(
    name="hikvision_system_only",
    sections=["hikvision_system_only"],
    service_name="Hikvision System (test)",
    discovery_function=discover_hikvision_system,
    check_function=check_hikvision_system,
)
