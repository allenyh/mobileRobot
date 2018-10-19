class Motor{
  int in1
  int in2
  int en
  static int pwm_min = 0;
  static int pwm_max = 255;
  void Motor(int ina,int inb, int en0){
    in1 = ina;
    in2 = inb;
    en = en0;
  }
  void firstSetup(){
    digitalWrite(in1, LOW);
    digitalWrite(in2, LOW);
    analogWrite(en, 0);
  }
  void setSpeed(int pwm){
    if(pwm > 0){
      digitalWrite(in1, HIGH);
      digitalWrite(in2, LOW);
    }
    else if(pwm < 0){
      digitalWrite(in1, LOW);
      digitalWrite(in2, HIGH);
    }
    else{
      digitalWrite(in1, LOW);
      digitalWrite(in2, LOW);
    }
    if(pwm > pwm_max)
      pwm = pwm_max;
    else if(pwm < pwm_min)
      pwm = pwm_min;
    analogWrite(en, pwm);
  }
}
