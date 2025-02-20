 #include "ld2411s.h"
 #include "esphome/core/log.h"

 namespace esphome {

 static const char *const TAG = "ld2411s";

 void LD2411SComponent::setup() {
  ESP_LOGCONFIG(TAG, "Setting up LD2411S...");
  // Initialize any resources here
 }

 void LD2411SComponent::loop() {
  if (uart_ == nullptr) {
   ESP_LOGW(TAG, "UART component is not set!");
   return;
  }

  while (uart_->available()) {  // Usa uart_->available()
   uint8_t byte;
   uart_->read(&byte, 1);      // Usa uart_->read()
   read_buffer_[read_buffer_pos_++] = byte;
   if (read_buffer_pos_ >= sizeof(read_buffer_)) {
    read_buffer_pos_ = 0;  // Overflow, reset buffer
   }
   process_data_();
  }
 }

 void LD2411SComponent::dump_config() {
  ESP_LOGCONFIG(TAG, "LD2411S:");
  ESP_LOGCONFIG(TAG, "  Name: %s", this->name_.c_str());
  // LOG_UART_DEVICE(this);  // Ya no es necesario

  if (this->min_motion_sensor_ != nullptr) {
   LOG_SENSOR("  ", "Min Motion Sensor", this->min_motion_sensor_);
  }
  if (this->max_motion_sensor_ != nullptr) {
   LOG_SENSOR("  ", "Max Motion Sensor", this->max_motion_sensor_);
  }
  if (this->min_presence_sensor_ != nullptr) {
   LOG_SENSOR("  ", "Min Presence Sensor", this->min_presence_sensor_);
  }
  if (this->max_presence_sensor_ != nullptr) {
   LOG_SENSOR("  ", "Max Presence Sensor", this->max_presence_sensor_);
  }
  if (this->unoccupied_time_sensor_ != nullptr) {
   LOG_SENSOR("  ", "Unoccupied Time Sensor", this->unoccupied_time_sensor_);
  }
 }

 void LD2411SComponent::process_data_() {
  // Implement your data processing logic here
  // This is where you parse the data from the LD2411S sensor
  // and update the sensor values.
  // Example:
  // if (data_is_valid) {
  //  float distance = parse_distance(read_buffer_);
  //  this->distance_sensor_->publish_state(distance);
  // }
 }

 void LD2411SComponent::reset_system() {
  ESP_LOGI(TAG, "Resetting LD2411S system...");
  // Add code to reset the LD2411S module if needed
 }

 //-----------------------------------------------------------------------------------------------------------------------------

 UARTSensor::UARTSensor(uart::UARTDevice *uart_bus) : uart_bus_(uart_bus) {}

 void UARTSensor::update() {
  // Implement your data processing logic here
  // This is where you parse the data from the LD2411S sensor
  // and update the sensor values.
  // Example:
  // if (data_is_valid) {
  //  float distance = parse_distance(read_buffer_);
  //  this->distance_sensor->publish_state(distance);
  // }
 }

 }  // namespace esphome
 ```
