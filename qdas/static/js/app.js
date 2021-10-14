//webkitURL is deprecated but nevertheless
URL = window.URL || window.webkitURL;

var gumStream;                      //stream from getUserMedia()
var rec;                            //Recorder.js object
var input;                          //MediaStreamAudioSourceNode we'll be recording

// shim for AudioContext when it's not avb.
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext //audio context to help us record
// let max = document.getElementsByTagName("audio").length;

for (let i = 1; i <= max; i++) {
    document.getElementById("recordButton_" + i).addEventListener("click", () => { startRecording(i) });
    document.getElementById("stopButton_" + i).addEventListener("click", () => {stopRecording(i)});
    document.getElementById("pauseButton_" + i).addEventListener("click", () => { pauseRecording(i) });
}

function startRecording(index) {
    console.log("recordButton clicked");

    var myList = document.getElementById('recordingsList_'+index)
    myList.innerHTML = '';

    /*
        Simple constraints object, for more advanced audio features see
        https://addpipe.com/blog/audio-constraints-getusermedia/
    */
    var constraints = { audio: true, video:false }

    /*
        Disable the record button until we get a success or fail from getUserMedia()
    */

    for (let i = 1; i <= max; i++)
        document.getElementById("recordButton_" + i).disabled = true;

    document.getElementById("stopButton_" + index).disabled = false;
    document.getElementById("pauseButton_" + index).disabled = false

    /*
        We're using the standard promise based getUserMedia()
        https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia
    */

    navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
        console.log("getUserMedia() success, stream created, initializing Recorder.js ...");

        /*
            create an audio context after getUserMedia is called
            sampleRate might change after getUserMedia is called, like it does on macOS when recording through AirPods
            the sampleRate defaults to the one set in your OS for your playback device

        */
        audioContext = new AudioContext();

        /*  assign to gumStream for later use  */
        gumStream = stream;

        /* use the stream */
        input = audioContext.createMediaStreamSource(stream);

        /*
            Create the Recorder object and configure to record mono sound (1 channel)
            Recording 2 channels  will double the file size
        */
        rec = new Recorder(input,{numChannels:1})

        //start the recording process
        rec.record()

        console.log("Recording started");

    }).catch(function(err) {
        //enable the record button if getUserMedia() fails
        for (let i = 1; i <= max; i++)
            document.getElementById("recordButton_" + i).disabled = false;

        document.getElementById("stopButton_" + index).disabled = true;
        document.getElementById("pauseButton_" + index).disabled = true
    });
}

function pauseRecording(index){
    console.log("pauseButton clicked rec.recording=",rec.recording );
    if (rec.recording){
        //pause
        rec.stop();
        document.getElementById("pauseButton_" + index).innerHTML="Resume";
    }else{
        //resume
        rec.record()
        document.getElementById("pauseButton_" + index).innerHTML="Pause";

    }
}

function stopRecording(index) {
    console.log("stopButton clicked");

    //disable the stop button, enable the record too allow for new recordings
    for (let i = 1; i <= max; i++)
        document.getElementById("recordButton_" + i).disabled = false;

    document.getElementById("stopButton_" + index).disabled = true;
    document.getElementById("pauseButton_" + index).disabled = true

    //reset button just in case the recording is stopped while paused
    document.getElementById("pauseButton_" + index).innerHTML="Pause";

    //tell the recorder to stop the recording
    rec.stop();

    //stop microphone access
    gumStream.getAudioTracks()[0].stop();

    //create the wav blob and pass it on to createDownloadLink
    rec.exportWAV((blob) => { createDownloadLink(blob, index) });
}

function createDownloadLink(blob, index) {

    var url = URL.createObjectURL(blob);
    var au = document.createElement('audio');
    var li = document.createElement('li');
    var link = document.createElement('a');

    //name of .wav file to use during submit and download (without extendion)
    var filename = new Date().toISOString();

    //add controls to the <audio> element
    au.controls = true;
    au.src = url;
    link.href = url;

    //add the new audio element to li
    li.appendChild(au);

    //add the save to disk link to li
    li.appendChild(link);

    //submit link
    var submit = document.createElement('a');
    submit.href="#";
    submit.innerHTML = "Submit";
    submit.setAttribute("name", "submitButton");
    submit.setAttribute("id", "submitButton" + index);
    submit.addEventListener("click", function(event){
          var xhr=new XMLHttpRequest();
          xhr.onload=function(e) {
              if(this.readyState === 4) {
                  console.log("Server returned: ",e.target.responseText);
              }
          };
          var fd=new FormData();
          fd.append("audio_data",blob);
          xhr.open("POST","/response",true);
          xhr.send(fd);
    })
    li.appendChild(document.createTextNode (" "))//add a space in between
    li.appendChild(submit)//add the submit link to li

    //add the li element to the ol
    console.log('recordingsList_' + index)
    document.getElementById('recordingsList_' + index).appendChild(li);

    var recButtons = document.querySelectorAll( "button[id^='recordButton_']" );
    console.log(recButtons.length)
    var lastSubmitButton = document.getElementById("submitButton" + recButtons.length)
    lastSubmitButton.setAttribute("href", "/success")

}
