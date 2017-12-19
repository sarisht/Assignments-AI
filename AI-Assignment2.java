
import java.io.*;
import java.util.LinkedList;
import java.util.Stack;

public class GoalStack {
     public static LinkedList tem=new LinkedList<String>();
     public static LinkedList a1=new LinkedList<String>();
     public static LinkedList a2=new LinkedList<String>();
     public static LinkedList start=new LinkedList<String>();                   //Linked List start to store the start state
     public static LinkedList goal = new LinkedList<String> ();                 //Linked List goal to store the goal state
     public static Stack im=new Stack<String> ();                               //stack im to store the actions to be performed
     public static void main(String args[]) throws IOException
     {
        BufferedReader br = new BufferedReader (new InputStreamReader(System.in));

     System.out.println("Enter the start state");
     String a="";
      while(true)                                                               //accepting start state from user
     {
         a=br.readLine();
         if(a.equals("AE"))
         {
             start.add(a);
             break;
         }
         String b[]=a.split(" ");
         for(int aw=0;aw<b.length;aw++)
         {
         	a1.add(b[aw]);
         }
         int i;
         for (i=1;i<b.length;i++)
         {
                 start.add(b[i]+" ON "+b[i-1]);
         }
         start.add(b[0]+" ONT");
         start.add(b[i-1]+" CL");
         
     }                                                                          //start state accepted
     System.out.println("Enter the goal state");
     while(true)                                                                //accepting goal state from user
     {
         a=br.readLine();
         if(a.equals("AE"))
         {
             goal.add(a);
             break;
         }
         String b[]=a.split(" ");
         for(int aw=0;aw<b.length;aw++)
         {
         	a2.add(b[aw]);
         }
         int i;
         for (i=1;i<b.length;i++)
         {
                 goal.add(b[i]+" ON "+b[i-1]);
         }
         goal.add(b[0]+" ONT");
         goal.add(b[i-1]+" CL");
         
     }       
     int sar=a1.size();
     int isht=a2.size();
     if(sar==isht)
     {
      for(int i=0;i<a1.size();i++)
      {
      	if(a2.contains(a1.get(i)))
      		continue;
      	else
      	  {
      System.out.println("Wrong Arguments");
      return;
  }	
      }
     }
     else
     {
      System.out.println("Wrong Arguments");
      return;
  }
                                                                               //goal state accepted
     sort();                                                                   //invoking sort() function to remove from goal the states common with start
           for(int i=0;i<tem.size();i++)
      {
          String  temp=(String) tem.get(i);
          im.push(temp);                                                        //pushing the states to be achieved in stack im
      } 
     for(int i=0;i<goal.size();i++)
      {
          String  temp=(String) goal.get(i);
          im.push(temp);                                                        //pushing the states to be achieved in stack im
      }
      plan();                                                                   //invoking plan() function to print the planning
     }
     public static void sort()                                                  //declaration of function sort()
     {                                                                          //defination of function sort() begins
       int length=start.size();
       for(int i=0;i<length;i++)
       {
           String temp=(String) start.get(i);
           if(goal.contains(temp))
           {
               tem.add(temp);
               goal.remove(temp);                                               // removing the common states from goal
           }
       }
    }                                                                           //defination of function sort() ends
    public static void on(String a, String b)                                   //declaration of function on()
    {                                                                           //defination of function on() begins
        String a1=a+" HOLD";
        String a2=b+" CL";
        String a3=a+" STACK "+b;
        im.push(a3);                                                            //pushing operation STACK to achieve a ON b state
        im.push(a1);                                                            //pushing pre conditions
        im.push(a2);                                                            
        
    }                                                                           //defination of function on() ends
    public static void ont(String a)                                            //declaration of function ont()
    {                                                                           //defination of function ont() begins
        String a1=a+" HOLD";
        String a2=a+" PD";
        im.push(a2);                                                            //pushing operation HOLD to achieve a ONT state
        im.push(a1);                                                            //pushing pre conditions
    }                                                                           //defination of function ont() ends
    public static void cl(String a)                                             //declaration of function cl()
    {                                                                           //defination of function cl() begins
        int i=0;
        String b="";
      for(i=0;i<start.size();i++)
        {
            String temp=(String) start.get(i);
            
            if(temp.endsWith(" ON "+a))                                         //obtaining the block kept upon the block a, which is to be cleared
            {
                String[] q=new String [3];
                q=temp.split(" ");
                b=q[0];                                                         //the obtained block kept over a is stored in b
                break;
            }
        }
        String a2=b+" CL";
        String a3=b+" ON "+a;
        String a1=b+" UNSTACK "+a ;                                             
        im.push(a1);                                                            //pushing operation UNSTACK to achieve a CL state
        im.push("AE");
        im.push(a3);                                                            //pushing pre conditions
        im.push(a2);
    }                                                                           //defination of function cl() ends
    public static void ae()                                                     //declaration of function ae()
    {                                                                           //defination of function ae() begins
        String a="NULL";
        String c="NULL";
        for(int i=0;i<start.size();i++)
        {
            String temp=(String) start.get(i);
            if(temp.contains(" HOLD"))                                          //obtaining the block which is currently held 
            {
                String b[]=new String [2];
                b=temp.split(" ");
                a=b[0];                                                         //the required block currently held is stored in b
            }
        }
          for(int i=0;i<goal.size();i++)
        {
            String temp=(String) goal.get(i);
            if(temp.contains(a+" ON "))                                         // obtaining the block{if any} on which the block currently held is to be kept i.e. if a ON c is a goal state
            {
                String b[]=new String [3];
                b=temp.split(" ");
                c=b[2];
            }
        }if(a!="NULL"){                                                         //if arm is not empty then proceed
          if(c!="NULL")                                                         //if the block is to kept on some other block as per the goal state then proceed
          {
              String t=c+" CL";                                                 //check if the block c on which a is to kept is CL
              if(start.contains(t))
              {
                  System.out.println(a+" STACK "+c);                            //pushing operation a STACK c to achieve a ON c and AE
                  stack(a,c);                                                   //invoking stack() function
                  return;                                                   
              }
              else                                                              //if the block on which a is to be kept is not CL then proceed
              {
                  System.out.println(a+" PD");                                  //ushing operation PD to achieve AE
                  pd(a);                                                        //invoking pd() function
                  return;   
              }
          }
          else                                                                  //if a is not to be kept on any other block in the goal state(i.e. a is to be kept on table} then proceed
              {
                  System.out.println(a+" PD");                                  //pushing a PD to achieve AE
                  pd(a);                                                        //invoking pd() function
                  return;   
              }
        }
        else                                                                    //if no block is held then proceed
            return;                                                            
    }                                                                           //defination of function ae() ends
    public static void hold(String a)                                           //declaration of function hold()
    {                                                                           //defination of function hold() begins
        if(start.contains(a+" ONT"))                                            //if the block to be held is on table then proceed
        {
        String a2=a+" CL";
        String a3=a+" ONT";
        String a4=a+" PU";
        im.push(a4);                                                            //pushing operation PU to achieve a HOLD state
        im.push("AE");
        im.push(a3);                                                            //pushing pre conditions
        im.push(a2);
        }
        else                                                                    //if the  block to be held is not on table then proceed
        {
             int i=0;
        String b="";
      for(i=0;i<start.size();i++)
        {
            String temp=(String) start.get(i);
            
            if(temp.contains(a+" ON "))                                         //obtaining the block on which the block to be held is kept
            {
                String[] q=new String [3];                     
                q=temp.split(" ");
                b=q[2];                                                          
                break;
            }
        }
        if(b!=""){
        String a2=a+" CL";
        String a3=a+" ON "+b;
        String a1=a+" UNSTACK "+b ;
        im.push(a1);                                                            //pushing operation UNSTACK to achieve a HOLD state
        im.push("AE");
        im.push(a3);                                                            //pushing pre conditions
        im.push(a2);
        }
        }
    }                                                                           //defination of function hold() ends
    public static void pu(String a)                                             //declaration of function pu()
    {                                                                           //defination of function pu() begins
        start.remove(a+" ONT");
        start.remove("AE");                                                     //adding and removing states from the current state caused due to performing operation PU
        start.add(a+" HOLD");
    }                                                                           //defination of function pu() ends
    
