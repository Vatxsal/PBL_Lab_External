#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ThingSpeak.h>
#include <math.h>

const char* ssid = "OnePlus 10R 5G";
const char* password = "122333444";
unsigned long channelID = 2756320;
const char* apiKey = "HJ98F8G2001K4NQJ";

WiFiClient client;
const int soundPin = A0;
unsigned long lastUpdateTime = 0;
const unsigned long uploadInterval = 5000;

const int numSamples = 10;
int samples[numSamples];
int sampleIndex = 0;
int baselineNoiseLevel = 0;

float calculateSoundDb(int avgSoundLevel) {
    int adjustedLevel = avgSoundLevel - baselineNoiseLevel;
    if (adjustedLevel < 0) adjustedLevel = 0;
    return 20 * log10(adjustedLevel + 1); 
}

void setup() {
    Serial.begin(115200);
    WiFi.begin(ssid, password);
    ThingSpeak.begin(client);

    Serial.print("Connecting to Wi-Fi");
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nConnected to Wi-Fi!");

    for (int i = 0; i < numSamples; i++) {
        samples[i] = 0;
    }

    Serial.println("Calibrating... Please ensure a quiet environment.");
    long total = 0;
    int baselineSamples = 100;
    for (int i = 0; i < baselineSamples; i++) {
        total += analogRead(soundPin);
        delay(10);
    }
    baselineNoiseLevel = total / baselineSamples;
    Serial.print("Baseline noise level: ");
    Serial.println(baselineNoiseLevel);
}

void loop() {
    int soundLevel = analogRead(soundPin);
    samples[sampleIndex] = soundLevel;
    sampleIndex = (sampleIndex + 1) % numSamples;

    long total = 0;
    for (int i = 0; i < numSamples; i++) {
        total += samples[i];
    }
    int avgSoundLevel = total / numSamples;

    float soundDb = calculateSoundDb(avgSoundLevel);

    Serial.print("Sound Level (dB): ");
    Serial.println(soundDb);

    if (millis() - lastUpdateTime >= uploadInterval) {
        lastUpdateTime = millis();
        ThingSpeak.setField(1, soundDb);
        if (ThingSpeak.writeFields(channelID, apiKey) == 200) {
            Serial.println("Data successfully sent to ThingSpeak.");
        } else {
            Serial.println("Failed to send data to ThingSpeak.");
        }
    }

    delay(50);
}
