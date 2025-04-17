#pragma once

#include "esphome.h"

namespace esphome {
namespace uart_sensor {

class UARTSensor : public Component, public UARTDevice {
 public:
  explicit UARTSensor(UARTComponent *parent);

  Sensor *presence_sensor = new Sensor();
  Sensor *motion_sensor = new Sensor();
  Sensor *distance_sensor = new Sensor();
  Sensor *max_motion_sensor = new Sensor();
  Sensor *min_motion_sensor = new Sensor();
  Sensor *max_presence_sensor = new Sensor();
  Sensor *min_presence_sensor = new Sensor();
  Sensor *unocc_time_sensor = new Sensor();

  void setup() override {}
  void loop() override;

 protected:
  std::vector<int> bytes;
  void processPacket();
};

}  // namespace uart_sensor
}  // namespace esphome
