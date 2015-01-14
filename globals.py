import array
import SOC_const_sam7pxxx

#even though really CPU related, used in arm7instrdecode, to prevent circular refs define here
SP   = 13 #SP = r13
LINK = 14 #Link = r14
PC   = 15 #pr = r15

# next 4 actually overlap the FIQ register array but
#  FIQ shares R0-R7 w/ sys & user
CPSR = 16 #32: NZCVQ    7:IF 5:T (thumb) 4-0: mode
SPSR = 17
D_CPSR = 18
LAST_REG = 19

# Boundary Scan Register - JTAG - 96 bits
BSR_0 = 0 # 0-31
BSR_1 = 0 # 32-63
BSR_2 = 0 # 64-95
BSR_3 = 0 # 96

###########################################################################
# NOTES:  BASE is defined in the SOC files
#         Main registers are defined by BASE + offset
#              also describe read/write, only and 1 (once)
#                   RESET are values that happen on reset
#         bits and values are defined by the mask - what positions are used
#              comments are for "set" unless stated otherwise
###########################################################################

#--------------------------------------------------------------------------
# Reset Controller
RSTC_CR = SOC_const_sam7pxxx.RSTC_BASE # control reg - wo - RESET:-
RSTC_SR = SOC_const_sam7pxxx.RSTC_BASE + 4 # status reg - ro - RESET:0x0000_0000
RSTC_MR = SOC_const_sam7pxxx.RSTC_BASE + 8 # mode reg - r/w - RESET:0x0000_0000

RSTC_CR_KEY = 0xFF000000  # Write 0xA5, any other aborts write
RSTC_CR_EXTRST = 0x8  # if KEY correct & set, assert NRST pin
RSTC_CR_PERRST = 0x4  # if KEY correct & set, resets peripherals
RSTC_CR_PROCRST = 0x1 # if KEY correct & set, resets processor

RSTC_SR_SRCMP = 0x20000 # set, software reset, controller busy
RSTC_SR_NRSTL = 0x10000 # NRST pin level at master clock
RSTC_SR_RSTTYP = 0x700  # reset type
RSTTYP_PWR = 0 # power reset
RSTTYP_WD = 2  # watchdog
RSTTYP_SWF = 3 # software
RSTTYP_USR = 4 # user
RSTTYP_BRN = 5 # brownout

RSTC_SR_BODSTS = 0x2   # high to low brownout detect since last read
RSTC_SR_URSTS  = 0x1   # high-to-low detect on NRST since last read

RSTC_MR_KEY = 0xFF000000 # write 0xA5
RSTC_MR_BODIEN = 0x10000 # BODSTS bit, RSTC_SR = 1, asserts rstc_irq
RSTC_MR_ERSTL  = 0xF00   # external reset length, 60us - 2s
RSTC_MR_URSTIEN = 0x10   # USRTS bit, RSTC_SR = 1, asserts rstc_irq if URSTEN = 0
RSTC_MR_URSTEN = 0x1     # go low, on NRST pin, user reset enable

#--------------------------------------------------------------------------
# Real-time Timer RTT
RTT_MR = SOC_const_sam7pxxx.RTT_BASE # mode register, r/w - RESET:0x0000 8000
RTT_AR = SOC_const_sam7pxxx.RTT_BASE + 4 # alarm register, r/w - RESET:FFFF FFFF
RTT_VR = SOC_const_sam7pxxx.RTT_BASE + 8 # value register, ro - RESET:0x0000 8000
RTT_SR = SOC_const_sam7pxxx.RTT_BASE + 0xC # status register, ro - RESET:0x0000 8000

RTT_MR_RTTRST    = 0x40000 # reloads and resets clock divider, resets 32-b counter
RTT_MR_RTTINCIEN = 0x20000 # set, bit RTTINC in RTT_SR asserts interrupt.
RTT_MR_ALMIEN    = 0x10000 # set, bit ALMS in RTT_SR asserts interrupt
RTT_MR_RTPRES = 0xFFFF #0, pre-scaler period = 2^16, else period = value

RTT_AR_ALMV = 0xFFFFFFFF # Defines the alarm value (ALMV+1) compared with the Real-time Timer.
RTT_VR_CRTV = 0xFFFFFFFF # Returns the current value of the Real-time Timer.
RTT_SR_RTTINC = 0x2 # The Real-time Timer has been incremented since the last read of the RTT_SR
RTT_SR_ALMS = 0x1 # The Real-time Alarm occurred since the last read of RTT_SR.

#--------------------------------------------------------------------------
# Periodic Interval Timer
PIT_MR = SOC_const_sam7pxxx.PIT_BASE # Mode reg - r/w - RESET:0x000F FFFF
PIT_SR = SOC_const_sam7pxxx.PIT_BASE + 4 # Status reg - ro - RESET:0x0000 0000
PIT_PIVR = SOC_const_sam7pxxx.PIT_BASE + 8 # Periodic Interval Value Register - ro - RESET:0x0000 0000
PIT_PIIR = SOC_const_sam7pxxx.PIT_BASE + 12 # Periodic Interval Image Register - ro - RESET:0x0000 0000

PIT_MR_PITIEN = 0x2000000 # The bit PITS in PIT_SR asserts interrupt.
PIT_MR_PITEN  = 0x1000000 # The Periodic Interval Timer is enabled.
PIT_SR_PITS = 1 # The Periodic Interval timer has reached PIV since the last read of PIT_PIVR

PIT_PIVR_PICNT = 0xFFF00000 # Returns the number of occurrences of periodic intervals since the last read of PIT_PIVR.
PIT_PIVR_CPIV  = 0x000FFFFF # Returns the current value of the periodic interval timer.

