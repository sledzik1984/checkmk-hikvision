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
# HIKVISION . SYSTEM STATUS (SINGLE SERVICE)
###############################################################################

def parse_hikvision_system(string_table):
    if not string_table:
        return None

    row = string_table[0]

    try:
        return {
            "device_status": int(row[0]),
            "online": int(row[1]),
            "cpu_num": int(row[2]),
            "mem_usage": int(row[3]),
        }
    except (IndexError, ValueError):
        return None


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
    if section is not None:
        yield Service()


def check_hikvision_system(section):
    if section is None:
        yield Result(
            state=State.UNKNOWN,
            summary="No SNMP data received",
        )
        return

    if section["online"] != 1:
        yield Result(
            state=State.CRIT,
            summary="Device offline",
        )
        return

    yield Result(
        state=State.OK,
        summary=(
            f"Online, CPUs: {section['cpu_num']}, "
            f"Memory usage: {section['mem_usage']}%"
        ),
    )

    yield Result(
        state=State.OK,
        notice=f"Device status code: {section['device_status']}",
    )


check_plugin_hikvision_system = CheckPlugin(
    name="hikvision_system_only",
    sections=["hikvision_system_only"],
    service_name="Hikvision NVR System",
    discovery_function=discover_hikvision_system,
    check_function=check_hikvision_system,
)
