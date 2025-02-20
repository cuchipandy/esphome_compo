// ld2411s.h
#pragma once

#include "esphome/core/component.h"
#include "esphome/components/uart/uart.h"
#include "esphome/components/sensor/sensor.h"
#include <Ticker.h>

namespace esphome {

class LD2411SComponent : public Component, public uart::UARTDevice {
 public:
  LD2411SComponent(const std::string &name) : name_(name) {}

  void setup() override;
  void loop() override;
  void dump_config() override;

  void set_name(std::string name) { name_ = name; }
  void set_min_motion_sensor(sensor::Sensor *min_motion_sensor) { min_motion_sensor_ = min_motion_sensor; }
  void set_max_motion_sensor(sensor::Sensor *max_motion_sensor) { max_motion_sensor_ = max_motion_sensor; }
  void set_min_presence_sensor(sensor::Sensor *min_presence_sensor) { min_presence_sensor_ = min_presence_sensor; }
  void set_max_presence_sensor(sensor::Sensor *max_presence_sensor) { max_presence_sensor_ = max_presence_sensor; }
  void set_unoccupied_time_sensor(sensor::Sensor *unoccupied_time_sensor) { unoccupied_time_sensor_ = unoccupied_time_sensor; }

  sensor::Sensor *get_min_motion_sensor() const { return min_motion_sensor_; }
  sensor::Sensor *get_max_motion_sensor() const { return max_motion_sensor_; }
  sensor::Sensor *get_min_presence_sensor() const { return min_presence_sensor_; }
  sensor::Sensor *get_max_presence_sensor() const { return max_presence_sensor_; }
  sensor::Sensor *get_unoccupied_time_sensor() const { return unoccupied_time_sensor_; }

  void reset_system();

 protected:
  std::string name_;
  sensor::Sensor *min_motion_sensor_ = nullptr;
  sensor::Sensor *max_motion_sensor_ = nullptr;
  sensor::Sensor *min_presence_sensor_ = nullptr;
  sensor::Sensor *max_presence_sensor_ = nullptr;
  sensor::Sensor *unoccupied_time_sensor_ = nullptr;

  uint8_t read_buffer_[256];
  size_t read_buffer_pos_{0};
  void process_data_();
};

class UARTSensor {
 public:
    UARTSensor(uart::UARTDevice *uart_bus);
    void update();

    sensor::Sensor *distance_sensor;
    sensor::Sensor *presence_sensor;
    sensor::Sensor *motion_sensor;
    sensor::Sensor *max_motion_sensor;
    sensor::Sensor *min_motion_sensor;
    sensor::Sensor *max_presence_sensor;
    sensor::Sensor *min_presence_sensor;
    sensor::Sensor *unocc_time_sensor;

 private:
    uart::UARTDevice *uart_bus_;
};

}  // namespace esphome
