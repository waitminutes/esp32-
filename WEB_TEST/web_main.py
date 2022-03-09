class web_viewer():
    def config_page():
        return b'''
            <!DOCTYPE html>
            <html lang="en" xml:lang="en">

            <head>

            <title>MYESP32 AP Test</title>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="icon" href="data:image/ico;base64,aWNv">                  
            </head>
            <body style="background-color: #f3e8bc ">
            <center>
            <h1>WEB服务器测试</h1>


            <div>
                <p>
                    LED状态: <font color="#FF0000"><span id="switch_state">初始化</span></font><br>
                </p>
            </div>
            <div>
                <p>
                <form name="form" method="post" action="#"> 
                手动操作
                </form>
                    
                    <input type="button" name="powerOn" onclick="ONSEND();" value="开灯"> 
                    <input type="button" name="powerOff" onclick="OFFSEND();" value="关灯"> 
                    
                </p>

            </div>
            <div>
                    <p>
                    温度： <font color="#FF0000"><span id="TEST_number">loading</span></font>&nbsp℃&nbsp&nbsp&nbsp  
                    湿度： <font color="#FF0000"><span id="ON_number">loading</span></font>&nbsp%&nbsp&nbsp&nbsp
                    
                    </p>
            </div>
            <div>
                    <p>
                    光照强度： <font color="#FF0000"><span id="light_number">loading</span></font>&nbsp&nbsp&nbsp&nbsp  
                    
                    
                    </p>
            </div>            
            <div>
                <p>当前时间： 
                <font color="#FF0000" id="TIME_message">xxxx-xx-xx xx:xx:xx</font>
                </p>
            </div>

            </center>
                <script>                      
                setInterval(getData1, 5000);
                
                
                function getData1() {
                var xhttp = new XMLHttpRequest();
                xhttp.onreadystatechange = function() {
                    if (this.readyState == 4 && this.status == 200) {
                    document.getElementById("TEST_number").innerHTML =
                    this.responseText;
                    }
                };
                
                xhttp.open("GET", "temperature_numberer", true);
                xhttp.send();
                setTimeout(getData2,10)
                setTimeout(getData3,10)
                }
                function getData2() {
                var xhttp = new XMLHttpRequest();
                xhttp.onreadystatechange = function() {
                    if (this.readyState == 4 && this.status == 200) {
                    document.getElementById("ON_number").innerHTML =
                    this.responseText;
                    }
                };
                
                xhttp.open("GET", "humidity_numberer", true);
                xhttp.send();
                
                }
                function getData3() {
                var xhttp = new XMLHttpRequest();
                xhttp.onreadystatechange = function() {
                    if (this.readyState == 4 && this.status == 200) {
                    document.getElementById("light_number").innerHTML =
                    this.responseText;
                    }
                };
                
                xhttp.open("GET", "light_intensity", true);
                xhttp.send();
                
                }
                 
                function ONSEND(){
                    var xhttp = new XMLHttpRequest();
                    xhttp.onreadystatechange = function() {

                    if (this.readyState == 4 && this.status == 200) {
                    document.getElementById("switch_state").innerHTML =
                    this.responseText;
                    }
                };
                xhttp.open("GET", "LED_ON", true); 
                xhttp.send();
                }

                function OFFSEND(){
                    var xhttp = new XMLHttpRequest();
                    xhttp.onreadystatechange = function() {           
                    if (this.readyState == 4 && this.status == 200) {
                    document.getElementById("switch_state").innerHTML =
                    this.responseText;
                     }
                };
                xhttp.open("GET", "LED_OFF", true); 
                xhttp.send();  
                }

                </script>

            </body>
            </html>'''

