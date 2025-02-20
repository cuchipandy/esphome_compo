#pragma once

#include "esphome.h"

namespace esphome {
namespace ld2411s {

class LD2411SSensor : public Component, public UARTDevice {
 public:
  LD2411SSensor(UARTComponent *parent) : UARTDevice(parent) {}

  Sensor *presence_sensor{new Sensor()};
  Sensor *motion_sensor{new Sensor()};
  Sensor *distance_sensor{new Sensor()};
  Sensor *max_motion_sensor{new Sensor()};
  Sensor *min_motion_sensor{new Sensor()};
  Sensor *max_presence_sensor{new Sensor()};
  Sensor *min_presence_sensor{new Sensor()};
  Sensor *unocc_time_sensor{new Sensor()};

  void setup() override {}

  void loop() override {
    while (available()) {
      uint8_t byte = read();
      this->bytes_.push_back(byte);

      if (this->bytes_.size() >= 2 &&
          ((this->bytes_[this->bytes_.size() - 2] == 0x55 && this->bytes_[this->bytes_.size() - 1] == 0x55) ||
           (this->bytes_.size() >= 4 && this->bytes_[this->bytes_.size() - 4] == 0x04 &&
            this->bytes_[this->bytes_.size() - 3] == 0x03 && this->bytes_[this->bytes_.size() - 2] == 0x02 &&
            this->bytes_[this->bytes_.size() - 1] == 0x01))) {
        this->process_packet_();
        this->bytes_.clear();
      }
    }
  }

 protected:
  void process_packet_() {
    if (this->bytes_.size() < 3)
      return;

    if (this->bytes_[0] == 0xAA && this->bytes_[1] == 0xAA) {
      switch (this->bytes_[2]) {
        case 0x00:
          this->presence_sensor->publish_state(0);
          this->motion_sensor->publish_state(0);
          break;
        case 0x01:
        case 0x02:
          this->presence_sensor->publish_state(1);
          this->motion_sensor->publish_state(this->bytes_[2] == 0x01);
          if (this->bytes_.size() >= 5) {
            uint16_t distance = (this->bytes_[4] << 8) | this->bytes_[3];
            this->distance_sensor->publish_state(distance);
          }
          break;
      }
    } else if (this->bytes_.size() >= 20 && this->bytes_[0] == 0xFD && this->bytes_[1] == 0xFC &&
               this->bytes_[2] == 0xFB && this->bytes_[3] == 0xFA && this->bytes_[6] == 0x73 && this->bytes_[7] == 0x01) {
      uint16_t max_motion = (this->bytes_[11] << 8) | this->bytes_[10];
      uint16_t min_motion = (this->bytes_[13] << 8) | this->bytes_[12];
      uint16_t max_presence = (this->bytes_[15] << 8) | this->bytes_[14];
      uint16_t min_presence = (this->bytes_[17] << 8) | this->bytes_[16];
      uint16_t unocc_time = (this->bytes_[19] << 8) | this->bytes_[18];

      this->max_motion_sensor->publish_state(max_motion);
      this->min_motion_sensor->publish_state(min_motion);
      this->max_presence_sensor->publish_state(max_presence);
      this->min_presence_sensor->publish_state(min_presence);
      this->unocc_time_sensor->publish_state(unocc_time / 10.0f);
    }
  }

  std::vector<uint8_t> bytes_;
};

}  // namespace ld2411s
}  // namespace esphome
