/*
 * Copyright (C) 2017 Hendrik van Essen and FU Berlin
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
*/

var hostName = "de.fu_berlin.mi.riot_app_market";

chrome.runtime.onMessage.addListener(notify);

function notify(message) {

    var sending = chrome.runtime.sendNativeMessage("de.fu_berlin.mi.riot_app_market", message);
    sending.then(onResponse, onError);
}

function onResponse(message) {
    console.log("onResponse: " + message);
}

function onError(message) {
    console.log("onError: " + message);
}
