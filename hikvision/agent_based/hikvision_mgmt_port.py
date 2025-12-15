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
# HIKVISION . MANAGEMENT TCP PORT
###############################################################################

def parse_hikvision_mgmt_port(string_table):
    if not string_table or not string_table[0]:
        return None

    try:
        return int(string_table[0][0])
    except ValueError:
        return None


snmp_section_hikvision_mgmt_port = SimpleSNMPSection(
    name="hikvision_mgmt_port",
    detect=startswith(".1.3.6.1.2.1.1.1.0", "Hikvision"),
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.50001.1",
        oids=[
            "2.0",  # hikManagementTcpPort
        ],
    ),
    parse_function=parse_hikvision_mgmt_port,
)


def discover_hikvision_mgmt_port(section):
    if section is not None:
        yield Service()


def check_hikvision_mgmt_port(section):
    if section is None:
        yield Result(
            state=State.UNKNOWN,
            summary="No SNMP data for management port",
        )
        return

    yield Result(
        state=State.OK,
        summary=f"Management TCP port: {section}",
    )


check_plugin_hikvision_mgmt_port = CheckPlugin(
    name="hikvision_mgmt_port",
    sections=["hikvision_mgmt_port"],
    service_name="Hikvision NVR Management Port",
    discovery_function=discover_hikvision_mgmt_port,
    check_function=check_hikvision_mgmt_port,
)
