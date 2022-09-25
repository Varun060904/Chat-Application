# Chat-Application
A simple chat application using Python and MySql !

So how this works ,
      Firstly the server runs , using socket module in python. Then it accepts connections when user try to run the app.
      Then during the login process , server recives the username and password from the user and using mysql it checks and verifys.
      Once verified it skips to next step of sending the data which contains all the users available on the server .
      Once the user selects which user he wants to chat with , the chat history previously available is sent , 
      else if the conversation is new a random 5 digit named text file gets created which is updated in Mysql database for rewriting purpose
      This whole thing runs in a while loop , so users can use functions multiple times !
   
