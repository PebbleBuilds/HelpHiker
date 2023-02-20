#ifndef HELPHIKER_MOTORS
#define HELPHIKER_MOTORS

#include <Arduino.h>
#include <math.h>

class Motor
{
    int m_iPin1, m_iPin2;

    public: 
        Motor(int iPin1, int iPin2){
            m_iPin1 = iPin1;
            m_iPin2 = iPin2;
        }

        void Setup()
        {
            pinMode(m_iPin1, OUTPUT);
            pinMode(m_iPin2, OUTPUT);

            analogWrite(m_iPin1, 0);
            analogWrite(m_iPin2, 0);
        }

        void Write(int iValue)
        {
            if(iValue > 0){
                analogWrite(m_iPin1, iValue);
                analogWrite(m_iPin2, 0);
            }
            else{
                analogWrite(m_iPin1, 0);
                analogWrite(m_iPin2, -iValue);
            }
        }
};

#endif