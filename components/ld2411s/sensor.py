import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor, uart
from esphome.const import UNIT_CENTIMETER, UNIT_SECOND, DEVICE_CLASS_DISTANCE, STATE_CLASS_MEASUREMENT

DEPENDENCIES = ["uart"]

ld2411s_ns = cg.esphome_ns.namespace("ld2411s")
LD2411SSensor = ld2411s_ns.class_("LD2411SSensor", cg.PollingComponent, uart.UARTDevice)

def setup_ld2411s(config):
    var = cg.new_Pvariable(config[CONF_ID])
    yield cg.register_component(var, config)
    yield sensor.register_sensor(var, config)
    return var


CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(LD2411SSensor),
        cv.Required("uart_id"): cv.use_id(uart.UARTComponent),
        cv.Optional("distance"): sensor.sensor_schema(
            unit_of_measurement=UNIT_CENTIMETER,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_DISTANCE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional("presence"): sensor.sensor_schema(),
        cv.Optional("motion"): sensor.sensor_schema(),
        cv.Optional("max_motion"): sensor.sensor_schema(),
        cv.Optional("min_motion"): sensor.sensor_schema(),
    }
).extend(cv.polling_component_schema("1s")).extend(uart.UART_DEVICE_SCHEMA)

async def to_code(config):
    var = cg.new_Pvariable(config[cv.GenerateID()])
    await cg.register_component(var, config)
    await uart.register_uart_device(var, config)

    if "distance" in config:
        sens = await sensor.new_sensor(config["distance"])
        cg.add(var.set_distance_sensor(sens))

    if "presence" in config:
        sens = await sensor.new_sensor(config["presence"])
        cg.add(var.set_presence_sensor(sens))

    if "motion" in config:
        sens = await sensor.new_sensor(config["motion"])
        cg.add(var.set_motion_sensor(sens))

    if "max_motion" in config:
        sens = await sensor.new_sensor(config["max_motion"])
        cg.add(var.set_max_motion_sensor(sens))

    if "min_motion" in config:
        sens = await sensor.new_sensor(config["min_motion"])
        cg.add(var.set_min_motion_sensor(sens))