PIT_PIIR_PICNT = 0xFFF00000 # Returns the number of occurrences of periodic intervals since the last read of PIT_PIVR.
PIT_PIIR_CPIV  = 0x000FFFFF # Returns the current value of the periodic interval timer.

#--------------------------------------------------------------------------
# Watchdog Timer
WDT_MR = SOC_const_sam7pxxx.WDT_BASE # Mode reg - wo - RESET:
WDT_SR = SOC_const_sam7pxxx.WDT_BASE + 4 # Status reg - rw1 - RESET:0x3FFF 2FFF
WDT_PIVR = SOC_const_sam7pxxx.WDT_BASE + 8 # Periodic Interval Value Register - ro - RESET:0x0000 0000

WDT_CR_KEY = 0xFF000000 # 0xA5
WDT_CR_WDRSTT = 1 # Restarts the Watchdog.
WDT_MR_WDIDLEHLT = 0x20000000 # The Watchdog runs(0)/stops(1) when the system is in idle state
WDT_MR_WDDBGHLT  = 0x10000000 # The Watchdog runs(0)/stops(1) when the processor is in debug state
WDT_MR_WDD       = 0xFFF0000  # If the Watchdog Timer value is <= WDD, w WDRSTT 1, restarts timer
                              #                                >  WDD, w WDRSTT 1, watchdog err
WDT_MR_WDDIS   = 0x8000 # Disables the Watchdog Timer.
WDT_MR_WDRPROC = 0x4000 # fault will activate all(0)/
WDT_MR_WDRSTEN = 0x2000 # A Watchdog fault (underflow or error) triggers a Watchdog reset.
WDT_MR_WDFIEN  = 0x1000 # A Watchdog fault (underflow or error) asserts interrupt.
WDT_MR_WDV     = 0xFFF  # Defines the value loaded in the 12-bit Watchdog Counter.

WDT_SR_WDERR = 0x2 # At least one Watchdog error occurred since the last read of WDT_SR.
WDT_SR_WDUNF = 0x1 # At least one Watchdog underflow occurred since the last read of WDT_SR.

#--------------------------------------------------------------------------
# Voltage Regulator Mode Controller
VREG_MR = SOC_const_sam7pxxx.VREG_BASE + 0x60 # rw RESET:0
VREG_MR_PSTDBY = 1 # Voltage regulator in standby mode (low-power mode).

#--------------------------------------------------------------------------
# Memory Controller
MC_RCR = SOC_const_sam7pxxx.MC_BASE # Remap control register, wo, RESET: -
MC_ASR = SOC_const_sam7pxxx.MC_BASE + 4 # Abort status register, ro, RESET: 0
MC_AASR = SOC_const_sam7pxxx.MC_BASE + 8 # Abort Address status register, ro, RESET: 0
MC_EFC0 = SOC_const_sam7pxxx.MC_BASE + 0x60 #
MC_EFC1 = SOC_const_sam7pxxx.MC_BASE + 0x70 # SAM7S512 only

MC_RCR_RCB = 1 # This Command Bit acts on a toggle basis: writing a 1 alternatively cancels and restores the remapping of the page zero
               # memory devices.
MC_ASR_SVMST1 = 0x2000000 # At least one (1)/ none (0) abort due to the ARM7TDMI occurred.
MC_ASR_SVMST0 = 0x1000000 # At least one (1)/ none (0) abort due to the PDC occurred.
MC_ASR_MST1   = 0x20000 # The last aborted access was(1) / was not(0) due to the ARM7TDMI.
MC_ASR_MST0   = 0x10000 # The last aborted access was(1) / was not(0) due to the PDC.
MC_ASR_ABTTYP = 0xC00 # 0-data r, 1-data w, 2-code fetch, 3-fetch
MC_ASR_ABTSZ  = 0x300 # 0-B, 1-1/2w, 2-w, 3-reserved
MC_ASR_MISADD = 0x2 # The last aborted access was (1) / was not(0) due to an address misalignment.
MC_ASR_UNDADD = 0x1 # The last abort was (1) / was not(0) due to the access of an undefined address in the address space.

MC_AASR_ABTADD = 0xFFFFFFFF # This field contains the address of the last aborted access.

#--------------------------------------------------------------------------
# Embedded Flash Crontroller - See notes
MC_FMR0 = SOC_const_sam7pxxx.MC_BASE + 0x60 # MC Flash Mode Register  Read-write 0x0
MC_FCR0 = SOC_const_sam7pxxx.MC_BASE + 0x64 # MC Flash Command Register  Write-only
MC_FSR0 = SOC_const_sam7pxxx.MC_BASE + 0x68 # MC Flash Status Register  Read-only
# = SOC_const_sam7pxxx.MC_BASE + 0x6C Reserved

# (EFC1) Register Mapping Offset Register
MC_FMR1 = SOC_const_sam7pxxx.MC_BASE + 0x70 # MC Flash Mode Register  Read-write 0x0
MC_FCR1 = SOC_const_sam7pxxx.MC_BASE + 0x74 # MC Flash Command Register  Write-only
MC_FSR1 = SOC_const_sam7pxxx.MC_BASE + 0x78 # MC Flash Status Register  Read-only
# = SOC_const_sam7pxxx.MC_BASE + 0x7C Reserved

# NOTE: DEFS Skipped - TODO

#--------------------------------------------------------------------------
# Fast Flash Programming interface
# Wire commands - no software

#--------------------------------------------------------------------------
# Serial Fast Flash Programming

#--------------------------------------------------------------------------
# Peripheral DMA Controller (PDC) User Interface

