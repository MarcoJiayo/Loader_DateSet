// ==UserScript==
// @name         google��������ҳ����ת
// @version      1.0.1
// @author       ����name
// @namespace    https://greasyfork.org/zh-CN/users/378268
// @include      *

//               �� jQuery�����ļ� ��
// @require      https://greasyfork.org/scripts/39025-micoua-jquery-min-js/code/Micoua_jQuery_min_js.js?version=255336
//               �� jQueryUI�����ļ� ��
// @require      https://greasyfork.org/scripts/40306-micoua-jqueryui-min-js/code/Micoua_jQueryUI_min_js.js?version=267377

// @grant        unsafeWindow
// @grant        GM_setValue
// @grant        GM_getValue
// @grant        GM_deleteValue
// @grant        GM_listValues
// ==/UserScript==

(function () {
    /**
     * �����
     */
    function main() {
        gotoWeb(); // ��ת��ҳ
    }

    /**
     * ȫ�ֱ���
     */
    var currentURL = window.location.href; // ��ȡ��ǰ��ҳ��ַ
    var url = "https://www.google.com.hk/?hl=zh-cn"; // Ԥ������ת��ҳ

    /**
     * ��ת��ҳ
     */
    gotoWeb = function () {
        /** ����������ҳ */
        var urls = {
            "googleHelpURLs": [
                "123.hao245.com",
                "360.hao245.com",
                "hao123.com/?tn="
            ]
        };
        /** ������վ����ת */
        var googleHelpURLs = GM_getValue("googleHelpURLs") === undefined ? urls.googleHelpURLs : $.merge(GM_getValue("googleHelpURLs"), urls.googleHelpURLs);
        for (var i = 0; i < googleHelpURLs.length; i++) { if (currentURL.indexOf(googleHelpURLs[i]) != -1) { window.location.href = url; return; } }
    };

    /**
     * �������������ݺ����������
     */
    if (true) main();
})();