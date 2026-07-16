const SpeechRecognition =
window.SpeechRecognition ||
window.webkitSpeechRecognition;

if(SpeechRecognition){

    const recognition = new SpeechRecognition();

    recognition.lang = "hi-IN";

    recognition.continuous = false;

    recognition.interimResults = true;

    recognition.maxAlternatives = 1;

    let listening = false;

    micBtn.onclick = function(){

        if(listening){

            recognition.stop();

            return;

        }

        recognition.start();

    };

    recognition.onstart = function(){

        listening = true;

        micBtn.innerHTML = "🔴";

        micBtn.style.background = "#ff4d4d";

        input.placeholder = "Listening...";

    };

    recognition.onresult = function(event){

        let transcript = "";

        for(
            let i = event.resultIndex;
            i < event.results.length;
            i++
        ){

            transcript += event.results[i][0].transcript;

        }

        input.value = transcript;

    };

    recognition.onend = function(){

        listening = false;

        micBtn.innerHTML = "🎤";

        micBtn.style.background = "";

        input.placeholder = "Ask your health question...";

        if(input.value.trim()!==""){

            sendMessage();

        }

    };

    recognition.onerror = function(event){

        console.log(event.error);

        listening = false;

        micBtn.innerHTML = "🎤";

        micBtn.style.background = "";

        input.placeholder = "Ask your health question...";

    };

}
else{

    console.log("Speech Recognition not supported.");

}