#--------------------------------------------------------------------------
# Advanced Interrupt Controller (AIC)
AIC_SMR0 = SOC_const_sam7pxxx.AIC_BASE + 0x00 # Source Mode Register 0  Read/Write 0x0
AIC_SMR1 = SOC_const_sam7pxxx.AIC_BASE + 0x04 # Source Mode Register 1  Read/Write 0x0
AIC_SMR31 = SOC_const_sam7pxxx.AIC_BASE + 0x7C # Source Mode Register 31  Read/Write 0x0
AIC_SVR0 = SOC_const_sam7pxxx.AIC_BASE + 0x80 # # Source Vector Register 0  Read/Write 0x0
AIC_SVR1 = SOC_const_sam7pxxx.AIC_BASE + 0x84 # Source Vector Register 1  Read/Write 0x0
AIC_IVR = SOC_const_sam7pxxx.AIC_BASE + 0xFC # Source Vector Register 31 0x100 Interrupt Vector Register  Read-only 0x0
AIC_FVR = SOC_const_sam7pxxx.AIC_BASE + 0x104 # FIQ Interrupt Vector Register  Read-only 0x0
AIC_ISR = SOC_const_sam7pxxx.AIC_BASE + 0x108 # Interrupt Status Register  Read-only 0x0
AIC_IPR = SOC_const_sam7pxxx.AIC_BASE + 0x10C # Interrupt Pending Register 0x110 Interrupt Mask Register (2) AIC_IMR Read-only 0x0
AIC_CISR = SOC_const_sam7pxxx.AIC_BASE + 0x114 # Core Interrupt Status Register  Read-only 0x0
AIC_IECR = SOC_const_sam7pxxx.AIC_BASE + 0x120 # Interrupt Enable Command Register
AIC_IDCR = SOC_const_sam7pxxx.AIC_BASE + 0x124 # Interrupt Disable Command Register (2)
AIC_ICCR = SOC_const_sam7pxxx.AIC_BASE + 0x128 # Interrupt Clear Command Register  Write-only ---
AIC_ISCR = SOC_const_sam7pxxx.AIC_BASE + 0x12C # Interrupt Set Command Register (2)  Write-only ---
AIC_EOICR = SOC_const_sam7pxxx.AIC_BASE + 0x130 # End of Interrupt Command Register  Write-only ---
AIC_SPU = SOC_const_sam7pxxx.AIC_BASE + 0x134 # Spurious Interrupt Vector Register  Read/Write 0x0
AIC_DCR = SOC_const_sam7pxxx.AIC_BASE + 0x138 # Debug Control Register  Read/Write 0x0
AIC_FFER = SOC_const_sam7pxxx.AIC_BASE + 0x140 # Fast Forcing Enable Register
AIC_FFDR = SOC_const_sam7pxxx.AIC_BASE + 0x144 # Fast Forcing Disable Register (2)
AIC_FFSR = SOC_const_sam7pxxx.AIC_BASE + 0x148 # Fast Forcing Status Register (2)

#--------------------------------------------------------------------------
# Power Management Controller (PMC) User Interface
PMC_SCER  = SOC_const_sam7pxxx.PMC_BASE + 0x00 # System Clock Enable Register wo
PMC_SCDR  = SOC_const_sam7pxxx.PMC_BASE + 0x04 # System Clock Disable Register wo
PMC_SCSR  = SOC_const_sam7pxxx.PMC_BASE + 0x08 # System Clock Status Register
PMC_PCER  = SOC_const_sam7pxxx.PMC_BASE + 0x10 # Peripheral Clock Enable Register  Write-only 
PMC_PCDR  = SOC_const_sam7pxxx.PMC_BASE + 0x14 # Peripheral Clock Disable Register  Write-only
PMC_PCSR  = SOC_const_sam7pxxx.PMC_BASE + 0x18 # Peripheral Clock Status Register  Read-only 0x0
CKGR_MOR  = SOC_const_sam7pxxx.PMC_BASE + 0x20 # Main Oscillator Register  Read-write 0x0
CKGR_MCFR = SOC_const_sam7pxxx.PMC_BASE + 0x24 # Main Clock Frequency Register  Read-only 0x0
CKGR_PLLR = SOC_const_sam7pxxx.PMC_BASE + 0x2C # PLL Register  (2) Read-write 0x3F00
PMC_MCKR  = SOC_const_sam7pxxx.PMC_BASE + 0x30 # Master Clock Register  Read-write 0x0
PMC_PCK0  = SOC_const_sam7pxxx.PMC_BASE + 0x40 # Programmable Clock 0 Register  Read-write 0x0
PMC_PCK1  = SOC_const_sam7pxxx.PMC_BASE + 0x44 # Programmable Clock 1 Register  Read-write 0x0
PMC_PCK2  = SOC_const_sam7pxxx.PMC_BASE + 0x48 # Programmable Clock 2 Register  Read-write 0x0
PMC_IER   = SOC_const_sam7pxxx.PMC_BASE + 0x60 # Interrupt Enable Register  Write-only --
PMC_IDR   = SOC_const_sam7pxxx.PMC_BASE + 0x64 # Interrupt Disable Register  Write-only --
PMC_SR    = SOC_const_sam7pxxx.PMC_BASE + 0x68 # Status Register  Read-only 0x08
PMC_IMR   = SOC_const_sam7pxxx.PMC_BASE + 0x6C # Interrupt Mask Register  Read-only 0x0

PMC_SCER_PCK2 = 0x4 # Enables the corresponding Programmable Clock output.
PMC_SCER_PCK1 = 0x2 # Enables the corresponding Programmable Clock output.
PMC_SCER_PCK0 = 0x1 # Enables the corresponding Programmable Clock output.
PMC_SCER_UDP = 0x80 # Enables the 48 MHz clock of the USB Device Port.
PMC_SCER_PCK = 0x1  # Enables the Processor clock.

PMC_SCDR_PCK2 = 0x4 # Enables the corresponding Programmable Clock output.
PMC_SCDR_PCK1 = 0x2 # Enables the corresponding Programmable Clock output.
PMC_SCDR_PCK0 = 0x1 # Enables the corresponding Programmable Clock output.
PMC_SCDR_UDP = 0x80 # Enables the 48 MHz clock of the USB Device Port.
PMC_SCDR_PCK = 0x1  # Enables the Processor clock.

