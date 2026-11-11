DefinitionBlock ("", "SSDT", 2, "LOCAL", "HDA0", 0x00000001)
{
    External (\_SB.PC00, DeviceObj)
    External (\_SB.PC00.HDAS, DeviceObj)

    Scope (\_SB.PC00)
    {
        Device (HDA0)
        {
            Name (_ADR, 0x001F0003)
            Method (_STA, 0, NotSerialized)
            {
                If (_OSI ("Darwin"))
                {
                    If (CondRefOf (\_SB.PC00.HDAS))
                    {
                        Return (Zero)
                    }
                    Return (0x0F)
                }
                Return (Zero)
            }

            Method (_DSM, 4, NotSerialized)
            {
                If (!Arg2)
                {
                    Return (Buffer () { 0x03 })
                }
                Return (Package ()
                {
                    "device-id", Buffer () { 0xD0, 0x7A, 0x00, 0x00 },
                    "layout-id", Buffer () { 0x64, 0x00, 0x00, 0x00 },
                    "alc-layout-id", Buffer () { 0x64, 0x00, 0x00, 0x00 },
                    "built-in", Buffer () { 0x00 }
                })
            }
        }
    }
}
