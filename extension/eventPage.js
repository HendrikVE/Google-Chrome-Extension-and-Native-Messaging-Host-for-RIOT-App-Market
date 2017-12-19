/*
 * Copyright (C) 2017 Hendrik van Essen and FU Berlin
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
*/

var hostName = "de.fu_berlin.mi.riot_app_market";

var isFirefox = typeof InstallTrigger !== 'undefined';
var isChrome = !!window.chrome && !!window.chrome.webstore;

if (isChrome) {

    chrome.runtime.onMessageExternal.addListener(

        function(request, sender, sendResponse) {

            if (request.request != null) {

                if (request.request == "version") {
                    var manifest = chrome.runtime.getManifest();
                    sendResponse({version: manifest.version});
                }
                else if (request.request == "native_messaging_host_accessible") {
                    chrome.runtime.sendNativeMessage(hostName, {native_messaging_host_accessible: true},
                        function() {
                            if (chrome.runtime.lastError) {
                                if (chrome.runtime.lastError.message == "Specified native messaging host not found.") {

                                    sendResponse({success: false});
                                    return;
                                }
                            }

                            sendResponse({success: true});
                        }
                    );
                    // send a response asynchronously. See: https://developer.chrome.com/apps/runtime#event-onMessageExternal
                    return true;
                }
                else {
                    sendResponse({error: "unknown request type: " + request.request});
                }
            }
            else {
                //if output_archive is null, something did not work when building the application
                if (request.output_archive != null) {
                    chrome.runtime.sendNativeMessage(hostName, request,
                        function() {
                            if (chrome.runtime.lastError) {
                                if (chrome.runtime.lastError.message == "Specified native messaging host not found.") {
                                    alert("You need to install the riotam Native Messaging Host provided in riotam-chrome-integration/native-messaging-host/");
                                }
                            }
                        }
                    );
                }
            }
        }
    );
}
else if (isFirefox) {

    browser.runtime.onMessage.addListener(notify);

    function notify(message) {

        var sending = browser.runtime.sendNativeMessage("de.fu_berlin.mi.riot_app_market", message);
        sending.then(onResponse, onError);
    }

    function onResponse(message) {
        console.log("onResponse: " + message);
    }

    function onError(message) {
        console.log("onError: " + message);
    }
}