PMC_SCSR_PCK2 = 0x4 # Enables the corresponding Programmable Clock output.
PMC_SCSR_PCK1 = 0x2 # Enables the corresponding Programmable Clock output.
PMC_SCSR_PCK0 = 0x1 # Enables the corresponding Programmable Clock output.
PMC_SCSR_UDP = 0x80 # Enables the 48 MHz clock of the USB Device Port.
PMC_SCSR_PCK = 0x1  # Enables the Processor clock.

#--------------------------------------------------------------------------
# Debug Unit (DBGU) User Interface

DBGU_CR   = SOC_const_sam7pxxx.DBGU_BASE # Control Register  Write-only 
DBGU_MR   = SOC_const_sam7pxxx.DBGU_BASE + 0x0004 # Mode Register  Read-write 0x0
DBGU_IER  = SOC_const_sam7pxxx.DBGU_BASE + 0x0008 # Interrupt Enable Register  Write-only 
DBGU_IDR  = SOC_const_sam7pxxx.DBGU_BASE + 0x000C # Interrupt Disable Register  Write-only 
DBGU_IMR  = SOC_const_sam7pxxx.DBGU_BASE + 0x0010 # Interrupt Mask Register  Read-only 0x0
DBGU_SR   = SOC_const_sam7pxxx.DBGU_BASE + 0x0014 # Status Register  Read-only 
DBGU_RHR  = SOC_const_sam7pxxx.DBGU_BASE + 0x0018 # Receive Holding Register  Read-only 0x0
DBGU_THR  = SOC_const_sam7pxxx.DBGU_BASE + 0x001C # Transmit Holding Register  Write-only 
DBGU_BRGR = SOC_const_sam7pxxx.DBGU_BASE + 0x0020 # Baud Rate Generator Register  Read-write 0x0
# 0x0024 - 0x003C Reserved
DBGU_CIDR = SOC_const_sam7pxxx.DBGU_BASE + 0x0040 # Chip ID Register  Read-only 
DBGU_EXID = SOC_const_sam7pxxx.DBGU_BASE + 0x0044 # Chip ID Extension Register  Read-only 
DBGU_FNR  = SOC_const_sam7pxxx.DBGU_BASE + 0x0048 # Force NTRST Register  Read-write 0x0
# 0x004C - 0x00FC Reserved
DBGU_PDC  = SOC_const_sam7pxxx.DBGU_BASE + 0x0100 # - 0x0124  PDC Area

DBGU_CR_RSTSTA = 0x100 # Resets the status bits PARE, FRAME and OVRE in the DBGU_SR.
DBGU_CR_TXDIS = 0x80  # The transmitter is disabled. If a character is being processed and a character has been written the DBGU_THR and
                      # RSTTX is not set, both characters are completed before the transmitter is stopped.
DBGU_CR_TXEN = 0x40   # The transmitter is enabled if TXDIS is 0.
DBGU_CR_RXDIS = 0x20  # The receiver is disabled. If a character is being processed and RSTRX is not set, the character is completed before the receiver is stopped.
DBGU_CR_RXEN = 0x10   # The receiver is enabled if RXDIS is 0.
DBGU_CR_RSTTX = 0x8   # The transmitter logic is reset and disabled. If a character is being transmitted, the transmission is aborted.
DBGU_CR_RSTRX = 0x4   # The receiver logic is reset and disabled. If a character is being received, the reception is aborted.

DBGU_MR_CHMODE = 0xC000
DBGU_MR_PAR = 0xE00
#PAR: Parity Type PAR Parity Type
# 0 0 0 Even parity
# 0 0 1 Odd parity
# 0 1 0 Space: parity forced to 0
# 0 1 1 Mark: parity forced to 1
# 1 x x No parity
#CHMODE: Channel Mode CHMODE Mode Description
# 0 0 Normal Mode
# 0 1 Automatic Echo
# 1 0 Local Loopback
# 1 1 Remote Loopback

DBGU_IER_COMMRX  = 0x80000000 # COMMRX: Enable COMMRX (from ARM) Interrupt
DBGU_IER_COMMTX  = 0x40000000 # COMMTX: Enable COMMTX (from ARM) Interrupt
DBGU_IER_RXBUFF  = 0x1000 # RXBUFF: Enable Buffer Full Interrupt
DBGU_IER_TXBUFE  = 0x800 # TXBUFE: Enable Buffer Empty Interrupt
DBGU_IER_TXEMPTY = 0x200 # TXEMPTY: Enable TXEMPTY Interrupt
DBGU_IER_PARE    = 0x80 # PARE: Enable Parity Error Interrupt
DBGU_IER_FRAME   = 0x40 # FRAME: Enable Framing Error Interrupt
DBGU_IER_OVRE    = 0x20 # OVRE: Enable Overrun Error Interrupt
DBGU_IER_ENDTX   = 0x10 # ENDTX: Enable End of Transmit Interrupt
DBGU_IER_ENDRX   = 0x8 # ENDRX: Enable End of Receive Transfer Interrupt
DBGU_IER_TXRDY   = 0x2 # TXRDY: Enable TXRDY Interrupt
DBGU_IER_RXRDY   = 0x1 # RXRDY: Enable RXRDY Interrupt

