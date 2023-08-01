#SingleInstance force
#Persistent
#include Lib\AutoHotInterception.ahk

AHI := new AutoHotInterception()

keyboardId := AHI.GetKeyboardId(0x258A, 0x0049) ; replace with your keyboard's ID

AHI.SubscribeKey(keyboardId, GetKeySC("Space"), true, Func("BackLight"))
AHI.SubscribeKey(keyboardId, GetKeySC("RShift"), true, Func("TopLight"))
AHI.SubscribeKey(keyboardId, GetKeySC("NumpadEnter"), true, Func("Fan"))
AHI.SubscribeKey(keyboardId, GetKeySC("1"), true, Func("Socket"))
return

BackLight(state){
    if (state = 1) {
        url := "http://192.168.1.3:5069/jsonex"
        whr := ComObjCreate("WinHttp.WinHttpRequest.5.1")
        whr.Open("POST", url)
        whr.SetRequestHeader("Content-Type", "application/json")
        jsonPayload := "{""appliance"":""bl""}"
        whr.Send(jsonPayload)
    }
}

TopLight(state){
    if (state = 1) {
        url := "http://192.168.1.3:5069/jsonex"
        whr := ComObjCreate("WinHttp.WinHttpRequest.5.1")
        whr.Open("POST", url)
        whr.SetRequestHeader("Content-Type", "application/json")
        jsonPayload := "{""appliance"":""tl""}"
        whr.Send(jsonPayload)
    }
}

Fan(state){
    if (state = 1) {
        url := "http://192.168.1.3:5069/jsonex"
        whr := ComObjCreate("WinHttp.WinHttpRequest.5.1")
        whr.Open("POST", url)
        whr.SetRequestHeader("Content-Type", "application/json")
        jsonPayload := "{""appliance"":""f""}"
        whr.Send(jsonPayload)
    }
}

Socket(state){
    if (state = 1) {
        url := "http://192.168.1.3:5069/jsonex"
        whr := ComObjCreate("WinHttp.WinHttpRequest.5.1")
        whr.Open("POST", url)
        whr.SetRequestHeader("Content-Type", "application/json")
        jsonPayload := "{""appliance"":""s""}"
        whr.Send(jsonPayload)
    }
}

^Esc::
	ExitApp
