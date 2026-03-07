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





});