DBGU_IDR_COMMRX  = 0x80000000 # COMMRX: disable COMMRX (from ARM) Interrupt
DBGU_IDR_COMMTX  = 0x40000000 # COMMTX: disable COMMTX (from ARM) Interrupt
DBGU_IDR_RXBUFF  = 0x1000 # RXBUFF: disable Buffer Full Interrupt
DBGU_IDR_TXBUFE  = 0x800 # TXBUFE: disable Buffer Empty Interrupt
DBGU_IDR_TXEMPTY = 0x200 # TXEMPTY: disable TXEMPTY Interrupt
DBGU_IDR_PARE    = 0x80 # PARE: disable Parity Error Interrupt
DBGU_IDR_FRAME   = 0x40 # FRAME: disable Framing Error Interrupt
DBGU_IDR_OVRE    = 0x20 # OVRE: disable Overrun Error Interrupt
DBGU_IDR_ENDTX   = 0x10 # ENDTX: disable End of Transmit Interrupt
DBGU_IDR_ENDRX   = 0x8 # ENDRX: disable End of Receive Transfer Interrupt
DBGU_IDR_TXRDY   = 0x2 # TXRDY: disable TXRDY Interrupt
DBGU_IDR_RXRDY   = 0x1 # RXRDY: disable RXRDY Interrupt

DBGU_IMR_COMMRX  = 0x80000000 # COMMRX: Mask COMMRX Interrupt
DBGU_IMR_COMMTX  = 0x40000000 # COMMTX: Mask COMMTX Interrupt
DBGU_IMR_RXBUFF  = 0x1000 # RXBUFF: Mask RXBUFF Interrupt
DBGU_IMR_TXBUFE  = 0x800 # TXBUFE: Mask TXBUFE Interrupt
DBGU_IMR_TXEMPTY = 0x200 # TXEMPTY: Mask TXEMPTY Interrupt
DBGU_IMR_PARE    = 0x80 # PARE: Mask Parity Error Interrupt
DBGU_IMR_FRAME   = 0x40 # FRAME: Mask Framing Error Interrupt
DBGU_IMR_OVRE    = 0x20 # OVRE: Mask Overrun Error Interrupt
DBGU_IMR_ENDTX   = 0x10 # ENDTX: Mask End of Transmit Interrupt
DBGU_IMR_ENDRX   = 0x8 # ENDRX: Mask End of Receive Transfer Interrupt
DBGU_IMR_TXRDY   = 0x2 # TXRDY: Disable TXRDY Interrupt
DBGU_IMR_RXRDY   = 0x1 # RXRDY: Mask RXRDY Interrupt

DBGU_SR_COMMRX  = 0x80000000 # COMMRX: 
DBGU_SR_COMMTX  = 0x40000000 # COMMTX: 
DBGU_SR_RXBUFF  = 0x1000 # RXBUFF:
DBGU_SR_TXBUFE  = 0x800 # TXBUFE: 
DBGU_SR_TXEMPTY = 0x200 # TXEMPTY:
DBGU_SR_PARE    = 0x80 # PARE: 
DBGU_SR_FRAME   = 0x40 # FRAME: 
DBGU_SR_OVRE    = 0x20 # OVRE: 
DBGU_SR_ENDTX   = 0x10 # ENDTX: 
DBGU_SR_ENDRX   = 0x8 # ENDRX: 
DBGU_SR_TXRDY   = 0x2 # TXRDY: 
DBGU_SR_RXRDY   = 0x1 # RXRDY:

DBGU_RHR_RXCHR = 0xFF # Last received character if RXRDY is set.
DBGU_THR_TXCHR = 0xFF # Next character to be transmitted after the current character if TXRDY is not set.

DBGU_BRGR_CD = 0xFFFF # 0 dis, 1 MCK, 2-65535 MCK/(CDx16)

DBGU_CIDR_EXT = 0x80000000 # 
DBGU_CIDR_NVPTYP = 0x70000000 # 0-ROM, 1-ROMless or flash, 4-SRAM emu ROM, 2-embed flash, 3 ROM&flash NVPSIZ is ROM, NVPSIZ2 is flash
DBGU_CIDR_ARCH = 0xFF00000 # See SAM7 datasheet
DBGU_CIDR_SRAMSIZ = 0xF0000 # 1-1k, 2-2k, 3-6k, 4-112k, 5-4k, 6-80k, 7-160k, 8-8k, 9-16k, A-32k, B-64k, C-128k, D-256k, E-96k, F-512k
DBGU_CIDR_NVPSIZ2 = 0xF000 # 0-0, 1-8k, 2-16k, 3-32k, 5-64k, 7-128k, 9-256k, A-512k, C-1024k, E-2048k
DBGU_CIDR_NVPSIZ  = 0xF00 # 0-0, 1-8k, 2-16k, 3-32k, 5-64k, 7-128k, 9-256k, A-512k, C-1024k, E-2048k
DBGU_CIDR_EPROC   = 0xE0 # b010 = ARM7TDMI, others ARM9
DBGU_CIDR_VERSION = 0x1F # Version

DBGU_EXID_EXID = 0xFFFFFFFF

DBGU_FNR_FNTRST = 0x1 # 

#--------------------------------------------------------------------------
# Programmable Multibit ECC Error Location (PIO) User Interface

