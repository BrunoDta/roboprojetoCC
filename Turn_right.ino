#define ENA 2   // Left
#define ENB 12    // Right
#define gpRb 14  // left Backward
#define gpRf 13  // left Forward
#define gpLb 33  // Right Backward
#define gpLf 15  // right Forward
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);//open serial and set the baudrate
  pinMode(gpLb,OUTPUT);//before useing io pin, pin mode must be set first 
  pinMode(gpLf,OUTPUT);
  pinMode(gpRb,OUTPUT);
  pinMode(gpRf,OUTPUT);
  pinMode(ENA,OUTPUT);
  pinMode(ENB,OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(ENA,HIGH); //enable L298n A channel
  digitalWrite(ENB,HIGH); //enable L298n B channel
  digitalWrite(gpLb,LOW); //set gpLb low level
  digitalWrite(gpLf,HIGH); //set gpLf hight level
  digitalWrite(gpRb,HIGH); //set gpRb hight level
  digitalWrite(gpRf,LOW); //set gpRf low level
  Serial.println("Right"); //send message to serial monitor
}
