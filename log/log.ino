#include <OneWire.h>
#include <DallasTemperature.h>
#include <stdio.h>


/* Variables for use later
 * sleep_time = Time between measurements
 * temp_chip = which analog port is used to register
 *     input from termostat chip.
 * temp_rod = which digital port is used to register
 *     input from termostat rod.
 * oneWire_rod =
 * sensor_rod =
 */
const int sleep_time = 10 * 1000;
const int temp_chip = A0;
const int temp_rod = 5;
OneWire oneWire_rod(temp_rod);
DallasTemperature sensor_rod(&oneWire_rod, 0);


void setup() {
	Serial.begin(9600);
	pinMode(temp_chip, INPUT);
	sensor_rod.begin();
}


float temp_read(float pin) {
	/* Read temperature from analogue temperature sensor
	 * Converts reading to degrees Celsius
	 */
	const int beta = 4090;
	const int res = 10;
	int a = 1023 - analogRead(pin);
	float lo = (1025.0 * res / a - res) / res;
	float temp = beta / (log(lo) + beta / 298.0) - 273.0;
	return temp;
}


void temp_csv_format(void) {
	/* Read temperature and print it in csv friendly format
	 * fields: tempC_chip, tempC_rod
	 * Temperatures are measured in celsius.
	 */
	float tempC_chip = temp_read(temp_chip);
	float tempC_rod = 0.0;

	sensor_rod.requestTemperatures();
	tempC_rod = sensor_rod.getTempCByIndex(0);
	Serial.print(tempC_chip);
	Serial.print(",");
	Serial.println(tempC_rod);
}


void temp_human(void) {
	/* Debug print temperatures in human readable format.
	 * notes: Reuses code. This could use a refactor.
	 */
	float tempC_chip = temp_read(temp_chip);
	float tempC_rod = 0.0;

	sensor_rod.requestTemperatures();
	tempC_rod = sensor_rod.getTempCByIndex(0);
	Serial.print("Temperature chip, rod: ");
	Serial.print(tempC_chip);
	Serial.print(", ");
	Serial.println(tempC_rod);
}


void loop() {
	// temp_human();
	temp_csv_format();
	delay(sleep_time);
}