PIO_PER = SOC_const_sam7pxxx.PIO_BASE # 0x0000 PIO Enable Register PIO_PER Write-only 
PIO_PDR = SOC_const_sam7pxxx.PIO_BASE + 0x0004 # PIO Disable Register PIO_PDR Write-only 
PIO_PSR = SOC_const_sam7pxxx.PIO_BASE + 0x0008 # PIO Status Register
PIO_OER = SOC_const_sam7pxxx.PIO_BASE + 0x0010 # Output Enable Register PIO_OER Write-only 
PIO_ODR = SOC_const_sam7pxxx.PIO_BASE + 0x0014 # Output Disable Register PIO_ODR Write-only 
PIO_OSR = SOC_const_sam7pxxx.PIO_BASE + 0x0018 # Output Status Register PIO_OSR Read-only 0x0000 0000
PIO_IFER = SOC_const_sam7pxxx.PIO_BASE + 0x0020 # Glitch Input Filter Enable Register PIO_IFER Write-only 
PIO_IFDR = SOC_const_sam7pxxx.PIO_BASE + 0x0024 # Glitch Input Filter Disable Register PIO_IFDR Write-only 
PIO_IFSR = SOC_const_sam7pxxx.PIO_BASE + 0x0028 # Glitch Input Filter Status Register PIO_IFSR Read-only 0x0000 0000
PIO_SODR = SOC_const_sam7pxxx.PIO_BASE + 0x0030 # Set Output Data Register PIO_SODR Write-only 
PIO_CODR = SOC_const_sam7pxxx.PIO_BASE + 0x0034 # Clear Output Data Register PIO_CODR Write-only
PIO_ODSR = SOC_const_sam7pxxx.PIO_BASE + 0x0038 # Output Data Status Register PIO_ODSR Read-only
PIO_PDSR = SOC_const_sam7pxxx.PIO_BASE + 0x003C # Pin Data Status Register PIO_PDSR Read-only (3)
PIO_IER = SOC_const_sam7pxxx.PIO_BASE + 0x0040 # Interrupt Enable Register PIO_IER Write-only 
PIO_IDR = SOC_const_sam7pxxx.PIO_BASE + 0x0044 # Interrupt Disable Register PIO_IDR Write-only 
PIO_IMR = SOC_const_sam7pxxx.PIO_BASE + 0x0048 # Interrupt Mask Register PIO_IMR Read-only 0x00000000
PIO_ISR = SOC_const_sam7pxxx.PIO_BASE + 0x004C # Interrupt Status Register (4) PIO_ISR Read-only 0x00000000
PIO_MDER = SOC_const_sam7pxxx.PIO_BASE + 0x0050 # Multi-driver Enable Register PIO_MDER Write-only 
PIO_MDDR = SOC_const_sam7pxxx.PIO_BASE + 0x0054 # Multi-driver Disable Register PIO_MDDR Write-only 
PIO_MDSR = SOC_const_sam7pxxx.PIO_BASE + 0x0058 # Multi-driver Status Register PIO_MDSR Read-only 0x00000000
PIO_PUDR = SOC_const_sam7pxxx.PIO_BASE + 0x0060 # Pull-up Disable Register PIO_PUDR Write-only 
PIO_PUER = SOC_const_sam7pxxx.PIO_BASE + 0x0064 # Pull-up Enable Register PIO_PUER Write-only 
PIO_PUSR = SOC_const_sam7pxxx.PIO_BASE + 0x0068 # Pad Pull-up Status Register PIO_PUSR Read-only 0x00000000
PIO_ASR = SOC_const_sam7pxxx.PIO_BASE + 0x0070 # Peripheral A Select Register (5) PIO_ASR Write-only
PIO_BSR = SOC_const_sam7pxxx.PIO_BASE + 0x0074 # Peripheral B Select Register (5) PIO_BSR Write-only 
PIO_ABSR = SOC_const_sam7pxxx.PIO_BASE + 0x0078 # AB Status Register
# 0x007C to 0x009C Reserved
PIO_OWER = SOC_const_sam7pxxx.PIO_BASE + 0x00A0 # Output Write Enable PIO_OWER Write-only 
PIO_OWDR = SOC_const_sam7pxxx.PIO_BASE + 0x00A4 # Output Write Disable PIO_OWDR Write-only 
PIO_OWSR = SOC_const_sam7pxxx.PIO_BASE + 0x00A8 # Output Write Status Register PIO_OWSR Read-only 0x00000000

#--------------------------------------------------------------------------
# Serial Peripheral Interface (SPI)
SPI_CR = SOC_const_sam7pxxx.SPI_BASE + 0x00 # Control Register SPI_CR Write-only ---
SPI_MR = SOC_const_sam7pxxx.SPI_BASE + 0x04 # Mode Register SPI_MR Read-write 0x0
SPI_RDR = SOC_const_sam7pxxx.SPI_BASE + 0x08 # Receive Data Register SPI_RDR Read-only 0x0
SPI_TDR = SOC_const_sam7pxxx.SPI_BASE + 0x0C # Transmit Data Register SPI_TDR Write-only ---
SPI_SR = SOC_const_sam7pxxx.SPI_BASE + 0x10 # Status Register SPI_SR Read-only 0x000000F0
SPI_IER = SOC_const_sam7pxxx.SPI_BASE + 0x14 # Interrupt Enable Register SPI_IER Write-only ---
SPI_IDR = SOC_const_sam7pxxx.SPI_BASE + 0x18 # Interrupt Disable Register SPI_IDR Write-only ---
SPI_IMR = SOC_const_sam7pxxx.SPI_BASE + 0x1C # Interrupt Mask Register SPI_IMR Read-only 0x0
# 0x20 - 0x2C Reserved
SPI_CSR0 = SOC_const_sam7pxxx.SPI_BASE + 0x30 # Chip Select Register 0 SPI_CSR0 Read-write 0x0
SPI_CSR1 = SOC_const_sam7pxxx.SPI_BASE + 0x34 # Chip Select Register 1 SPI_CSR1 Read-write 0x0
SPI_CSR2 = SOC_const_sam7pxxx.SPI_BASE + 0x38 # Chip Select Register 2 SPI_CSR2 Read-write 0x0
SPI_CSR3 = SOC_const_sam7pxxx.SPI_BASE + 0x3C # Chip Select Register 3 SPI_CSR3 Read-write 0x0
# 0x004C - 0x00F8 Reserved 
# 0x004C - 0x00FC Reserved 
# 0x100 - 0x124 Reserved for the PDC

# NOTE see

