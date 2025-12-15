#!/usr/bin/env python3

from cmk.rulesets.v1 import Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    Float,
    LevelDirection,
    SimpleLevels,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, Topic


def _parameter_form():
    return Dictionary(
        elements={
            "levels": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Memory usage thresholds (%)"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Float(unit_symbol="%"),
                    prefill_fixed_levels=DefaultValue((80.0, 90.0)),
                ),
                required=True,
            ),
        }
    )


rule_spec_hikvision_memory_usage = CheckParameters(
    name="hikvision_memory_usage",
    title=Title("Hikvision Memory Usage"),
    topic=Topic.OPERATING_SYSTEM,
    parameter_form=_parameter_form,
)
