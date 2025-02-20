# __init__.py
import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import automation
from esphome.components import sensor, uart, binary_sensor, number
from esphome.const import (
    CONF_ID,
    CONF_NAME,
    CONF_ON_VALUE,
    CONF_STATE,
    DEVICE_CLASS_OCCUPANCY,
    DEVICE_CLASS_MOTION,
    UNIT_CENTIMETER,
    UNIT_SECOND,
    CONF_INTERNAL,
    CONF_ENTITY_CATEGORY,
    ENTITY_CATEGORY_DIAGNOSTIC,
    CONF_ON_PRESS,
    CONF_DATA
)

CODEOWNERS = ["@your_github_username"]  # Reemplaza con tu nombre de usuario de GitHub

DEPENDENCIES = ["uart"]

LD2411SComponent = cg.global_ns.class_("LD2411SComponent", cg.Component)  # Elimina la herencia de uart::UARTDevice aquí
UARTSensor = cg.global_ns.class_("UARTSensor")

CONF_DISTANCE_SENSOR_ID = "distance_sensor_id"
CONF_PRESENCE_SENSOR_ID = "presence_sensor_id"
CONF_MOTION_SENSOR_ID = "motion_sensor_id"
CONF_MAX_MOTION_SENSOR_ID = "max_motion_sensor_id"
CONF_MIN_MOTION_SENSOR_ID = "min_motion_sensor_id"
CONF_MAX_PRESENCE_SENSOR_ID = "max_presence_sensor_id"
CONF_MIN_PRESENCE_SENSOR_ID = "min_presence_sensor_id"
CONF_UNOCC_TIME_SENSOR_ID = "unocc_time_sensor_id"

CONF_MIN_MOTION = "min_motion"
CONF_MAX_MOTION = "max_motion"
CONF_MIN_PRESENCE = "min_presence"
CONF_MAX_PRESENCE = "max_presence"
CONF_UNOCCUPIED_TIME = "unoccupied_time"
CONF_UART_ID = "uart_id"

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(LD2411SComponent),
        cv.Required(CONF_NAME): cv.string,
        cv.Required(CONF_UART_ID): cv.use_id(uart.UART),  # Usa uart.UARTComponent en lugar de uart.UART
        cv.Optional(CONF_MIN_MOTION): sensor.sensor_schema(
            UNIT_CENTIMETER, ICON="mdi:ruler", accuracy_decimals=0
        ),
        cv.Optional(CONF_MAX_MOTION): sensor.sensor_schema(
            UNIT_CENTIMETER, ICON="mdi:ruler", accuracy_decimals=0
        ),
        cv.Optional(CONF_MIN_PRESENCE): sensor.sensor_schema(
            UNIT_CENTIMETER, ICON="mdi:ruler", accuracy_decimals=0
        ),
        cv.Optional(CONF_MAX_PRESENCE): sensor.sensor_schema(
            UNIT_CENTIMETER, ICON="mdi:ruler", accuracy_decimals=0
        ),
        cv.Optional(CONF_UNOCCUPIED_TIME): sensor.sensor_schema(
            UNIT_SECOND, ICON="mdi:timer", accuracy_decimals=0
        ),
    }
).extend(cv.COMPONENT_SCHEMA)

RESET_SYSTEM_ACTION_SCHEMA = automation.maybe_simple_value(
    cv.Schema(
        {
            cv.Required(CONF_ID): cv.use_id(LD2411SComponent),
        }
    )
)

@automation.register_action(
    "ld2411s.reset_system",
    RESET_SYSTEM_ACTION_SCHEMA,
    cv.use_id(LD2411SComponent),
)
async def ld2411s_reset_system_action(config, action_id, template_arg, args):
    paren = cg.get_variable(config[CONF_ID])
    var = cg.new_Pvariable(action_id, template_arg, paren)
    return var

async def to_code(config):
    cg.add_library("Ticker", "1.0")
    cg.add_library("CRC16", "1.0.0")
    cg.add_library("SoftwareSerial", "1.0")

    var = cg.new_Pvariable(config[CONF_ID], config[CONF_NAME])
    await cg.register_component(var, config)
    
    # Get the UART component by ID
    uart_component = await cg.get_variable(config[CONF_UART_ID])
    cg.add(var.set_uart(uart_component))

    cg.add(var.set_name(config[CONF_NAME]))

    if CONF_MIN_MOTION in config:
        sens = await sensor.new_sensor(config[CONF_MIN_MOTION])
        cg.add(var.set_min_motion_sensor(sens))
    if CONF_MAX_MOTION in config:
        sens = await sensor.new_sensor(config[CONF_MAX_MOTION])
        cg.add(var.set_max_motion_sensor(sens))
    if CONF_MIN_PRESENCE in config:
        sens = await sensor.new_sensor(config[CONF_MIN_PRESENCE])
        cg.add(var.set_min_presence_sensor(sens))
    if CONF_MAX_PRESENCE in config:
        sens = await sensor.new_sensor(config[CONF_MAX_PRESENCE])
        cg.add(var.set_max_presence_sensor(sens))
    if CONF_UNOCCUPIED_TIME in config:
        sens = await sensor.new_sensor(config[CONF_UNOCCUPIED_TIME])
        cg.add(var.set_unoccupied_time_sensor(sens))
