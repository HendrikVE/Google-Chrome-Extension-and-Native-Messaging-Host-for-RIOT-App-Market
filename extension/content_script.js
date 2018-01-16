/*
 * Copyright (C) 2017 FU Berlin
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
*/

window.addEventListener("message", function(event) {

    if (event.source == window && event.data && event.data.action == "rapstore") {
        // notify background script
        chrome.runtime.sendMessage(event.data);
    }
});

// add a value to let the website know, that the extension is installed
document.body.classList.add("rapstore_extension_installed");

// test connection to native messaging host through background script
var connectionTestRequest = {action: "test_connection_native_messaging_host"}
chrome.runtime.sendMessage(connectionTestRequest, function(response) {

    if (chrome.runtime.lastError) {
        console.error(chrome.runtime.lastError.message);
    }

    console.log("send to background script");

    if (response.success == true) {
        // add a value to let the website know, that the native messaging host is installed
        document.body.classList.add("rapstore_native_messaging_host_installed");
    }
});