#--------------------------------------------------------------------------
# Two-wire Interface (TWI) SAM7S512/256/128/64/321/32
TWI_CR   = SOC_const_sam7pxxx.TWI_BASE + 0x0000 # Control Register TWI_CR Write-only N/A
TWI_MMR  = SOC_const_sam7pxxx.TWI_BASE + 0x0004 # Master Mode Register TWI_MMR Read-write 0x0000
# 0x0008 # Reserved
TWI_IADR = SOC_const_sam7pxxx.TWI_BASE + 0x000C # Internal Address Register TWI_IADR Read-write 0x0000
TWI_CWGR = SOC_const_sam7pxxx.TWI_BASE + 0x0010 # Clock Waveform Generator Register TWI_CWGR Read-write 0x0000
TWI_SR   = SOC_const_sam7pxxx.TWI_BASE + 0x0020 # Status Register TWI_SR Read-only 0x0008
TWI_IER  = SOC_const_sam7pxxx.TWI_BASE + 0x0024 # Interrupt Enable Register TWI_IER Write-only N/A
TWI_IDR  = SOC_const_sam7pxxx.TWI_BASE + 0x0028 # Interrupt Disable Register TWI_IDR Write-only N/A
TWI_IMR  = SOC_const_sam7pxxx.TWI_BASE + 0x002C # Interrupt Mask Register TWI_IMR Read-only 0x0000
TWI_RHR  = SOC_const_sam7pxxx.TWI_BASE + 0x0030 # Receive Holding Register TWI_RHR Read-only 0x0000
TWI_THR  = SOC_const_sam7pxxx.TWI_BASE + 0x0034 # Transmit Holding Register TWI_THR Read-write 0x0000
# 0x0038 - 0x00FC Reserved

#--------------------------------------------------------------------------
# Universal Synchronous Asynchronous Receiver Transceiver (USART)
US_CR = SOC_const_sam7pxxx.USART0_BASE + 0x0000 # Control Register US_CR Write-only 
US_MR = SOC_const_sam7pxxx.USART0_BASE + 0x0004 # Mode Register US_MR Read-write 
US_IER = SOC_const_sam7pxxx.USART0_BASE + 0x0008 # Interrupt Enable Register US_IER Write-only 
US_IDR = SOC_const_sam7pxxx.USART0_BASE + 0x000C # Interrupt Disable Register US_IDR Write-only 
US_IMR = SOC_const_sam7pxxx.USART0_BASE + 0x0010 # Interrupt Mask Register US_IMR Read-only 0x0
US_CSR = SOC_const_sam7pxxx.USART0_BASE + 0x0014 # Channel Status Register US_CSR Read-only 
US_RHR = SOC_const_sam7pxxx.USART0_BASE + 0x0018 # Receiver Holding Register US_RHR Read-only 0x0
US_THR = SOC_const_sam7pxxx.USART0_BASE + 0x001C # Transmitter Holding Register US_THR Write-only 
US_BRGR = SOC_const_sam7pxxx.USART0_BASE + 0x0020 # Baud Rate Generator Register US_BRGR Read-write 0x0
US_RTOR = SOC_const_sam7pxxx.USART0_BASE + 0x0024 # Receiver Time-out Register US_RTOR Read-write 0x0
US_TTGR = SOC_const_sam7pxxx.USART0_BASE + 0x0028 # Transmitter Timeguard Register US_TTGR Read-write 0x0
# 0x2C - 0x3C Reserved
US_FIDI = SOC_const_sam7pxxx.USART0_BASE + 0x0040 # FI DI Ratio Register US_FIDI Read-write 0x174
US_NER = SOC_const_sam7pxxx.USART0_BASE + 0x0044 # Number of Errors Register US_NER Read-only 
# 0x0048 Reserved
US_IF = SOC_const_sam7pxxx.USART0_BASE + 0x004C # IrDA Filter Register US_IF Read-write 0x0

#--------------------------------------------------------------------------
# Synchronous Serial Controller (SSC)
SSC_CR = SOC_const_sam7pxxx.SSC_BASE # Control Register SSC_CR Write
SSC_CMR = SOC_const_sam7pxxx.SSC_BASE + 0x4 # Clock Mode Register SSC_CMR Read-write 0x0
# 0x8 Reserved
# 0xC Reserved
SSC_RCMR = SOC_const_sam7pxxx.SSC_BASE + 0x10 # Receive Clock Mode Register SSC_RCMR Read-write 0x0
SSC_RFMR = SOC_const_sam7pxxx.SSC_BASE + 0x14 # Receive Frame Mode Register SSC_RFMR Read-write 0x0
SSC_TCMR = SOC_const_sam7pxxx.SSC_BASE + 0x18 # Transmit Clock Mode Register SSC_TCMR Read-write 0x0
SSC_TFMR = SOC_const_sam7pxxx.SSC_BASE + 0x1C # Transmit Frame Mode Register SSC_TFMR Read-write 0x0
SSC_RHR = SOC_const_sam7pxxx.SSC_BASE + 0x20 # Receive Holding Register SSC_RHR Read 0x0
SSC_THR = SOC_const_sam7pxxx.SSC_BASE + 0x24 # Transmit Holding Register SSC_THR Write 
# 0x28 Reserved
# 0x2C Reserved
SSC_RSHR = SOC_const_sam7pxxx.SSC_BASE + 0x30 # Receive Sync. Holding Register SSC_RSHR Read 0x0
SSC_TSHR = SOC_const_sam7pxxx.SSC_BASE + 0x34 # Transmit Sync. Holding Register SSC_TSHR Read-write 0x0
SSC_RC0R = SOC_const_sam7pxxx.SSC_BASE + 0x38 # Receive Compare 0 Register SSC_RC0R Read-write 0x0
SSC_RC1R = SOC_const_sam7pxxx.SSC_BASE + 0x3C # Receive Compare 1 Register SSC_RC1R Read-write 0x0
SSC_SR = SOC_const_sam7pxxx.SSC_BASE + 0x40 # Status Register SSC_SR Read 0x000000CC
SSC_IER = SOC_const_sam7pxxx.SSC_BASE + 0x44 # Interrupt Enable Register SSC_IER Write 
SSC_IDR = SOC_const_sam7pxxx.SSC_BASE + 0x48 # Interrupt Disable Register SSC_IDR Write 
SSC_IMR = SOC_const_sam7pxxx.SSC_BASE + 0x4C # Interrupt Mask Register SSC_IMR Read 0x0
# 0x50-0xFC Reserved
# 0x100- 0x124 Reserved for Peripheral Data Controller (PDC)

