$(document).ready(function () {

    /* ── helpers ── */
    function nowTime() {
        const d = new Date();
        return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }

    function scrollToBottom() {
        const box = document.getElementById("chat-canvas-body");
        box.scrollTop = box.scrollHeight;
    }

    function escapeHtml(text) {
        return String(text)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    /* ── Typing indicator (shown while SAM thinks) ── */
    function showTyping() {
        removeTyping();
        const chatBox = document.getElementById("chat-canvas-body");
        chatBox.innerHTML += `
        <div class="msg-row receiver" id="typingRow">
            <div class="msg-avatar sam-avatar">S</div>
            <div class="msg-bubble-wrap">
                <div class="receiver_message msg-bubble">
                    <div class="typing-dots">
                        <span></span><span></span><span></span>
                    </div>
                </div>
            </div>
        </div>`;
        scrollToBottom();
    }

    function removeTyping() {
        const row = document.getElementById("typingRow");
        if (row) row.remove();
    }

    /* ── Display SAM's spoken text (siri wave section) ── */
    eel.expose(DisplayMessage);
    function DisplayMessage(message) {
        $(".siri-message").text(message);
    }

    /* ── Show main oval (idle state) ── */
    eel.expose(ShowHood);
    function ShowHood() {
        $('#oval').attr("hidden", false);
        $('#siriwave').attr("hidden", true);
    }

    /* ── Sender bubble (User typed / said) ── */
    eel.expose(senderText);
    function senderText(message) {
        if (!message || message.trim() === "") return;
        removeTyping();
        const chatBox = document.getElementById("chat-canvas-body");
        chatBox.innerHTML += `
        <div class="msg-row sender">
            <div class="msg-avatar user-avatar">U</div>
            <div class="msg-bubble-wrap">
                <div class="sender_message msg-bubble">${escapeHtml(message)}</div>
                <div class="msg-time">${nowTime()}</div>
            </div>
        </div>`;
        scrollToBottom();
        showTyping(); // show SAM thinking after user sends
    }

    /* ── Receiver bubble (SAM reply) ── */
    let lastReceiverMessage = "";
    let lastReceiverTime = 0;
    eel.expose(receiverText);
    function receiverText(message) {
        if (!message || message.trim() === "") return;

        const cleanMessage = message.trim();
        const now = Date.now();

        if (cleanMessage === lastReceiverMessage && now - lastReceiverTime < 2000) {
            console.log("Duplicate receiver message skipped:", cleanMessage);
            removeTyping();
            return;
        }

        lastReceiverMessage = cleanMessage;
        lastReceiverTime = now;

        removeTyping();
        const chatBox = document.getElementById("chat-canvas-body");
        chatBox.innerHTML += `
        <div class="msg-row receiver">
            <div class="msg-avatar sam-avatar">S</div>
            <div class="msg-bubble-wrap">
                <div class="receiver_message msg-bubble">${escapeHtml(cleanMessage)}</div>
                <div class="msg-time">${nowTime()}</div>
            </div>
        </div>`;
        scrollToBottom();
    }

    /* ── In-canvas input bar ── */
    $("#canvasInput").on("keypress", function (e) {
        if (e.which === 13) {
            e.preventDefault();
            const msg = $(this).val().trim();
            if (msg) {
                $(this).val("");
                window.PlayAssistant && window.PlayAssistant(msg);
            }
        }
    });

    $("#canvasSendBtn").on("click", function () {
        const msg = $("#canvasInput").val().trim();
        if (msg) {
            $("#canvasInput").val("");
            window.PlayAssistant && window.PlayAssistant(msg);
        }
    });

    /* ── Set today's date in divider ── */
    const today = new Date().toLocaleDateString([], { weekday: 'long', month: 'short', day: 'numeric' });
    const dateLbl = document.getElementById("chat-date-label");
    if (dateLbl) dateLbl.textContent = today;

});