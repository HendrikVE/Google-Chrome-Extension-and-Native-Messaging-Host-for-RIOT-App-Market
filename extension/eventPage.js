chrome.runtime.onMessageExternal.addListener(
    function(request, sender, sendResponse) {
        
        //if output_file is null, something did not work when building the application
        if(request.output_file != null) {
            var hostName = "de.fu_berlin.mi.riot_app_market";
            chrome.runtime.sendNativeMessage(hostName, request,
                function(response) {
                console.log("Received " + response);
            });
        }
    }
);