const input = document.getElementById("userInput");

const sendBtn = document.getElementById("sendBtn");

const micBtn = document.getElementById("micBtn");

const cameraBtn = document.getElementById("cameraBtn");

const uploadBtn = document.getElementById("uploadBtn");

const chatContainer = document.getElementById("chatContainer");


// =====================================
// ADD MESSAGE
// =====================================

function addMessage(text, type){

    const msg = document.createElement("div");

    msg.className = type;

    msg.innerHTML = text;

    chatContainer.appendChild(msg);

    chatContainer.scrollTop = chatContainer.scrollHeight;

}


// =====================================
// SEND MESSAGE
// =====================================

function sendMessage(){

    let text = input.value.trim();

    if(text==="") return;

    addMessage(text,"user");

    input.value="";

    // TODO
    // Python Backend ko yahi connect karna hai

    setTimeout(function(){

        addMessage(
            "🤖 AI Response will come from Streamlit Backend.",
            "bot"
        );

    },700);

}

sendBtn.onclick = sendMessage;


// =====================================
// ENTER KEY
// =====================================

input.addEventListener("keydown",function(e){

    if(e.key==="Enter"){

        sendMessage();

    }

});


// =====================================
// CAMERA
// =====================================

let cameraOn=false;

cameraBtn.onclick=function(){

    cameraOn=!cameraOn;

    if(cameraOn){

        cameraBtn.innerHTML="📹";

        cameraBtn.style.background="#2563eb";

        console.log("Camera ON");

    }

    else{

        cameraBtn.innerHTML="📷";

        cameraBtn.style.background="";

        console.log("Camera OFF");

    }

};


// =====================================
// FILE UPLOAD
// =====================================

uploadBtn.onclick=function(){

    const file=document.createElement("input");

    file.type="file";

    file.accept="image/*,.pdf";

    file.click();

    file.onchange=function(){

        if(file.files.length>0){

            addMessage(

                "📎 "+file.files[0].name,

                "user"

            );

            console.log(file.files[0]);

        }

    };

};


// =====================================
// AUTO FOCUS
// =====================================

window.onload=function(){

    input.focus();

};