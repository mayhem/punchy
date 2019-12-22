
char buf[10];
char buf_index = 0;

void setup() 
{
    Serial.begin(9600);
    pinMode(2, OUTPUT);
    digitalWrite(2, LOW);
    
    buf[0] = 0;
}

void loop() 
{
    char ch;
    int  d;
    
    if (Serial.available() > 0) 
    {
        ch = Serial.read();
        if (ch == 10)
        {
            d = atoi(buf);
            if (d <= 0)
                Serial.println("bad input. ignored.");
            else
            {
                digitalWrite(2, HIGH);
                delay(d);
                digitalWrite(2, LOW);
                Serial.print(d);
                Serial.println("ms");
            }
            buf[0] = 0;
            buf_index = 0;
        }
        else
        {
            buf[buf_index] = ch;
            buf_index++;
            buf[buf_index] = 0;
        }
    }
}
