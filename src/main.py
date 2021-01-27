import ctypes
import ctypes.wintypes
import traceback
import atexit



WM_KEYDOWN=0x0100
WM_SYSKEYDOWN=0x0104
WH_KEYBOARD_LL=13
VK_PACKET=0xe7
LLKHF_INJECTED=0x10
LLKHF_ALTDOWN=0x20
PM_REMOVE=1



ctypes.wintypes.ULONG_PTR=ctypes.POINTER(ctypes.wintypes.DWORD)
ctypes.wintypes.LRESULT=ctypes.c_int
ctypes.wintypes.LowLevelKeyboardProc=ctypes.WINFUNCTYPE(ctypes.c_int,ctypes.c_int,ctypes.wintypes.WPARAM,ctypes.wintypes.LPARAM)
ctypes.wintypes.KBDLLHOOKSTRUCT=type("KBDLLHOOKSTRUCT",(ctypes.Structure,),{"_fields_":[("vk_code",ctypes.wintypes.DWORD),("scan_code",ctypes.wintypes.DWORD),("flags",ctypes.wintypes.DWORD),("time",ctypes.c_int),("dwExtraInfo",ctypes.wintypes.ULONG_PTR)]})
ctypes.windll.kernel32.GetModuleHandleW.argtypes=(ctypes.wintypes.LPCWSTR,)
ctypes.windll.kernel32.GetModuleHandleW.restype=ctypes.wintypes.HMODULE
ctypes.windll.user32.CallNextHookEx.argtypes=(ctypes.POINTER(ctypes.wintypes.HHOOK),ctypes.c_int,ctypes.wintypes.WPARAM,ctypes.wintypes.LPARAM)
ctypes.windll.user32.CallNextHookEx.restype=ctypes.wintypes.LRESULT
ctypes.windll.user32.DispatchMessageW.argtypes=(ctypes.wintypes.LPMSG,)
ctypes.windll.user32.DispatchMessageW.restype=ctypes.wintypes.LRESULT
ctypes.windll.user32.PeekMessageW.argtypes=(ctypes.wintypes.LPMSG,ctypes.wintypes.HWND,ctypes.c_uint,ctypes.c_uint,ctypes.c_uint)
ctypes.windll.user32.PeekMessageW.restype=ctypes.wintypes.BOOL
ctypes.windll.user32.SetWindowsHookExW.argtypes=(ctypes.c_int,ctypes.wintypes.LowLevelKeyboardProc,ctypes.wintypes.HINSTANCE,ctypes.wintypes.DWORD)
ctypes.windll.user32.SetWindowsHookExW.restype=ctypes.wintypes.HHOOK
ctypes.windll.user32.TranslateMessage.argtypes=(ctypes.wintypes.LPMSG,)
ctypes.windll.user32.TranslateMessage.restype=ctypes.wintypes.BOOL
ctypes.windll.user32.UnhookWindowsHookEx.argtypes=(ctypes.wintypes.HHOOK,)
ctypes.windll.user32.UnhookWindowsHookEx.restype=ctypes.wintypes.BOOL



