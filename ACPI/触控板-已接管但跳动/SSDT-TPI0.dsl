// GXTP5100 on physical 00:15.0; original firmware TPID address=0x2c, HID descriptor=0x20.
// New local name I2CX avoids redefining the firmware's conditional I2C0.
DefinitionBlock ("", "SSDT", 2, "GY", "TPI0", 1)
{
    External (\_SB.PC00, DeviceObj)
    Scope (\_SB.PC00)
    {
        Device (I2CX)
        {
            Name (_ADR, 0x00150000)
            Method (_STA, 0, NotSerialized)
            {
                If (_OSI ("Darwin")) { Return (0x0F) }
                Return (Zero)
            }
            Device (TPAD)
            {
                Name (_HID, "GXTP5100")
                Name (_CID, "PNP0C50")
                Name (_UID, One)
                Name (_STA, 0x0F)
                Name (_S0W, 0x03)
                Name (_CRS, ResourceTemplate ()
                {
                    I2cSerialBusV2 (0x002C, ControllerInitiated, 400000,
                        AddressingMode7Bit, "\\_SB.PC00.I2CX", 0,
                        ResourceConsumer, , Exclusive)
                })
                Method (XDSM, 4, Serialized)
                {
                    If (Arg0 == ToUUID ("3cdff6f7-4267-4555-ad05-b30a3d8938de"))
                    {
                        If (Arg2 == Zero) { Return (Buffer () { 0x03 }) }
                        If (Arg2 == One) { Return (0x20) }
                    }
                    Return (Buffer () { 0x00 })
                }
            }
        }
    }
}
