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
        }

        void Write(int iValue)
        {
            if(iValue < 0){
                analogWrite(iPin1, abs(iValue));
                analogWrite(iPin2, 0);
            }
            else{
                analogWrite(iPin1, 0);
                analogWrite(iPin2, abs(iValue));
            }
        }
}