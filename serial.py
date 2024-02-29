import wmi

# WMI 인스턴스 생성
c = wmi.WMI()


# Win32_USBControllerDevice를 사용하여 USB 컨트롤러와 연결된 장치를 조회
for usb in c.Win32_USBControllerDevice():
    device_id = usb.Dependent.DeviceID
    print(c.Win32_PnPEntity(DeviceID=device_id))
    # Win32_PnPEntity를 사용하여 USB 장치의 상세 정보 조회
    for pnp in c.Win32_PnPEntity(DeviceID=device_id):
        print(f"Device: {pnp.Description}")
        print(f"Class GUID: {pnp.ClassGuid}")
        print(f"Manufacturer: {pnp.Manufacturer}")
        print(f"Service: {pnp.Service}")
        print("-----")