# -*- coding: UTF-8 -*-
# @reference: https://github.com/superdashu/frida_with_wechat_applet/blob/master/hook.js
# @author: r3col
# @Time : 2022/9/17 15:29

import frida
import sys


def on_message(message, data):
    pass

def process():
    session = frida.attach('wechat.exe')
    script = session.create_script("""
var baseAddr = Module.findBaseAddress('libruntime_host_export.dll');
console.log('libruntime_host_export.dll baseAddr: ' + baseAddr);


var EncryptBufToFile = Module.findExportByName('libruntime_host_export.dll', 'EncryptBufToFile');

if (EncryptBufToFile) {

    console.log('EncryptBufToFile 函数地址: ' + EncryptBufToFile);

    // HOOK函数, 监听参数
    Interceptor.attach(EncryptBufToFile, {
        onEnter: function (args) {
            // 微信小程序AppId
            //this.appId = ptr(args[0]).readPointer().readAnsiString();
            // 微信小程序本地缓存文件路径
            //this.apkgFilePath = ptr(args[1]).readPointer().readAnsiString();
            this.apkgFilePath = "D://" + Math.random().toString().slice(-6) + ".wxapkg";
            // 小程序代码原始内容(未加密)
            this.originalData = Memory.readByteArray(args[2], args[3].toInt32());
            console.log("load...");
        },
        onLeave: function (retval) {
            console.log('文件解密成功', this.apkgFilePath);

            // 将未加密的包保存下来
            var f = new File(this.apkgFilePath, 'wb');
            f.write(this.originalData);
            f.flush();
            f.close();

            delete this.originalData;
        }
    });

} else {
    console.log('libruntime_host_export.dll 模块未加载, 请先打开界面中的小程序面板');
}
""")
    script.on('message', on_message)
    script.load()
    print("[!] Ctrl+D on UNIX, Ctrl+Z on Windows/cmd.exe to detach from instrumented program.\n\n")
    sys.stdin.read()
    session.detach()


if __name__ == '__main__':
    process()
