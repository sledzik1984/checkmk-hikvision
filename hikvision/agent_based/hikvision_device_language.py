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
# HIKVISION . DEVICE LANGUAGE
###############################################################################

_LANGUAGE_MAP = {
    1: "English",
    2: "Simplified Chinese",
    3: "Traditional Chinese",
    4: "Japanese",
    5: "Korean",
    255: "Unknown",
}


def parse_hikvision_device_language(string_table):
    if not string_table or not string_table[0]:
        return None

    try:
        return int(string_table[0][0])
    except ValueError:
        return None


snmp_section_hikvision_device_language = SimpleSNMPSection(
    name="hikvision_device_language",
    detect=startswith(".1.3.6.1.2.1.1.1.0", "Hikvision"),
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.50001.1",
        oids=[
            "231.0",  # hikDeviceLanguage
        ],
    ),
    parse_function=parse_hikvision_device_language,
)


def discover_hikvision_device_language(section):
    if section is not None:
        yield Service()


def check_hikvision_device_language(section):
    if section is None:
        yield Result(
            state=State.UNKNOWN,
            summary="No SNMP data for device language",
        )
        return

    language = _LANGUAGE_MAP.get(section, "Unknown")
    state = State.OK if section in (1, 2, 3, 4, 5) else State.WARN

    yield Result(
        state=state,
        summary=f"Device language: {language} ({section})",
    )


check_plugin_hikvision_device_language = CheckPlugin(
    name="hikvision_device_language",
    sections=["hikvision_device_language"],
    service_name="Hikvision NVR Device Language",
    discovery_function=discover_hikvision_device_language,
    check_function=check_hikvision_device_language,
)
