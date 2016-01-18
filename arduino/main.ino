// Main configuration of my Arduino connected to a raspberry pi.

const int pin_busy_led = 9;
const int pin_buzzer = 11;
const int pin_thermistor = A0;
const int pin_radiotx = 8;

void beep(int duration=100)
{
    digitalWrite(pin_buzzer, HIGH);
    delay(duration);
    digitalWrite(pin_buzzer, LOW);
}

void setup()
{
    pinMode(pin_busy_led, OUTPUT);
    pinMode(pin_buzzer, OUTPUT);

    beep(100);
    Serial.begin(115200);
}

void read_thermistor()
{
    Serial.println(analogRead(pin_thermistor));
}

void radio_transmit()
{
    int n_pulses, n_switches;
    int* switches = NULL;

    while(!Serial.available());
    n_pulses = Serial.readStringUntil('\n').toInt();
    n_switches = n_pulses * 2 - 1;

    switches = (int*)malloc(sizeof(int) * n_switches);

    if (switches == NULL) {
        Serial.println("M");
        return;
    }

    for (int i = 0; i < n_switches; i++) {
        while(!Serial.available());
        switches[i] = Serial.readStringUntil('\n').toInt();
    }

    pinMode(pin_radiotx, OUTPUT);

    for (int i = 0; i < n_switches; i++) {
        digitalWrite(pin_radiotx, i % 2 ? LOW : HIGH);
        delayMicroseconds(switches[i]);
    }

    digitalWrite(pin_radiotx, LOW);

    free(switches);

    Serial.println("!");
}


void loop()
{
    beep(10);

    Serial.println("?");

    while(!Serial.available());
    char cmd = Serial.read();

    digitalWrite(pin_busy_led, HIGH);

    if (cmd == 'R') {
        radio_transmit();
    } else if (cmd == 'T') {
        read_thermistor();
    } else if (cmd == 'W') {
        delay(1000);
    } else {
        Serial.println("C");
    }
    
    digitalWrite(pin_busy_led, LOW);
}

