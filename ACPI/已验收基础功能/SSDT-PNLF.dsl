DefinitionBlock ("", "SSDT", 2, "ARL", "PNLF", 0x00000000)
{
    External (_SB_.PC00, DeviceObj)

    Scope (_SB_.PC00)
    {
        Device (PNLF)
        {
            Name (_HID, EisaId ("APP0002"))  // _HID: Hardware ID
            Name (_CID, "backlight")         // _CID: Compatible ID
            Name (_UID, 0x0A)                // _UID: Unique ID
            Name (_STA, 0x0B)                // _STA: Status
        }
    }
}
