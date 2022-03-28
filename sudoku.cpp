#include <iostream>         

using namespace std;

int main()                           

{

    int a,b,c,d,cnt=0; 

    for(a=0;a<=20;a++) 

     for(b=0;b<=40;b++) 

      for(c=0;c<=50;c++) 

       for(d=0;d<=50;d++) 

          { 

          if(a*100+b*50+c*10+d*5==2000 && a+b+c+d==50) 

                { 

             cout<<a<<" , "<<b<<" , "<<c<<" , "<<d<<endl; 

             cnt++; 

                } 

          } 

    cout<<"Count="<<cnt<<endl; 

    return 0; 

}
