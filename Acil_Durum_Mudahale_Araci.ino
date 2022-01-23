#include <MySQL_Connection.h>
#include <MySQL_Cursor.h>
#include <WiFi.h>
#include <LiquidCrystal_I2C.h>

String x;
String x_prv = "0000";

const char *ssid = "iPhone";
const char *password = "######";


const int ledPin = 5;

String text = "                ";

bool connectedd = false;

LiquidCrystal_I2C lcd(0x27, 16, 2); // Bu kodu kullanırken ekranda yazı çıkmaz ise 0x27 yerine 0x3f yazınız !!
  WiFiClient client;
  MySQL_Connection conn((Client *)&client);
  MySQL_Cursor *cur_mem1 = new MySQL_Cursor(&conn);


char user[] = "kaan"; // MySQL user login username
char passwordSQL[] = "######"; // MySQL user login password

char cam1_query[] = "SELECT anomaly_1, anomaly_2, anomaly_3, anomaly_4 FROM lvad.cdtp where cam_id=1";
char cam2_query[] = "SELECT anomaly_1, anomaly_2, anomaly_3, anomaly_4 FROM lvad.cdtp where cam_id=2";

char anomaly1_string[] = "DURAN ARABA VAR";
char anomaly2_string[] = "TERS YÖNDE ARABA";
char anomaly3_string[] = "YOLDA HAYVAN";

long head_count1_cam1 = 0;
long head_count2_cam1 = 0;
long head_count3_cam1 = 0;
long head_count4_cam1 = 0;

long head_count1_cam2 = 0;
long head_count2_cam2 = 0;
long head_count3_cam2 = 0;
long head_count4_cam2 = 0;

IPAddress server_addr(92,205,4,52); // IP of the MySQL server here

int i = 0;


WiFiServer  server(80);
void setup() {
  pinMode(ledPin, OUTPUT);
  //Código de configuração aqui
  Serial.begin(115200);

  connectToNetwork();

  digitalWrite (ledPin, LOW);
}

void loop() {

  mySqlLoop();
}
void connectToNetwork() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
 
  while (WiFi.status() != WL_CONNECTED) {
    delay(100);
    Serial.println("Establishing connection to WiFi..");
    
  }
 
  Serial.println("Connected to network");
 
}
void mySqlLoop(){
  i++;
  row_values *row = NULL;  

  if (conn.connect(server_addr, 3306, user, passwordSQL)) {
    Serial.println("Database connected.");
    
  }
  else{
    Serial.println("Connection failed.");
    Serial.println("Recording data.");
  }

  cur_mem1->execute(cam1_query);
  column_names *columns1 = cur_mem1->get_columns();

  // Read the row (we are only expecting the one)
  do {
    row = cur_mem1->get_next_row();
    if (row != NULL) {
      head_count1_cam1 = atol(row->values[0]);
      head_count2_cam1 = atol(row->values[1]);
      head_count3_cam1 = atol(row->values[2]);
	head_count4_cam1 = atol(row->values[3]);
    }
  } while (row != NULL); 

  x = String(head_count1_cam1) + String(head_count2_cam1) + String(head_count3_cam1) + String(head_count4_cam2);

  if (x[3] == '1' || x[2] == '1' || x[1] == '1' || x[0] == '1')
  {
    digitalWrite (ledPin, HIGH);
    Serial.println("led yakılıyor");
  }
  else
  {
    digitalWrite (ledPin, LOW);
    Serial.println("led kapatılıyor");
  }

  x = x_prv;

  cur_mem1->execute(cam2_query);

  column_names *columns2 = cur_mem1->get_columns();

  do {
    row = cur_mem1->get_next_row();
    if (row != NULL) {
      head_count1_cam2 = atol(row->values[0]);
      head_count2_cam2 = atol(row->values[1]);
      head_count3_cam2 = atol(row->values[2]);
	head_count4_cam2 = atol(row->values[3]);
    }
  } while (row != NULL); 

  x = String(head_count1_cam2) + String(head_count2_cam2) + String(head_count3_cam2) + String(head_count4_cam2);

  if (x[3] == '1' || x[2] == '1' || x[1] == '1' || x[0] == '1')
  {
    digitalWrite (ledPin, HIGH);
    Serial.println("led yakılıyor");
  }
  else
  {
    digitalWrite (ledPin, LOW);
    Serial.println("led kapatılıyor");
  }

  x = x_prv;

 
  // Show the result
  Serial.print("  CAM1 VERİ = ");
  Serial.println(String(head_count1_cam1) + " " + String(head_count2_cam1) + " " + String(head_count3_cam1) + " " + String(head_count4_cam1));

  Serial.print("  CAM2 VERİ = ");
  Serial.println(String(head_count1_cam2) + " " + String(head_count2_cam2) + " " + String(head_count3_cam2) + " " + String(head_count4_cam2));

}
