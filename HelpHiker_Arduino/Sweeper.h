#ifndef HELPHIKER_SWEEPER
#define HELPHIKER_SWEEPER

#include <Arduino.h>
#include <Servo.h> 

class Sweeper
{
  Servo servo;              // the servo
  int pos;              // current servo position 
  int increment;        // increment to move for each interval
  int  updateInterval;      // interval between updates
  unsigned long lastUpdate; // last update of position
  int m_iMinPos, m_iMaxPos;

public: 
  Sweeper(int interval, int start_increment, int start_pos, int iMinPos, int iMaxPos)
  {
    updateInterval = interval;
    increment = start_increment;
    pos = start_pos;
    m_iMinPos = iMinPos;
    m_iMaxPos = iMaxPos;
  }
  
  void Attach(int pin)
  {
    servo.attach(pin);
  }
  
  void Detach()
  {
    servo.detach();
  }
  
  void Update()
  {
    if((millis() - lastUpdate) > updateInterval)  // time to update
    {
      lastUpdate = millis();
      pos += increment;
      servo.write(pos);
      Serial.println(pos);
      if ((pos >= m_iMaxPos) || (pos <= m_iMinPos)) // end of sweep
      {
        // reverse direction
        increment = -increment;
      }
    }
  }
};

#endif