const btn = document.getElementById("scan");
btn.addEventListener("click", function() {
    btn.disabled = true;
    btn.innerHTML = "Scanning...";
    chrome.tabs.query({currentWindow: true, active: true}, function(tabs) {
        var url = tabs[0].url;
        var xhr = new XMLHttpRequest();
        xhr.open("GET", "http://127.0.0.1:5000/prediction?url=" + url, true);
        xhr.onload = function() {
            var models_passed = 0;
            var text = xhr.responseText;
            const p = document.getElementById("output");
            for (var i = 0; i < text.length; i++) {
                if (text.charAt(i) == "1") {
                    models_passed++;
                }
            }
            p.innerHTML = "This video passed: " + models_passed + "/4 of our models.";
            btn.disabled = false;
            btn.innerHTML = "Scan Transcript"
        }
        xhr.send();
    });
});