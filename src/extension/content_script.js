/*
 * Copyright (C) 2018 FU Berlin
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
*/

window.addEventListener("message", function(event) {

    if (event.source == window && event.data && isValidInputData(event.data)) {

        // notify background script
        chrome.runtime.sendMessage(event.data);
    }
});

addPayloadToWebsite();


function isValidInputData(data) {
    return typeof data.action !== "undefined" && typeof data.message !== "undefined"
}


function addPayloadToWebsite() {

    // add a value to let the website know, that the extension is installed
    document.body.classList.add("rapstore_extension_installed");

    // test connection to native messaging host through background script
    var connectionTestRequest = {action: "rapstore_test_connection_native_messaging_host", message: ""}

    chrome.runtime.sendMessage(connectionTestRequest, function(response) {

        if (chrome.runtime.lastError) {
            console.error(chrome.runtime.lastError.message);
        }

        if (response.success == true) {
            // add a value to let the website know, that the native messaging host is installed
            document.body.classList.add("rapstore_native_messaging_host_installed");
        }
    });
}
