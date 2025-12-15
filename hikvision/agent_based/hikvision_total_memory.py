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
# HIKVISION . TOTAL MEMORY (INTEGER)
###############################################################################

def parse_hikvision_total_memory(string_table):
    if not string_table or not string_table[0]:
        return None

    try:
        return int(string_table[0][0])
    except ValueError:
        return None


snmp_section_hikvision_total_memory = SimpleSNMPSection(
    name="hikvision_total_memory",
    detect=startswith(".1.3.6.1.2.1.1.1.0", "Hikvision"),
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.50001.1",
        oids=[
            "220.0",  # hikTotalMemory
        ],
    ),
    parse_function=parse_hikvision_total_memory,
)


def discover_hikvision_total_memory(section):
    if section is not None:
        yield Service()


def check_hikvision_total_memory(section):
    if section is None:
        yield Result(
            state=State.UNKNOWN,
            summary="No SNMP data for total memory",
        )
        return

    # Nie zgadujemy jednostki . pokazujemy surow. warto...
    yield Result(
        state=State.OK,
        summary=f"Total memory (raw): {section}",
    )


check_plugin_hikvision_total_memory = CheckPlugin(
    name="hikvision_total_memory",
    sections=["hikvision_total_memory"],
    service_name="Hikvision NVR Total Memory",
    discovery_function=discover_hikvision_total_memory,
    check_function=check_hikvision_total_memory,
)
