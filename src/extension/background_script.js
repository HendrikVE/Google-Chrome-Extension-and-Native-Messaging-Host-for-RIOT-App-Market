/*
 * Copyright (C) 2018 Hendrik van Essen and FU Berlin
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
*/

var nativeMessagingHostName = "net.riot_apps.rapstore_nmh";

chrome.runtime.onMessage.addListener(listener);


function listener(request, sender, sendResponse) {

    var responseCallback = substituteResponseCallback;

    if (typeof sendResponse !== "undefined") {
        responseCallback = sendResponse;
    }

    chrome.runtime.sendNativeMessage(nativeMessagingHostName, request, responseCallback);

    /*
     * The sendResponse callback is only valid if used synchronously, or if the event handler returns true to
     * indicate that it will respond asynchronously. The sendMessage function's callback will be invoked automatically
     * if no handlers return true or if the sendResponse callback is garbage-collected.
    */
    return true;
}


function substituteResponseCallback(response) {

    if(chrome.runtime.lastError) {
        console.error(chrome.runtime.lastError.message);
    }
}
