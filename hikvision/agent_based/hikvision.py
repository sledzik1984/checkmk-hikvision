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

########################################
# SYSTEM / MEMORY SECTION (BEZ params)
########################################

def parse_hikvision_system(string_table):
    print(f"DEBUG SYSTEM: string_table={string_table}")  # DEBUG

    if not string_table:
        return None
    row = string_table[0]
    return {
        "device_status": int(row[0]),
        "online": int(row[1]),
        "cpu_num": int(row[2]),
        "mem_usage": int(row[3]),
    }

snmp_section_hikvision_system = SimpleSNMPSection(
    name="hikvision_system",
    detect=startswith(".1.3.6.1.2.1.1.1.0", "Hikvision"),
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.50001.1",
        oids=["230.0", "102.0", "200.0", "221.0"],
    ),
    parse_function=parse_hikvision_system,
)

def discover_hikvision_system(section):
    if section:
        yield Service()

def check_hikvision_system(section):  # . BEZ params!
    if not section:
        return
    if section["online"] != 1:
        yield Result(State.CRIT, "Device offline")
        return
    yield Result(State.OK, f"Device online, CPUs: {section['cpu_num']}, Memory: {section['mem_usage']}%")
    yield Result(State.OK, notice=f"Status code: {section['device_status']}")

check_plugin_hikvision_system = CheckPlugin(
    name="hikvision_system",
    sections=["hikvision_system"],
    service_name="Hikvision System",
    discovery_function=discover_hikvision_system,
    check_function=check_hikvision_system,
)

########################################
# DISK TABLE SECTION (BEZ params)
########################################

def parse_hikvision_disks(string_table):
    print(f"DEBUG DISKS: string_table={string_table}")   # DODAJ

    disks = {}
    for row in string_table:
        index = row[0]
        disks[index] = {
            "volume": row[1],
            "status": int(row[2]),
            "free": int(row[3]),
            "total": int(row[4]),
        }
    return disks

snmp_section_hikvision_disks = SimpleSNMPSection(
    name="hikvision_disks",
    detect=startswith(".1.3.6.1.2.1.1.1.0", "Hikvision"),
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.50001.1.241.1",
        oids=["1", "2", "3", "4", "5"],
    ),
    parse_function=parse_hikvision_disks,
)

def discover_hikvision_disks(section):
    for idx in section:
        yield Service(item=idx)

def check_hikvision_disks(item, section):  # . BEZ params!
    disk = section.get(item)
    if disk is None:
        return
    state = State.OK if disk["status"] == 1 else State.CRIT
    used = disk["total"] - disk["free"]
    used_pct = int((used / disk["total"]) * 100) if disk["total"] > 0 else 0
    yield Result(
        state=state,
        summary=f"Volume {disk['volume']} . {used_pct}% used ({used}/{disk['total']} MB)",
    )

check_plugin_hikvision_disks = CheckPlugin(
    name="hikvision_disks",
    sections=["hikvision_disks"],
    service_name="Hikvision Disk %s",
    discovery_function=discover_hikvision_disks,
    check_function=check_hikvision_disks,
)
