
var hostName = "de.fu_berlin.mi.riot_app_market";

chrome.runtime.onMessageExternal.addListener(
    function(request, sender, sendResponse) {

        if (request.request != null) {

            if (request.request == "version") {
                var manifest = chrome.runtime.getManifest();
                sendResponse({version: manifest.version});
            }
            else {
                sendResponse({error: "unknown request type: " + request.request});
            }
        }
        
        //if output_file is null, something did not work when building the application
        if (request.output_file != null) {
            chrome.runtime.sendNativeMessage(hostName, request,
                function() {
                    if (chrome.runtime.lastError.message == "Specified native messaging host not found.") {
                        alert("You need to install the riotam Native Messaging Host provided in riotam-chrome-integration/native-messaging-host/");
                    }
                }
            );
        }
    }
);