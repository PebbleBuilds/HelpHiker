#ifndef HELPHIKER_MOTORS
#define HELPHIKER_MOTORS

#include <Arduino.h>
#include <math.h>

class Motor
{
    int m_iPin1, m_iPin2, m_iPinEnable;

    public: 
        Motor(int iPin1, int iPin2, int iPinEnable){
            m_iPin1 = iPin1;
            m_iPin2 = iPin2;
            m_iPinEnable = iPinEnable;
        }

        void Setup()
        {
            pinMode(m_iPin1, OUTPUT);
            pinMode(m_iPin2, OUTPUT);
            pinMode(m_iPinEnable, OUTPUT);

            digitalWrite(m_iPin1, 0);
            digitalWrite(m_iPin2, 0);
            analogWrite(m_iPinEnable, 0);
        }

        void Write(int iValue)
        {
            if(iValue == 0){
                digitalWrite(m_iPin1, 0);
                digitalWrite(m_iPin2, 0);
                analogWrite(m_iPinEnable, iValue);
            }
            else if(iValue > 0){
                digitalWrite(m_iPin1, 0);
                digitalWrite(m_iPin2, 1);
                analogWrite(m_iPinEnable, iValue);
            }
            else{
                digitalWrite(m_iPin1, 1);
                digitalWrite(m_iPin2, 0);
                analogWrite(m_iPinEnable, -iValue);
            }
        }
};

#endif