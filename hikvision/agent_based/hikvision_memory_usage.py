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
# SNMP SECTION
###############################################################################

def parse_hikvision_memory_usage(string_table):
    if not string_table or not string_table[0]:
        return None

    try:
        value = int(string_table[0][0])
        if 0 <= value <= 100:
            return value
    except ValueError:
        pass

    return None


snmp_section_hikvision_memory_usage = SimpleSNMPSection(
    name="hikvision_memory_usage",
    detect=startswith(".1.3.6.1.2.1.1.1.0", "Hikvision"),
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.50001.1",
        oids=["221.0"],
    ),
    parse_function=parse_hikvision_memory_usage,
)

###############################################################################
# DISCOVERY
###############################################################################

def discover_hikvision_memory_usage(section):
    if section is not None:
        yield Service()

###############################################################################
# CHECK
###############################################################################

def check_hikvision_memory_usage(params, section):
    if section is None:
        yield Result(State.UNKNOWN, "No SNMP data")
        return

    warn, crit = params["levels"]

    if section >= crit:
        state = State.CRIT
    elif section >= warn:
        state = State.WARN
    else:
        state = State.OK

    yield Result(
        state=state,
        summary=f"Memory usage: {section} %",
    )

###############################################################################
# PLUGIN REGISTRATION
###############################################################################

check_plugin_hikvision_memory_usage = CheckPlugin(
    name="hikvision_memory_usage",
    sections=["hikvision_memory_usage"],
    service_name="Hikvision Memory Usage",
    discovery_function=discover_hikvision_memory_usage,
    check_function=check_hikvision_memory_usage,
    check_default_parameters={
        "levels": (80.0, 90.0),
    },
    check_ruleset_name="hikvision_memory_usage",
)
