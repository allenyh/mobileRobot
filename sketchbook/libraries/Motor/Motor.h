#ifndef Motor_h
#define Motor_h

class Motor{

public:
  int in1;
  int in2;
  int enable;
  const int pwm_min = 0;
  const int pwm_max = 255;
  
  Motor();  
  void set(int ina,int inb,int en);
  void setup();
  void setSpeed(int pwm);
};

#endif
