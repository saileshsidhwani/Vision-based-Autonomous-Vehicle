

const byte numPins = 4;

byte num ;
int Start,steerFlag=0; ; 


byte pins[] = {12, 11, 10, 9, 8, 7, 6};


void setup() {
  Serial.begin(9600);
  pinMode(12, OUTPUT); 
  pinMode(11, OUTPUT); 
  pinMode(10, OUTPUT); 
  pinMode(9, OUTPUT); 
  pinMode(8, OUTPUT); 
  pinMode(7, OUTPUT); 
  pinMode(6, OUTPUT); 
  pinMode(5, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(13,OUTPUT);
  pinMode(A2,OUTPUT);
  pinMode(A3,OUTPUT);
  pinMode(A4,OUTPUT);
  pinMode(A0, INPUT);
  pinMode(A1,OUTPUT); 
  
  Start = 0;
  
  num = 0b00000000;
}

void loop() {

    /*analogWrite(A2,255);
    analogWrite(A3,255);
    analogWrite(A4,255);*/
  
  if(Serial.available() > 0) 
   num = Serial.read(); 
   
   //Serial.print("Start :");
   //Serial.println(num); 
   
  //Serial.println();
  
  //Serial.print("DATA on start :");
  //Serial.println(bitRead(num,5));
  
  
  if(bitRead(num,5))
  {
     Start = 1 ;
    Serial.print("DATA on start :");     
     digitalWrite(8, 0);
     //digitalWrite(13,LOW);
     //delay(1);
     digitalWrite(3,HIGH);
     if(analogRead(A0)<426 && steerFlag==0)
     {
       steerFlag=1;
       while(analogRead(A0)!=426)
       {
         digitalWrite(pins[3], HIGH);
         digitalWrite(pins[2], LOW);
       }
         
     }
     if(analogRead(A0)>426 && steerFlag==0)
     {
       steerFlag=1;
       while(analogRead(A0)>550)  //test and calc value
       {
         digitalWrite(pins[2], HIGH);
         digitalWrite(pins[3], LOW);
       }
     }
  } 
  
  if(bitRead(num, 4))
   {
      Start = 0 ;
     steerFlag=0; 
      digitalWrite(8, 1); 
      digitalWrite(3,LOW); 
     
   }  
     
     Serial.println();
    Serial.print("Start :");
   Serial.println(Start);
  
  
   
  if(Start == 1)
  {
     Serial.println();
     Serial.print("Data is :");
     Serial.println(num);
    
    
     for (byte i=0; i<numPins; i++)
     {
        byte state = bitRead(num, i);
        
        if(i==2)
        {
           if(analogRead(A0)> 110  && state==1) 
            digitalWrite(pins[i], state);
           else
            digitalWrite(pins[i],LOW); 
        }       
        else
        if(i==3)
        {
          if (analogRead(A0)< 880 && state==1)
            digitalWrite(pins[i], state);
          else 
            digitalWrite(pins[i], LOW);
        }
        else
           digitalWrite(pins[i], state);
         
        
        
        if( checkSTRT())
        {         
          analogWrite(A2,255);          
          analogWrite(A3,255);       
        }
        else
        {         
          analogWrite(A3,0);          
          analogWrite(A2,0);
        }
        
        
        
         
        if(checkLeftTurn())
        {
          analogWrite(A2,255);
          digitalWrite(6,HIGH);
          //digitalWrite(6,LOW);
        }
        else
        {
          if(checkSTRT()==0) 
          analogWrite(A2,0);
          digitalWrite(6,LOW);
          
        }
        
        if(checkRightTurn())
        {
          analogWrite(A3,255);
         // analogWrite(A2,0);
          digitalWrite(4,HIGH);
          
        }
        else          
        {
          if(checkSTRT()==0) 
            analogWrite(A3,0);
          digitalWrite(4,LOW);  
        }
        
        
        if(i==1)    
         if(state==1)      
          {
            analogWrite(A4,255);
            digitalWrite(7,HIGH);
            
          } 
         else         
          {
            analogWrite(A4,0);
            digitalWrite(7,LOW); 
          }
          
          
          if(bitRead(num,6)==1)
            digitalWrite(5,HIGH);
          else
            digitalWrite(5,LOW);
            
        Serial.print(state);
     }
  }  
  Serial.println();
  
  //delay(5);
}


int checkRightTurn()
{

   if( bitRead(num, 2) == 1 && analogRead(A0)<300)
      return 1 ;

   return 0;
}


int checkLeftTurn()
{

   if( bitRead(num, 3) == 1 && analogRead(A0)>550)
      return 1 ;

   return 0;
}      


int checkSTRT()
{

   if( bitRead(num, 0) == 1 && analogRead(A0)>300 && analogRead(A0)<550)
      return 1 ;

   return 0;
}      



