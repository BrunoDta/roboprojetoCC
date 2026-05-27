#define ENA 2   // Left
#define ENB 12    // Right
#define gpRb 14  // left Backward
#define gpRf 13  // left Forward
#define gpLb 33  // right Backward
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
  digitalWrite(ENA,HIGH);  //enable L298n A channel
  digitalWrite(ENB,HIGH);  //enable L298n B channel
  digitalWrite(gpLb,HIGH); //set gpLb hight level
  digitalWrite(gpLf,LOW); //set gpLf low level
  digitalWrite(gpRb,LOW); //set gpRb low level
  digitalWrite(gpRf,HIGH); //set gpRf hight level
  Serial.println("Left"); //send message to serial monitor
}