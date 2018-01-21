/*
 * Copyright (C) 2017 Hendrik van Essen and FU Berlin
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
*/

var nativeMessagingHostName = "de.fu_berlin.mi.riot_app_market";

chrome.runtime.onMessage.addListener(listener);

function listener(request, sender, sendResponse) {

    if(request.action == "test_connection_native_messaging_host") {
        chrome.runtime.sendNativeMessage(nativeMessagingHostName, request, sendResponse);
    }
    else {
        chrome.runtime.sendNativeMessage(nativeMessagingHostName, request, function(response) {
            if(chrome.runtime.lastError) {
                console.error(chrome.runtime.lastError.message);
            }
        });
    }

    /*
     * The sendResponse callback is only valid if used synchronously, or if the event handler returns true to
     * indicate that it will respond asynchronously. The sendMessage function's callback will be invoked automatically
     * if no handlers return true or if the sendResponse callback is garbage-collected.
    */
    return true;
}
