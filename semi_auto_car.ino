#include <NewPing.h>

#define TRIG_PIN 9
#define ECHO_PIN 10
#define MAX_DISTANCE 200
#define MOTOR1_FWD 5
#define MOTOR1_BWD 6
#define MOTOR2_FWD 7
#define MOTOR2_BWD 8

NewPing sonar(TRIG_PIN, ECHO_PIN, MAX_DISTANCE);

void setup() {
    pinMode(MOTOR1_FWD, OUTPUT);
    pinMode(MOTOR1_BWD, OUTPUT);
    pinMode(MOTOR2_FWD, OUTPUT);
    pinMode(MOTOR2_BWD, OUTPUT);
    Serial.begin(9600);
}

void loop() {
    int distance = sonar.ping_cm();
    Serial.print("Distance: ");
    Serial.println(distance);

    if (distance > 20 || distance == 0) { // Move forward if no obstacle
        digitalWrite(MOTOR1_FWD, HIGH);
        digitalWrite(MOTOR1_BWD, LOW);
        digitalWrite(MOTOR2_FWD, HIGH);
        digitalWrite(MOTOR2_BWD, LOW);
    } else { // Stop and avoid obstacle
        digitalWrite(MOTOR1_FWD, LOW);
        digitalWrite(MOTOR1_BWD, LOW);
        digitalWrite(MOTOR2_FWD, LOW);
        digitalWrite(MOTOR2_BWD, LOW);
        delay(500);
        turnRight(); // AI-based decision function
    }
    delay(100);
}

void turnRight() {
    digitalWrite(MOTOR1_FWD, LOW);
    digitalWrite(MOTOR1_BWD, HIGH);
    digitalWrite(MOTOR2_FWD, HIGH);
    digitalWrite(MOTOR2_BWD, LOW);
    delay(800);
}


