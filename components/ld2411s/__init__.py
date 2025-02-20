import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import uart, sensor
from esphome.const import CONF_ID, UNIT_METER, ICON_ARROW_UP_DOWN

# Definir namespace para el componente
ld2411s_ns = cg.esphome_ns.namespace("ld2411s")
LD2411SComponent = ld2411s_ns.class_("LD2411SComponent", sensor.Sensor, cg.Component)

# Definir configuración esperada en el YAML
CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(LD2411SComponent),
    cv.Optional("distance"): sensor.sensor_schema(UNIT_METER, ICON_ARROW_UP_DOWN, 2),
}).extend(cv.COMPONENT_SCHEMA).extend(uart.UART_DEVICE_SCHEMA)

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await uart.register_uart_device(var, config)

    if "distance" in config:
        sens = await sensor.new_sensor(config["distance"])
        cg.add(var.set_distance_sensor(sens))

