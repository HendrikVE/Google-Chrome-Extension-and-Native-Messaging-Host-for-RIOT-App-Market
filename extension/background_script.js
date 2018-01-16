/*
 * Copyright (C) 2017 Hendrik van Essen and FU Berlin
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
*/

var nativeMessagingHostName = "de.fu_berlin.mi.riot_app_market";

chrome.runtime.onMessage.addListener(listener);

function listener(request, sender, extensionCallback) {

    console.log("listened on background script");

    if(request.action == "test_connection_native_messaging_host") {
        chrome.runtime.sendNativeMessage(nativeMessagingHostName, JSON.stringify(request), extensionCallback);
    }
    else {
        chrome.runtime.sendNativeMessage(nativeMessagingHostName, request, function(response) {
            if(chrome.runtime.lastError) {
                console.error(chrome.runtime.lastError.message);
            }
        });
    }

    // call callback asynchronously
    return true;
}
