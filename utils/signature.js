// Base64编码类
class Base64 {
    constructor() {
        this._keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
    }
    
    encode(input) {
        let output = "";
        let chr1, chr2, chr3, enc1, enc2, enc3, enc4;
        let i = 0;
        input = this._utf8_encode(input);
        while (i < input.length) {
            chr1 = input.charCodeAt(i++);
            chr2 = input.charCodeAt(i++);
            chr3 = input.charCodeAt(i++);
            enc1 = chr1 >> 2;
            enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);
            enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);
            enc4 = chr3 & 63;
            if (isNaN(chr2)) {
                enc3 = enc4 = 64;
            } else if (isNaN(chr3)) {
                enc4 = 64;
            }
            output = output +
                this._keyStr.charAt(enc1) + this._keyStr.charAt(enc2) +
                this._keyStr.charAt(enc3) + this._keyStr.charAt(enc4);
        }
        return output;
    }
    
    _utf8_encode(string) {
        string = string.replace(/\r\n/g,"\n");
        let utftext = "";
        for (let n = 0; n < string.length; n++) {
            let c = string.charCodeAt(n);
            if (c < 128) {
                utftext += String.fromCharCode(c);
            } else if((c > 127) && (c < 2048)) {
                utftext += String.fromCharCode((c >> 6) | 192);
                utftext += String.fromCharCode((c & 63) | 128);
            } else {
                utftext += String.fromCharCode((c >> 12) | 224);
                utftext += String.fromCharCode(((c >> 6) & 63) | 128);
                utftext += String.fromCharCode((c & 63) | 128);
            }
        }
        return utftext;
    }
}

// 自定义签名函数
function customSignature(str, secret) {
    let s = str + secret;
    // 步长抽样（每隔5个字符取1个）
    let sampled = "";
    for (let i = 0; i < s.length; i += 5) {
        sampled += s[i];
    }
    // 反转+charCode偏移
    let arr = [];
    for (let i = sampled.length - 1; i >= 0; i--) {
        arr.push(String.fromCharCode(sampled.charCodeAt(i) + 2));
    }
    let result = arr.join("");
    // Base64 编码
    let b64 = new Base64().encode(result);
    // 截取前32字符
    return b64.slice(0, 32);
}

// 生成带签名的URL
function generateSignedUrl(baseUrl, params, secret = "default_secret") {
    // 构建query字符串（排除signature参数）
    const queryParams = new URLSearchParams();
    for (const [key, value] of Object.entries(params)) {
        if (key !== 'signature') {
            queryParams.append(key, value);
        }
    }
    
    const queryString = queryParams.toString();
    const signature = customSignature(queryString, secret);
    
    // 添加签名参数
    queryParams.append('signature', signature);
    
    return baseUrl + '?' + queryParams.toString();
}

// 验证签名
function verifySignature(queryString, signature, secret = "default_secret") {
    const expectedSignature = customSignature(queryString, secret);
    return signature === expectedSignature;
}

// 从URL中提取query字符串
function getQueryStringFromUrl(url) {
    const urlObj = new URL(url);
    return urlObj.search.substring(1); // 去掉开头的'?'
}

// 导出函数（如果在Node.js环境中使用）
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        Base64,
        customSignature,
        generateSignedUrl,
        verifySignature,
        getQueryStringFromUrl
    };
}
