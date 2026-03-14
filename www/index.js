// siri configuration
window.addEventListener("DOMContentLoaded", () => {
  var siriWave = new SiriWave({
    container: document.getElementById("siri-container"),
    width: 640,
    height: 200,
    style: 'ios'
  });

  $('#MicBtn').click(function () {
    eel.playsoundwww()
    $('#oval').attr("hidden", true);
    $('#siriwave').attr("hidden", false);
    eel.allcommand()()
    
  });

function doc_keyUp(e) {
  console.log("KEY EVENT:", e.code, "meta:", e.metaKey)

  if (e.code === 'KeyJ' && e.metaKey) {
    eel.playsoundwww()
    $("#oval").attr("hidden", true)
    $("#siriwave").attr("hidden", false)
    eel.allcommand()()
  }
}

window.addEventListener('keydown', doc_keyUp)
 function PlayAssistant(message) {

        if (message != "") {

            $("#oval").attr("hidden", true);
            $("#siriwave").attr("hidden", false);
            eel.allcommand(message);
            $("#chatbox").val("")
            $("#MicBtn").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);

        }

    }
    window.PlayAssistant = PlayAssistant; // expose for in-canvas input bar
function ShowHideButton(message) {
  if (message.length == 0) {
    $("#MicBtn").attr('hidden', false);
    $("#SendBtn").attr('hidden', true);
  }
  else {
    $("#MicBtn").attr('hidden', true);
    $("#SendBtn").attr('hidden', false);
  }
}
   $("#chatbox").keyup(function () {

        let message = $("#chatbox").val();
        ShowHideButton(message)

    });

    // send button event handler
    $("#SendBtn").click(function () {

        let message = $("#chatbox").val()
        PlayAssistant(message)

    });

    // enter key handler
    $("#chatbox").keypress(function (e) {
        if (e.which === 13) {
            e.preventDefault();
            let message = $("#chatbox").val();
            PlayAssistant(message);
        }
    });
  
  });