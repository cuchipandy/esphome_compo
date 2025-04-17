#include "uart_sensor.h"

namespace esphome {
namespace uart_sensor {

UARTSensor::UARTSensor(UARTComponent *parent) : UARTDevice(parent) {}

void UARTSensor::loop() {
  while (available()) {
    bytes.push_back(read());

    if ((bytes.size() >= 2 && bytes[bytes.size() - 2] == 0x55 && bytes[bytes.size() - 1] == 0x55) ||
        (bytes.size() >= 4 && bytes[bytes.size() - 4] == 0x04 &&
         bytes[bytes.size() - 3] == 0x03 && bytes[bytes.size() - 2] == 0x02 &&
         bytes[bytes.size() - 1] == 0x01)) {
      processPacket();
      bytes.clear();
    }
  }
}

void UARTSensor::processPacket() {
  if ((bytes[0] == 0xAA) && (bytes[1] == 0xAA) && (bytes[2] == 0x00)) {
    presence_sensor->publish_state(0);
    motion_sensor->publish_state(0);
    return;
  }

  if ((bytes[0] == 0xAA) && (bytes[1] == 0xAA) && (bytes[2] == 0x01)) {
    presence_sensor->publish_state(1);
    motion_sensor->publish_state(1);

    int distance = (bytes[4] << 8) | bytes[3];
    distance_sensor->publish_state(distance);
    return;
  }

  if ((bytes[0] == 0xAA) && (bytes[1] == 0xAA) && (bytes[2] == 0x02)) {
    presence_sensor->publish_state(1);
    motion_sensor->publish_state(0);

    int distance = (bytes[4] << 8) | bytes[3];
    distance_sensor->publish_state(distance);
    return;
  }

  if ((bytes[0] == 0xFD) && (bytes[1] == 0xFC) && (bytes[2] == 0xFB) && (bytes[3] == 0xFA) &&
      (bytes[6] == 0x73) && (bytes[7] == 0x01)) {
    int max_m = (bytes[11] << 8) | bytes[10];
    int min_m = (bytes[13] << 8) | bytes[12];
    int max_p = (bytes[15] << 8) | bytes[14];
    int min_p = (bytes[17] << 8) | bytes[16];
    int unocc = (bytes[19] << 8) | bytes[18];

    max_motion_sensor->publish_state(max_m);
    min_motion_sensor->publish_state(min_m);
    max_presence_sensor->publish_state(max_p);
    min_presence_sensor->publish_state(min_p);
    unocc_time_sensor->publish_state(unocc / 10);
    return;
  }
}

}  // namespace uart_sensor
}  // namespace esphome
