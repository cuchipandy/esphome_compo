import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor, uart
from esphome.const import (
    UNIT_CENTIMETER,
    UNIT_EMPTY,
    ICON_MOTION_SENSOR,
    ICON_RADAR,
    ICON_TIMER,
    DEVICE_CLASS_DISTANCE,
    DEVICE_CLASS_PRESENCE,
    STATE_CLASS_MEASUREMENT,
)

CODEOWNERS = ["@cuchipandy"]

DEPENDENCIES = ["uart"]

ld2411s_ns = cg.esphome_ns.namespace("ld2411s")
LD2411SSensor = ld2411s_ns.class_("LD2411SSensor", cg.Component, uart.UARTDevice)

CONF_DISTANCE = "distance"
CONF_PRESENCE = "presence"
CONF_MOTION = "motion"
CONF_MAX_MOTION = "max_motion"
CONF_MIN_MOTION = "min_motion"
CONF_MAX_PRESENCE = "max_presence"
CONF_MIN_PRESENCE = "min_presence"
CONF_UNOCC_TIME = "unocc_time"

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(LD2411SSensor),
        cv.Optional(CONF_DISTANCE): sensor.sensor_schema(
            unit_of_measurement=UNIT_CENTIMETER,
            icon=ICON_RADAR,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_DISTANCE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_PRESENCE): sensor.sensor_schema(
            unit_of_measurement=UNIT_EMPTY,
            icon=ICON_MOTION_SENSOR,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_PRESENCE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_MOTION): sensor.sensor_schema(
            unit_of_measurement=UNIT_EMPTY,
            icon=ICON_MOTION_SENSOR,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_PRESENCE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_MAX_MOTION): sensor.sensor_schema(
            unit_of_measurement=UNIT_CENTIMETER,
            icon=ICON_RADAR,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_DISTANCE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_MIN_MOTION): sensor.sensor_schema(
            unit_of_measurement=UNIT_CENTIMETER,
            icon=ICON_RADAR,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_DISTANCE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_MAX_PRESENCE): sensor.sensor_schema(
            unit_of_measurement=UNIT_CENTIMETER,
            icon=ICON_RADAR,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_DISTANCE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_MIN_PRESENCE): sensor.sensor_schema(
            unit_of_measurement=UNIT_CENTIMETER,
            icon=ICON_RADAR,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_DISTANCE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_UNOCC_TIME): sensor.sensor_schema(
            unit_of_measurement=UNIT_EMPTY,
            icon=ICON_TIMER,
            accuracy_decimals=1,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
    }
).extend(uart.UART_DEVICE_SCHEMA).extend(cv.COMPONENT_SCHEMA)

async def to_code(config):
    var = cg.new_Pvariable(config[cv.GenerateID()])
    await cg.register_component(var, config)
    await uart.register_uart_device(var, config)

    for key, sensor_var in [
        (CONF_DISTANCE, "distance_sensor"),
        (CONF_PRESENCE, "presence_sensor"),
        (CONF_MOTION, "motion_sensor"),
        (CONF_MAX_MOTION, "max_motion_sensor"),
        (CONF_MIN_MOTION, "min_motion_sensor"),
        (CONF_MAX_PRESENCE, "max_presence_sensor"),
        (CONF_MIN_PRESENCE, "min_presence_sensor"),
        (CONF_UNOCC_TIME, "unocc_time_sensor"),
    ]:
        if key in config:
            sens = await sensor.new_sensor(config[key])
            cg.add(getattr(var, sensor_var).set(sens))
