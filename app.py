from flask import Flask, request, redirect, session
import subprocess
import re

app = Flask(__name__)
app.secret_key = "darksecret123"

USERNAME = "admin"
PASSWORD = "dark123"

HTML_LOGIN = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CYBER LOGIN</title>
<style>
body{margin:0;background:black;font-family:monospace;color:#00ffcc;overflow:hidden;}
canvas{position:fixed;top:0;left:0;z-index:-1;}
.card{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
background:rgba(0,0,0,0.85);padding:25px;border-radius:20px;
box-shadow:0 0 40px #00ffcc55;text-align:center;width:90%;max-width:320px;}
h2{text-shadow:0 0 15px #00ffcc;}
.info{font-size:12px;color:#aaa;margin-bottom:5px;}
input{width:100%;padding:12px;margin:10px 0;background:transparent;
border:2px solid #00ffcc55;border-radius:10px;color:#00ffcc;}
button{width:100%;padding:12px;border:none;border-radius:10px;
background:#00ffcc;font-weight:bold;cursor:pointer;}
button:hover{box-shadow:0 0 20px #00ffcc;}
.status{margin-top:10px;color:yellow;font-size:13px;}
</style>
</head>
<body>

<canvas id="matrix"></canvas>

<div class="card">
<h2>💀 CYBER ACCESS</h2>

<div class="info" id="date"></div>
<div class="info" id="clock"></div>
<div class="info" id="device"></div>
<div class="info" id="ip"></div>

<form method="POST" onsubmit="return fx()">
<input name="user" placeholder="Username" required>
<input id="pass" name="pass" type="password" placeholder="Password" required>
<button>LOGIN</button>
<div id="status" class="status"></div>
</form>
</div>

<audio id="s" src="https://www.soundjay.com/button/sounds/button-16.mp3"></audio>

<script>
function fx(){
document.getElementById("s").play();
document.getElementById("status").innerText="Authenticating...";
setTimeout(()=>{document.forms[0].submit();},1500);
return false;
}

let d=new Date();
let hari=["Minggu","Senin","Selasa","Rabu","Kamis","Jumat","Sabtu"];
let bulan=["Januari","Februari","Maret","April","Mei","Juni","Juli","Agustus","September","Oktober","November","Desember"];
document.getElementById("date").innerText=
hari[d.getDay()]+", "+d.getDate()+" "+bulan[d.getMonth()]+" "+d.getFullYear();

setInterval(()=>{
document.getElementById("clock").innerText=new Date().toLocaleTimeString();
},1000);

document.getElementById("device").innerText="Device: "+navigator.userAgent;

fetch("https://api.ipify.org?format=json")
.then(r=>r.json()).then(d=>{
document.getElementById("ip").innerText="IP: "+d.ip;
});

/* MATRIX */
let c=document.getElementById("matrix"),ctx=c.getContext("2d");
c.width=window.innerWidth;c.height=window.innerHeight;
let letters="01".split(""),font=14,cols=c.width/font,drops=[];
for(let x=0;x<cols;x++)drops[x]=1;
function draw(){
ctx.fillStyle="rgba(0,0,0,0.05)";
ctx.fillRect(0,0,c.width,c.height);
ctx.fillStyle="#0f0";ctx.font=font+"px monospace";
for(let i=0;i<drops.length;i++){
let t=letters[Math.floor(Math.random()*letters.length)];
ctx.fillText(t,i*font,drops[i]*font);
if(drops[i]*font>c.height&&Math.random()>0.975)drops[i]=0;
drops[i]++;
}}
setInterval(draw,33);
</script>

</body>
</html>
"""

HTML_PANEL = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
body{background:#0d0d0d;color:#00ffcc;font-family:monospace;text-align:center;}
h1{text-shadow:0 0 15px #00ffcc;}
.box{background:#111;padding:20px;border-radius:15px;
box-shadow:0 0 25px #00ffcc33;display:inline-block;margin-top:30px;}
input{width:90%;padding:10px;border-radius:8px;border:none;background:black;color:#00ffcc;}
button{padding:10px;margin:5px;border:none;border-radius:8px;background:#00ffcc;cursor:pointer;}
img{margin-top:10px;width:250px;border-radius:10px;}
.status{margin-top:10px;color:yellow;}
</style>
</head>
<body>

<h1>💀 DARK PANEL</h1>

<div class="box">
<input id="url" placeholder="URL YouTube"><br><br>
<button onclick="play()">▶ Play</button>
<button onclick="mp3()">⬇ MP3</button>

<div><img id="thumb" style="display:none;"></div>
<div id="status" class="status"></div>
</div>

<script>
function vid(url){
let r=/(?:youtube\\.com.*v=|youtu\\.be\\/)([^&]+)/;
let m=url.match(r);return m?m[1]:null;
}
function thumb(url){
let id=vid(url);
if(id){
let i=document.getElementById("thumb");
i.src="https://img.youtube.com/vi/"+id+"/hqdefault.jpg";
i.style.display="block";
}
}
function play(){
let u=document.getElementById("url").value;
thumb(u);
fetch("/play?url="+encodeURIComponent(u))
.then(r=>r.text()).then(d=>document.getElementById("status").innerText=d);
}
function mp3(){
let u=document.getElementById("url").value;
thumb(u);
fetch("/mp3?url="+encodeURIComponent(u))
.then(r=>r.text()).then(d=>document.getElementById("status").innerText=d);
}
</script>

</body>
</html>
"""

def valid(u):
    return re.match(r'^https?://', u)

@app.route("/", methods=["GET","POST"])
def login():
    if request.method=="POST":
        if request.form["user"]==USERNAME and request.form["pass"]==PASSWORD:
            session["login"]=True
            return redirect("/panel")
    return HTML_LOGIN

@app.route("/panel")
def panel():
    if not session.get("login"):
        return redirect("/")
    return HTML_PANEL

@app.route("/play")
def play():
    if not session.get("login"):
        return "Unauthorized"
    url=request.args.get("url")
    if not valid(url):
        return "URL tidak valid"
    subprocess.Popen(["mpv", url])
    return "▶ Playing..."

@app.route("/mp3")
def mp3():
    if not session.get("login"):
        return "Unauthorized"
    url=request.args.get("url")
    if not valid(url):
        return "URL tidak valid"
    subprocess.call(["yt-dlp","-x","--audio-format","mp3",url])
    return "⬇ Download selesai!"

app.run(host="0.0.0.0", port=5000)
