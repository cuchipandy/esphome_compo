import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor, uart
from esphome.const import CONF_ID, CONF_LAMBDA, CONF_SENSORS, UNIT_CENTIMETER, CONF_NAME, CONF_INTERNAL

DEPENDENCIES = ["uart"]
AUTO_LOAD = ["sensor"]

ld2411s_ns = cg.esphome_ns.namespace("ld2411s")
LD2411SSensor = ld2411s_ns.class_("UARTSensor", cg.Component, uart.UARTDevice)

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
    cv.Required(CONF_UART_ID): cv.use_id(uart.UARTComponent),
    cv.Optional(CONF_DISTANCE): sensor.sensor_schema(unit_of_measurement=UNIT_CENTIMETER),
    cv.Optional(CONF_PRESENCE): sensor.sensor_schema(internal=True),
    cv.Optional(CONF_MOTION): sensor.sensor_schema(internal=True),
    cv.Optional(CONF_MAX_MOTION): sensor.sensor_schema(internal=True),
    cv.Optional(CONF_MIN_MOTION): sensor.sensor_schema(internal=True),
    cv.Optional(CONF_MAX_PRESENCE): sensor.sensor_schema(internal=True),
    cv.Optional(CONF_MIN_PRESENCE): sensor.sensor_schema(internal=True),
    cv.Optional(CONF_UNOCC_TIME): sensor.sensor_schema(internal=True),
})

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await uart.register_uart_device(var, config)

    if CONF_DISTANCE in config:
        sens = await sensor.new_sensor(config[CONF_DISTANCE])
        cg.add(var.distance_sensor.set(sens))
    if CONF_PRESENCE in config:
        sens = await sensor.new_sensor(config[CONF_PRESENCE])
        cg.add(var.presence_sensor.set(sens))
    if CONF_MOTION in config:
        sens = await sensor.new_sensor(config[CONF_MOTION])
        cg.add(var.motion_sensor.set(sens))
    if CONF_MAX_MOTION in config:
        sens = await sensor.new_sensor(config[CONF_MAX_MOTION])
        cg.add(var.max_motion_sensor.set(sens))
    if CONF_MIN_MOTION in config:
        sens = await sensor.new_sensor(config[CONF_MIN_MOTION])
        cg.add(var.min_motion_sensor.set(sens))
    if CONF_MAX_PRESENCE in config:
        sens = await sensor.new_sensor(config[CONF_MAX_PRESENCE])
        cg.add(var.max_presence_sensor.set(sens))
    if CONF_MIN_PRESENCE in config:
        sens = await sensor.new_sensor(config[CONF_MIN_PRESENCE])
        cg.add(var.min_presence_sensor.set(sens))
    if CONF_UNOCC_TIME in config:
        sens = await sensor.new_sensor(config[CONF_UNOCC_TIME])
        cg.add(var.unocc_time_sensor.set(sens))

    # Add lambda for custom sensors
    cg.add(var.set_sensors_lambda(config[CONF_LAMBDA]))
