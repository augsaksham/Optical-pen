#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

const uint64_t my_radio_pipe = 0xE8E8F0F0E1LL;     //Remember that this code is the same as in the transmitter
RF24 radio(9, 10);  //CSN and CE pins

#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
#include "Wire.h"
#endif

struct Data_to_be_sent {
  byte ch1;
  byte ch2;
  byte ch3;
};

//Create a variable with the structure above and name it sent_data
Data_to_be_sent sent_data;

unsigned long millisStart;
long MouseX = 0;
long MouseY = 0;
char stat,x,y;

byte PS2ReadByte = 0;

#define PS2CLOCK  6
#define PS2DATA   5


void PS2GoHi(int pin){
  pinMode(pin, INPUT);
  digitalWrite(pin, HIGH);
}

void PS2GoLo(int pin){
  pinMode(pin, OUTPUT);
  digitalWrite(pin, LOW);
}

void PS2Write(unsigned char data){
  unsigned char parity=1;

  PS2GoHi(PS2DATA);
  PS2GoHi(PS2CLOCK);
  delayMicroseconds(300);
  PS2GoLo(PS2CLOCK);
  delayMicroseconds(300);
  PS2GoLo(PS2DATA);
  delayMicroseconds(10);
  PS2GoHi(PS2CLOCK);

  while(digitalRead(PS2CLOCK)==HIGH);

  for(int i=0; i<8; i++){
    if(data&0x01) PS2GoHi(PS2DATA);
    else PS2GoLo(PS2DATA);
    while(digitalRead(PS2CLOCK)==LOW);
    while(digitalRead(PS2CLOCK)==HIGH);
    parity^=(data&0x01);
    data=data>>1;
  }

  if(parity) PS2GoHi(PS2DATA);
  else PS2GoLo(PS2DATA);

  while(digitalRead(PS2CLOCK)==LOW);
  while(digitalRead(PS2CLOCK)==HIGH);

  PS2GoHi(PS2DATA);
  delayMicroseconds(50);

  while(digitalRead(PS2CLOCK)==HIGH);
  while((digitalRead(PS2CLOCK)==LOW)||(digitalRead(PS2DATA)==LOW));

  PS2GoLo(PS2CLOCK);
}

unsigned char PS2Read(void){
  unsigned char data=0, bit=1;

  PS2GoHi(PS2CLOCK);
  PS2GoHi(PS2DATA);
  delayMicroseconds(50);
  while(digitalRead(PS2CLOCK)==HIGH);

  delayMicroseconds(5);
  while(digitalRead(PS2CLOCK)==LOW);

  for(int i=0; i<8; i++){
    while(digitalRead(PS2CLOCK)==HIGH);
    if(digitalRead(PS2DATA)==HIGH) data|=bit;
    while(digitalRead(PS2CLOCK)==LOW);
    bit=bit<<1;
  }

  while(digitalRead(PS2CLOCK)==HIGH);
  while(digitalRead(PS2CLOCK)==LOW);
  while(digitalRead(PS2CLOCK)==HIGH);
  while(digitalRead(PS2CLOCK)==LOW);

  PS2GoLo(PS2CLOCK);

  return data;
}

void PS2MouseInit(void){
  PS2Write(0xFF);
  for(int i=0; i<3; i++) PS2Read();
  PS2Write(0xF0);
  PS2Read();
  delayMicroseconds(100);
}

void PS2MousePos(char &stat, char &x, char &y){
  PS2Write(0xEB);
  PS2Read();
  stat=PS2Read();
  x=PS2Read();
  y=PS2Read();
}


void setup(){
  radio.begin();
  radio.setAutoAck(false);
  radio.setDataRate(RF24_250KBPS);  
  radio.openWritingPipe(my_radio_pipe);
  
  //We start the radio comunication
  radio.stopListening();

  #if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
        Wire.begin();
  #elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE
        Fastwire::setup(400, true);
  #endif
  
  PS2GoHi(PS2CLOCK);
  PS2GoHi(PS2DATA);

  Serial.begin(9600);
  while(!Serial); 
  Serial.println("Setup");
  PS2MouseInit();
  Serial.println("Mouse Ready");
  millisStart=millis();
  MouseX = 0;
  MouseY = 0;
}

void nrf(char mx,char my,int button)
  {
    sent_data.ch1  = mx;
    sent_data.ch2  = my;
    sent_data.ch3  = button;
    radio.write(&sent_data, sizeof(Data_to_be_sent));
  }

void loop(){

    int but=analogRead(A4)-400;

    PS2MousePos(stat,x,y);
    //Serial.print(stat, BIN);
    //Serial.print("\tdelta X=");
    Serial.println(x, DEC);
    //Serial.print("\tdelta Y=");
    //Serial.println(y, DEC);

  MouseX = 128+x;
  MouseY = 128+y;

  nrf(MouseX, MouseY,but);
  //  delay(1000);
}
