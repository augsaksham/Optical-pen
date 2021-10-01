#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>


const uint64_t pipeIn = 0xE8E8F0F0E1LL;     //Remember that this code is the same as in the transmitter
RF24 radio(48, 49);  //CSN and CE pins

// The sizeof this struct should not exceed 32 bytes
struct Received_data {
  byte ch1;
  byte ch2;
  byte ch3;
};

Received_data received_data;

int Xaxis = 0;
int Yaxis = 0;
int but=0;

void reset_the_Data() 
{
  // 'safe' values to use when NO radio input is detected
  received_data.ch1 = 0;      //Throttle (channel 1) to 0
  received_data.ch2 = 0;
  received_data.ch3 = 0;
}



/******************/

void setup()
{
  Serial.begin(9600);
  Serial.print("1000");
  //We reset the received values
  reset_the_Data();

  //Once again, begin and radio configuration
  radio.begin();
  radio.setAutoAck(false);
  radio.setDataRate(RF24_250KBPS);  
  radio.openReadingPipe(1,pipeIn);
  
  //We start the radio comunication
  radio.startListening();

}

/******************/

unsigned long lastRecvTime = 0;

//We create the function that will read the data each certain time
void receive_the_data()
{
  while ( radio.available() ) {
  radio.read(&received_data, sizeof(Received_data));
  lastRecvTime = millis(); //Here we receive the data
}
}

/******************/
float var;

void loop()
{
  var= millis();
  
  while(!radio.available())
  {
//    Serial.println("not");
  }
  int Speed;
  
  //Receive the radio data
  receive_the_data();

//////////This small if will reset the data if signal is lost for 1 sec.
/////////////////////////////////////////////////////////////////////////
  /*unsigned long now = millis();
  if ( now - lastRecvTime > 1000 ) {
    // signal lost?
    reset_the_Data();
    //Go up and change the initial values if you want depending on
    //your aplications. Put 0 for throttle in case of drones so it won't
    //fly away
  } */

  
  Xaxis = received_data.ch1;   //X axis
  Yaxis = received_data.ch2;   //Y axis
  but = received_data.ch3; 

  Serial.print("X= ");
  Serial.print(Xaxis, DEC); 
  Serial.print("   Y= ");
  Serial.print(Yaxis, DEC);
  Serial.print("   Button ");
  Serial.println(but);
  //Serial.println(millis()-var); 
}//Loop end