KEY_DOWN=1
KEY_UP=0
VK_KEYS={0x03:"Cancel",0x08:"Backspace",0x09:"Tab",0x0c:"Clear",0x0d:"Enter",0x10:"Shift",0x11:"Ctrl",0x12:"Alt",0x13:"Pause",0x14:"CapsLock",0x1b:"Esc",0x20:"Spacebar",0x21:"PageUp",0x22:"PageDown",0x23:"End",0x24:"Home",0x25:"Left",0x26:"Up",0x27:"Right",0x28:"Down",0x29:"Select",0x2a:"Print",0x2b:"Execute",0x2c:"PrintScreen",0x2d:"Insert",0x2e:"Delete",0x2f:"Help",0x30:"0",0x31:"1",0x32:"2",0x33:"3",0x34:"4",0x35:"5",0x36:"6",0x37:"7",0x38:"8",0x39:"9",0x41:"A",0x42:"B",0x43:"C",0x44:"D",0x45:"E",0x46:"F",0x47:"G",0x48:"H",0x49:"I",0x4a:"J",0x4b:"K",0x4c:"L",0x4d:"M",0x4e:"N",0x4f:"O",0x50:"P",0x51:"Q",0x52:"R",0x53:"S",0x54:"T",0x55:"U",0x56:"V",0x57:"W",0x58:"X",0x59:"Y",0x5a:"Z",0x5b:"LeftWindows",0x5c:"RightWindows",0x5d:"Apps",0x5f:"Sleep",0x60:"0",0x61:"1",0x62:"2",0x63:"3",0x64:"4",0x65:"5",0x66:"6",0x67:"7",0x68:"8",0x69:"9",0x6a:"*",0x6b:"+",0x6c:"Separator",0x6d:"-",0x6e:"Decimal",0x6f:"/",0x70:"F1",0x71:"F2",0x72:"F3",0x73:"F4",0x74:"F5",0x75:"F6",0x76:"F7",0x77:"F8",0x78:"F9",0x79:"F10",0x7a:"F11",0x7b:"F12",0x7c:"F13",0x7d:"F14",0x7e:"F15",0x7f:"F16",0x80:"F17",0x81:"F18",0x82:"F19",0x83:"F20",0x84:"F21",0x85:"F22",0x86:"F23",0x87:"F24",0x90:"NumLock",0x91:"ScrollLock",0xa0:"LeftShift",0xa1:"RightShift",0xa2:"LeftCtrl",0xa3:"RightCtrl",0xa4:"LeftMenu",0xa5:"RightMenu",0xad:"VolumeMute",0xae:"VolumeDown",0xaf:"VolumeUp",0xba:";",0xbb:"+",0xbc:",",0xbd:"-",0xbe:".",0xbf:"/",0xc0:"`",0xdb:"[",0xdc:"\\",0xdd:"]",0xde:"'"}
NUMPAD_VK=(0x60,0x61,0x62,0x63,0x64,0x65,0x66,0x67,0x68,0x69,0x6a,0x6b,0x6c,0x6d,0x6e,0x6f)



def register_hook(cb):
	def _handle(c,wp,lp):
		try:
			dt=ctypes.cast(lp,ctypes.POINTER(ctypes.wintypes.KBDLLHOOKSTRUCT)).contents
			if (dt.vk_code!=VK_PACKET and dt.flags&(LLKHF_INJECTED|LLKHF_ALTDOWN)!=LLKHF_INJECTED|LLKHF_ALTDOWN):
				if (dt.vk_code==0xa5 and _handle._ig_alt==True):
					_handle._ig_alt=False
				else:
					if (dt.scan_code==0x21d and dt.vk_code==0xa2):
						_handle._ig_alt=True
					if (not cb((VK_KEYS[dt.vk_code] if dt.vk_code in VK_KEYS else None),dt.vk_code,(True if dt.vk_code in NUMPAD_VK else False),(KEY_DOWN if wp in (WM_KEYDOWN,WM_SYSKEYDOWN) else KEY_UP))):
						return -1
		except Exception as e:
			traceback.print_exception(None,e,e.__traceback__)
		return ctypes.windll.user32.CallNextHookEx(None,c,wp,lp)
	_handle._ig_alt=False
	kb_cb=ctypes.wintypes.LowLevelKeyboardProc(_handle)
	ctypes.windll.user32.SetWindowsHookExW(WH_KEYBOARD_LL,kb_cb,ctypes.windll.kernel32.GetModuleHandleW(None),ctypes.wintypes.DWORD(0))
	atexit.register(ctypes.windll.user32.UnhookWindowsHookEx,kb_cb)



register_hook(lambda k,vk,np,st:(print(k,vk,np,st),True)[1])
msg=ctypes.wintypes.LPMSG()
while (True):
	if (ctypes.windll.user32.PeekMessageW(msg,None,0,0,PM_REMOVE)!=0):
		ctypes.windll.user32.TranslateMessage(msg)
		ctypes.windll.user32.DispatchMessageW(msg)
