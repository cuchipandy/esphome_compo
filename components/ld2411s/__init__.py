import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor, uart
from esphome.const import CONF_ID

DEPENDENCIES = ["uart"]
AUTO_LOAD = ["sensor"]

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

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(LD2411SSensor),
    cv.Optional(CONF_DISTANCE): sensor.sensor_schema(),
    cv.Optional(CONF_PRESENCE): sensor.sensor_schema(),
    cv.Optional(CONF_MOTION): sensor.sensor_schema(),
    cv.Optional(CONF_MAX_MOTION): sensor.sensor_schema(),
    cv.Optional(CONF_MIN_MOTION): sensor.sensor_schema(),
    cv.Optional(CONF_MAX_PRESENCE): sensor.sensor_schema(),
    cv.Optional(CONF_MIN_PRESENCE): sensor.sensor_schema(),
    cv.Optional(CONF_UNOCC_TIME): sensor.sensor_schema(),
}).extend(cv.COMPONENT_SCHEMA).extend(uart.UART_DEVICE_SCHEMA)

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await uart.register_uart_device(var, config)

    for key in [CONF_DISTANCE, CONF_PRESENCE, CONF_MOTION, CONF_MAX_MOTION, CONF_MIN_MOTION, CONF_MAX_PRESENCE, CONF_MIN_PRESENCE, CONF_UNOCC_TIME]:
        if key in config:
            sens = await sensor.new_sensor(config[key])
            cg.add(getattr(var, f"{key}_sensor").set(sens))