    public static void pd(String a)                                             //declaration of function pd()
    {                                                                           //defination of function pd() begins
        start.add(a+" ONT");
        start.add("AE");                                                        //adding and removing states from the current state caused due to performing operation PD
        start.remove(a+" HOLD");
    }                                                                           //defination of function pd() ends
    
    public static void stack(String a,String b)                                 //declaration of function stack()
    {                                                                           //defination of function stack() begins
        start.remove(a+" HOLD");
        start.remove(b+"CL");
        start.add("AE");                                                        //adding and removing states from the current state caused due to performing operation STACK
        start.add(a+" ON "+b);
    }                                                                           //defination of function stack() ends
    public static void unstack(String a,String b)                               //declaration of function unstack()
    {                                                                           //defination of function unstack() begins
        start.remove(a+" ON "+b);
        start.remove("AE");                                                     //adding and removing states from the current state caused due to performing operation UNSTACK
        start.add(b+" CL");
        start.add(a+" HOLD");
    }                                                                           //defination of function unstack() ends
    public static void plan()                                                   //declaration of function plan()
    {                                                                           //defination of function plan() begins
     String[] b=new String [3];
     b[0]="";
     b[1]="";
     b[2]="";
     String a;
        while(im.isEmpty()!=true)                                               
        {
            a=(String) im.pop();                                                //obtaining the operation to be performed
            b=a.split(" ");
            if(a!="AE"){
            if(start.contains(a))                                               // checking if the operation to be performed is already true in the current state
            {                                                                   //continue to the next iteration
            }
            else                                                                // else if the operation to be performed is not present in the current state then proceed
            {
            switch(b[1])                                                        //invoking specific functions to perform the required operation
            {
                case "PU": pu(b[0]); System.out.println(a);                     //printing PU action of the planning
                           break;
                case "PD": pd(b[0]);System.out.println(a);                      //printing PD action of the planning
                           break;
                case "STACK": stack(b[0],b[2]); System.out.println(a);          //printing STACK action of the planning
                           break;
                case "UNSTACK": unstack(b[0],b[2]); System.out.println(a);      //printing UNSTACK action of the planning
                           break;
                case "ON": on(b[0],b[2]);                                       
                           break;
                case "ONT":ont(b[0]);
                           break;
                case "CL": cl(b[0]);
                           break;
                case "HOLD": hold(b[0]);
                           break;
            }
            }
            }
            else
                ae();                                                           //invoking ae() function if AE is the action to be performed
        }
    }                                                                           //defination of function plan() ends
}
