import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor, uart
from esphome.const import UNIT_CENTIMETER, UNIT_NONE, ICON_RADIO_TOWER, ICON_TIMER

CODEOWNERS = ["@tu_usuario"]

DEPENDENCIES = ["uart"]

ld2411s_ns = cg.esphome_ns.namespace("ld2411s")
LD2411SSensor = ld2411s_ns.class_("UARTSensor", cg.Component, uart.UARTDevice)

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(LD2411SSensor),
        cv.Optional("distance"): sensor.sensor_schema(
            unit_of_measurement=UNIT_CENTIMETER, icon=ICON_RADIO_TOWER, accuracy_decimals=0
        ),
        cv.Optional("presence"): sensor.sensor_schema(
            unit_of_measurement=UNIT_NONE, icon=ICON_RADIO_TOWER, accuracy_decimals=0
        ),
        cv.Optional("motion"): sensor.sensor_schema(
            unit_of_measurement=UNIT_NONE, icon=ICON_RADIO_TOWER, accuracy_decimals=0
        ),
        cv.Optional("max_motion"): sensor.sensor_schema(
            unit_of_measurement=UNIT_NONE, icon=ICON_RADIO_TOWER, accuracy_decimals=0
        ),
        cv.Optional("min_motion"): sensor.sensor_schema(
            unit_of_measurement=UNIT_NONE, icon=ICON_RADIO_TOWER, accuracy_decimals=0
        ),
        cv.Optional("max_presence"): sensor.sensor_schema(
            unit_of_measurement=UNIT_NONE, icon=ICON_RADIO_TOWER, accuracy_decimals=0
        ),
        cv.Optional("min_presence"): sensor.sensor_schema(
            unit_of_measurement=UNIT_NONE, icon=ICON_RADIO_TOWER, accuracy_decimals=0
        ),
        cv.Optional("unocc_time"): sensor.sensor_schema(
            unit_of_measurement=UNIT_NONE, icon=ICON_TIMER, accuracy_decimals=1
        ),
    }
).extend(uart.UART_DEVICE_SCHEMA).extend(cv.COMPONENT_SCHEMA)

async def to_code(config):
    var = cg.new_Pvariable(config[cv.GenerateID()])
    await cg.register_component(var, config)
    await uart.register_uart_device(var, config)
    
    if "distance" in config:
        sens = await sensor.new_sensor(config["distance"])
        cg.add(var.distance_sensor, sens)
    if "presence" in config:
        sens = await sensor.new_sensor(config["presence"])
        cg.add(var.presence_sensor, sens)
    if "motion" in config:
        sens = await sensor.new_sensor(config["motion"])
        cg.add(var.motion_sensor, sens)
    if "max_motion" in config:
        sens = await sensor.new_sensor(config["max_motion"])
        cg.add(var.max_motion_sensor, sens)
    if "min_motion" in config:
        sens = await sensor.new_sensor(config["min_motion"])
        cg.add(var.min_motion_sensor, sens)
    if "max_presence" in config:
        sens = await sensor.new_sensor(config["max_presence"])
        cg.add(var.max_presence_sensor, sens)
    if "min_presence" in config:
        sens = await sensor.new_sensor(config["min_presence"])
        cg.add(var.min_presence_sensor, sens)
    if "unocc_time" in config:
        sens = await sensor.new_sensor(config["unocc_time"])
        cg.add(var.unocc_time_sensor, sens)
