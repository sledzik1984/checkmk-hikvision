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
# HIKVISION . PRODUCT TYPE
###############################################################################

# Mapowanie enum.w z MIB
_PRODUCT_TYPE_MAP = {
    1: "DVR",
    2: "NVR",
    3: "IPC",
    255: "Unknown",
}


def parse_hikvision_product_type(string_table):
    if not string_table or not string_table[0]:
        return None

    try:
        return int(string_table[0][0])
    except ValueError:
        return None


snmp_section_hikvision_product_type = SimpleSNMPSection(
    name="hikvision_product_type",
    detect=startswith(".1.3.6.1.2.1.1.1.0", "Hikvision"),
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.50001.1",
        oids=[
            "100.0",  # hikProductType
        ],
    ),
    parse_function=parse_hikvision_product_type,
)


def discover_hikvision_product_type(section):
    if section is not None:
        yield Service()


def check_hikvision_product_type(section):
    if section is None:
        yield Result(
            state=State.UNKNOWN,
            summary="No SNMP data for product type",
        )
        return

    product_name = _PRODUCT_TYPE_MAP.get(section, "Unknown")
    state = State.OK if section in (1, 2, 3) else State.WARN

    yield Result(
        state=state,
        summary=f"Product type: {product_name} ({section})",
    )


check_plugin_hikvision_product_type = CheckPlugin(
    name="hikvision_product_type",
    sections=["hikvision_product_type"],
    service_name="Hikvision NVR Product Type",
    discovery_function=discover_hikvision_product_type,
    check_function=check_hikvision_product_type,
)
