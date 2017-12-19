/*
 * Copyright (C) 2017 FU Berlin
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
*/

window.addEventListener("message", function(event) {
    if (event.source == window &&
        event.data &&
        event.data.direction == "rapstore") {

        // notify background script
        browser.runtime.sendMessage(event.data.message);
    }
});
