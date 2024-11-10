#include <WiFi.h>


#define RED_LED1 12
#define YELLOW_LED1 14
#define GREEN_LED1 27

// Block 2 LEDs
#define RED_LED2 26
#define YELLOW_LED2 25
#define GREEN_LED2 33


const char* ssid = "PianoMan. The RobotGuy.RareBrain";
const char* password = "6141AB19??";

WiFiServer server(80);

//unsigned long lastMessageTime = 0; 
//unsigned long timeoutDuration = 30000;  

void setup() {

   // Set all pins as output
  pinMode(RED_LED1, OUTPUT);
  pinMode(YELLOW_LED1, OUTPUT);
  pinMode(GREEN_LED1, OUTPUT);
  pinMode(RED_LED2, OUTPUT);
  pinMode(YELLOW_LED2, OUTPUT);
  pinMode(GREEN_LED2, OUTPUT);

  Serial.begin(115200);
  
  // Connect to WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");


  Serial.println("ESP32 IP Address: ");
  Serial.println(WiFi.localIP());

  // Start the server
  server.begin();

}

void loop() {
  WiFiClient client = server.available();  // Listen for incoming clients

  if (client) {
    Serial.println("New Client Connected");

    String command = client.readStringUntil('\n');
    command.trim();  // Remove any whitespace

    Serial.println("Command received: " + command);

    // Update the last message time
    //lastMessageTime = millis();

    // Control the built-in LED based on the received command
    if (command == "yes1" or command=="yes3") {
      Serial.println("ROAD1 is experiencing a Congestion");
      digitalWrite(RED_LED1, LOW);
      digitalWrite(RED_LED2, LOW);
      digitalWrite(GREEN_LED1, LOW);
      digitalWrite(GREEN_LED2, LOW);
      digitalWrite(YELLOW_LED1, HIGH);
      digitalWrite(YELLOW_LED2, HIGH);
      delay(5000);
      digitalWrite(YELLOW_LED1, LOW);
      digitalWrite(YELLOW_LED2, LOW);
      digitalWrite(GREEN_LED1, HIGH);
      digitalWrite(RED_LED2, HIGH);
      delay(30000);
      digitalWrite(GREEN_LED1, LOW);
      digitalWrite(RED_LED1, LOW);
      delay(2000);
    } 

    else if (command == "yes2" or command=="yes4") {
      Serial.println("ROAD2 is experiencing a Congestion");
      digitalWrite(RED_LED1, LOW);
      digitalWrite(RED_LED2, LOW);
      digitalWrite(GREEN_LED1, LOW);
      digitalWrite(GREEN_LED2, LOW);
      digitalWrite(YELLOW_LED2, HIGH);
      digitalWrite(YELLOW_LED1, HIGH);
      delay(5000);
      digitalWrite(YELLOW_LED2, LOW);
      digitalWrite(YELLOW_LED1, LOW);
      digitalWrite(RED_LED1, HIGH);
      digitalWrite(GREEN_LED2, HIGH);
      delay(30000);
      digitalWrite(GREEN_LED2, LOW);
      digitalWrite(RED_LED1, LOW);
      delay(2000);
    } 
    else if (command == "0") {
      Serial.println("LED OFF");
      digitalWrite(RED_LED1, LOW);
      digitalWrite(RED_LED2, LOW);
      digitalWrite(GREEN_LED1, LOW);
      digitalWrite(GREEN_LED2, LOW);
      digitalWrite(YELLOW_LED2, HIGH);
      digitalWrite(YELLOW_LED1, HIGH);
      delay(10000);
    }

    // Close the connection
    client.stop();
    Serial.println("Client Disconnected");
  }

  else{
    //Block 1
    digitalWrite(RED_LED1, LOW);
    digitalWrite(RED_LED2, LOW);
    digitalWrite(GREEN_LED1, LOW);
    digitalWrite(GREEN_LED2, LOW);
    digitalWrite(YELLOW_LED2, HIGH);
    digitalWrite(YELLOW_LED1, HIGH);  // Turn on yellow LED for Block 1
    delay(5000);
    digitalWrite(YELLOW_LED1, LOW);
    digitalWrite(YELLOW_LED2, LOW);
    //delay(2000);

    digitalWrite(GREEN_LED1, HIGH);  // Turn on green LED for Block 1
    digitalWrite(RED_LED2, HIGH);
    delay(10000);
    digitalWrite(GREEN_LED1, LOW);
    digitalWrite(RED_LED2, LOW);
    //delay(2000);

  //The yellow light should always go ON before a transition 
    digitalWrite(RED_LED1, LOW);
    digitalWrite(RED_LED2, LOW);
    digitalWrite(GREEN_LED1, LOW);
    digitalWrite(GREEN_LED2, LOW); 
    digitalWrite(YELLOW_LED2, HIGH);
    digitalWrite(YELLOW_LED1, HIGH);  // Turn on yellow LED for Block 1
    delay(10000);
    digitalWrite(YELLOW_LED1, LOW);
    digitalWrite(YELLOW_LED2, LOW);
    //delay(2000);

    digitalWrite(RED_LED1, HIGH);  // Turn on red LED for Block 1
    digitalWrite(GREEN_LED2, HIGH);
    delay(10000);
    digitalWrite(RED_LED1, LOW);
    digitalWrite(GREEN_LED2, LOW);
    //delay(2000);

    //Block 2
    digitalWrite(RED_LED1, LOW);
    digitalWrite(RED_LED2, LOW);
    digitalWrite(GREEN_LED1, LOW);
    digitalWrite(GREEN_LED2, LOW);

    digitalWrite(YELLOW_LED2, HIGH);
    digitalWrite(YELLOW_LED1, HIGH);  // Turn on yellow LED for Block 2
    delay(10000);
    digitalWrite(YELLOW_LED2, LOW);
    digitalWrite(YELLOW_LED1, LOW);
    //delay(2000);

    digitalWrite(RED_LED1, LOW);
    digitalWrite(RED_LED2, LOW);
    digitalWrite(GREEN_LED1, LOW);
    digitalWrite(GREEN_LED2, LOW);
    digitalWrite(RED_LED1, HIGH);
    digitalWrite(GREEN_LED2, HIGH);  // Turn on green LED for Block 2
    delay(10000);
    digitalWrite(RED_LED1, LOW);
    digitalWrite(GREEN_LED2, LOW);
    //delay(2000);

//The yellow light should always go ON before a transition
    digitalWrite(RED_LED1, LOW);
    digitalWrite(RED_LED2, LOW);
    digitalWrite(GREEN_LED1, LOW);
    digitalWrite(GREEN_LED2, LOW);
    digitalWrite(YELLOW_LED2, HIGH);
    digitalWrite(YELLOW_LED1, HIGH);  
    delay(10000);
    digitalWrite(YELLOW_LED1, LOW);
    digitalWrite(YELLOW_LED2, LOW);
    //delay(2000);

    digitalWrite(GREEN_LED1, HIGH);
    digitalWrite(RED_LED2, HIGH);  // Turn on red LED for Block 2
    delay(10000);
    digitalWrite(RED_LED2, LOW);
    digitalWrite(GREEN_LED1, LOW);
    //delay(2000);

  }

  // Check for timeout: if no message received in timeoutDuration, turn off LED
//  if (millis() - lastMessageTime > timeoutDuration) {
//    digitalWrite(ledPin, LOW);  // Turn off LED
    //Serial.println("No message received for 1 minute, LED OFF due to timeout.");
//  }
//  millis()==0;

}
