#include "CTBot.h"
CTBot myBot;
String ssid = "";
String pass = "";
String token = "";
int rele = 5;  
void setup() {
	myBot.wifiConnect(ssid, pass);
	myBot.setTelegramToken(token);
	pinMode(rele, OUTPUT);
	digitalWrite(rele, LOW);
  Serial.begin(115200);
  Serial.println("Iniciando bot...");
}
void loop() {
	// a variable to store telegram message data
	TBMessage msg;
	if (myBot.getNewMessage(msg)) {
		if (msg.text.equals("/xxxxxx")) {
      Serial.println("Chat");
      Serial.println(msg.chatInstance);
      Serial.println("Sender");
      Serial.println(msg.sender.id);
			digitalWrite(rele, HIGH);
      delay(100);
      digitalWrite(rele, LOW);
			myBot.sendMessage(msg.sender.id, "OK");
		}
	}
}