#--------------------------------------------------------------------------
# Timer Counter (TC)
# NOTE: index by 0x00 + channel * 0x40
TC_CCR = SOC_const_sam7pxxx.TC_BASE + 0x00 # Channel Control Register TC_CCR Write-only 
TC_CMR = SOC_const_sam7pxxx.TC_BASE + 0x04 # Channel Mode Register TC_CMR Read-write 0
# 0x08 Reserved
# 0x0C Reserved
TC_CV = SOC_const_sam7pxxx.TC_BASE + 0x10 # Counter Value TC_CV Read-only 0
TC_RA = SOC_const_sam7pxxx.TC_BASE + 0x14 # Register A TC_RA
TC_RB = SOC_const_sam7pxxx.TC_BASE + 0x18 # Register B TC_RB
TC_RC = SOC_const_sam7pxxx.TC_BASE + 0x1C # Register C TC_RC Read-write 0
TC_SR = SOC_const_sam7pxxx.TC_BASE + 0x20 # Status Register TC_SR Read-only 0
TC_IER = SOC_const_sam7pxxx.TC_BASE + 0x24 # Interrupt Enable Register TC_IER Write-only
TC_IDR = SOC_const_sam7pxxx.TC_BASE + 0x28 # Interrupt Disable Register TC_IDR Write-only
TC_IMR = SOC_const_sam7pxxx.TC_BASE + 0x2C # Interrupt Mask Register TC_IMR Read-only 0
TC_BCR = SOC_const_sam7pxxx.TC_BASE + 0xC0 # Block Control Register TC_BCR Write-only
TC_BMR = SOC_const_sam7pxxx.TC_BASE + 0xC4 # Block Mode Register TC_BMR Read-write 0
# 0xFC Reserved

#--------------------------------------------------------------------------
# Pulse Width Modulation Controller (PWM)

#--------------------------------------------------------------------------
# USB Device Port (UDP) User Interface
UDP_FRM_NUM = SOC_const_sam7pxxx.UDP_BASE + 0x000 # Frame Number Register UDP_FRM_NUM Read-only 0x0000_0000
UDP_GLB_STAT = SOC_const_sam7pxxx.UDP_BASE + 0x004 # Global State Register UDP_GLB_STAT Read-write 0x0000_0000
UDP_FADDR = SOC_const_sam7pxxx.UDP_BASE + 0x008 # Function Address Register UDP_FADDR Read-write 0x0000_0100
UDP_IER = SOC_const_sam7pxxx.UDP_BASE + 0x010 # Interrupt Enable Register UDP_IER Write-only
UDP_IDR = SOC_const_sam7pxxx.UDP_BASE + 0x014 # Interrupt Disable Register UDP_IDR Write-only
UDP_IMR = SOC_const_sam7pxxx.UDP_BASE + 0x018 # Interrupt Mask Register UDP_IMR Read-only 0x0000_1200
UDP_ISR = SOC_const_sam7pxxx.UDP_BASE + 0x01C # Interrupt Status Register UDP_ISR Read-only  (1)
UDP_ICR = SOC_const_sam7pxxx.UDP_BASE + 0x020 # Interrupt Clear Register UDP_ICR Write-only
UDP_RST_EP = SOC_const_sam7pxxx.UDP_BASE + 0x028 # Reset Endpoint Register UDP_RST_EP Read-write
#0x030 + 0x4 * (ept_num - 1) Endpoint Control and Status Register UDP_CSR Read-write 0x0000_0000
UDP_CSR0 = SOC_const_sam7pxxx.UDP_BASE + 0x030
UDP_CSR1 = SOC_const_sam7pxxx.UDP_BASE + 0x034
#0x050 + 0x4 * (ept_num - 1) Endpoint FIFO Data Register UDP_FDR Read-write 0x0000_0000
UDP_FDR0 = SOC_const_sam7pxxx.UDP_BASE + 0x050
UDP_FDR1 = SOC_const_sam7pxxx.UDP_BASE + 0x054

#--------------------------------------------------------------------------
# Analog-to-Digital Converter (ADC)

#--------------------------------------------------------------------------
# ID Code Register - 32 bits
ID_CODE_REG = 0x05B1A03F #0x5B0A01F + b1 # Version, Part, MFG

#--------------------------------------------------------------------------
# make it easier for swapping regs even though all regs are not swapped
#  allocate all 16 anywayPMODE_USR = int("10000", 2)
PMODE_WORK_IDX = 0
PMODE_SYS_IDX = 16 # sys & usr maps to same
PMODE_USR_IDX = 16
PMODE_FIQ_IDX = 32
PMODE_SVC_IDX = 48
PMODE_ABT_IDX = 64 # abort
PMODE_IRQ_IDX = 80
PMODE_MON_IDX = 96
PMODE_HPY_IDX = 112
PMODE_UND_IDX = 128
PMODE_END = 144

#--------------------------------------------------------------------------
regs = array.array('L', [0]) * PMODE_END

baseLocations = 65536 * 15 # 268435455  # 256MByte
memory = array.array('B', [0]) * baseLocations
iomemory = array.array('B', [0]) * baseLocations

