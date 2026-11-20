                Method (WMAE, 3, Serialized)
                {
                    If ((Arg1 == 0x11))
                    {
                        CreateByteField (Arg2, 0x03, GFDI)
                        Switch (ToInteger (GFDI))
                        {
                            Case (Zero)
                            {
                                If ((ToInteger (Arg2) == 0x00010000))
                                {
                                    Return (^^PCI0.LPC0.EC0.REJF (One))
                                }

                                If ((ToInteger (Arg2) == 0x000F0000))
                                {
                                    If ((^^PCI0.GPP0.PG00._STA () == Zero))
                                    {
                                        Return (One)
                                    }
                                    Else
                                    {
                                        Return (Zero)
                                    }
                                }

                                If ((ToInteger (Arg2) == 0x00100000))
                                {
                                    Local0 = Zero
                                    If ((Acquire (^^PCI0.LPC0.EC0.LFCM, 0xA000) == Zero))
                                    {
                                        Local0 = ^^PCI0.LPC0.EC0.FNCE /* \_SB_.PCI0.LPC0.EC0_.FNCE */
                                        Release (^^PCI0.LPC0.EC0.LFCM)
                                    }

                                    Return (Local0)
                                }

                                If ((ToInteger (Arg2) == 0x00030000))
                                {
                                    Local0 = Zero
                                    If ((Acquire (^^PCI0.LPC0.EC0.LFCM, 0xA000) == Zero))
                                    {
                                        Local0 = ^^PCI0.LPC0.EC0.FLBT /* \_SB_.PCI0.LPC0.EC0_.FLBT */
                                        Release (^^PCI0.LPC0.EC0.LFCM)
                                    }

                                    Return (Local0)
                                }

                                If ((ToInteger (Arg2) == 0x00070000))
                                {
                                    Return (0x0001001F)
                                }

                                If ((ToInteger (Arg2) == 0x00080000))
                                {
                                    Return (0x0101)
                                }

                                If ((ToInteger (Arg2) == 0x00090000))
                                {
                                    Return (0x05)
                                }

                                If ((ToInteger (Arg2) == 0x000C0000))
                                {
                                    Return (0x0307)
                                }

                                If ((ToInteger (Arg2) == 0x000E0200))
                                {
                                    Return (^^PCI0.LPC0.EC0.GFPB) /* \_SB_.PCI0.LPC0.EC0_.GFPB */
                                }

                                If ((ToInteger (Arg2) == 0x000E0300))
                                {
                                    Return (^^PCI0.LPC0.EC0.GFPP) /* \_SB_.PCI0.LPC0.EC0_.GFPP */
                                }

                                If ((ToInteger (Arg2) == 0x001E0200))
                                {
                                    If (((ODV1 >= 0x05) && (ODV1 <= 0x09)))
                                    {
                                        Return ((ODV1 - 0x04))
                                    }
                                    Else
                                    {
                                        Return (Zero)
                                    }
                                }

                                If ((ToInteger (Arg2) == 0x001E0300))
                                {
                                    If (((ODV1 >= 0x0A) && (ODV1 <= 0x0E)))
                                    {
                                        Return ((ODV1 - 0x09))
                                    }
                                    Else
                                    {
                                        Return (Zero)
                                    }
                                }

                                If ((ToInteger (Arg2) == 0x001A0000))
                                {
                                    If ((PANT & 0x02))
                                    {
                                        If ((M009 (0x4A) == One))
                                        {
                                            Return (One)
                                        }
                                        Else
                                        {
                                            Return (Zero)
                                        }
                                    }
                                    Else
                                    {
                                        Return (Zero)
                                    }
                                }

                                If ((ToInteger (Arg2) == 0x001F0000))
                                {
                                    If ((^^PCI0.LPC0.EC0.AASS == Zero))
                                    {
                                        Return (One)
                                    }
                                    Else
                                    {
                                        Return (Zero)
                                    }
                                }

                                If ((ToInteger (Arg2) == 0x00210000))
                                {
                                    Local0 = ^^PCI0.LPC0.EC0.GMDM /* \_SB_.PCI0.LPC0.EC0_.GMDM */
                                    If ((Local0 == One))
                                    {
                                        Return (One)
                                    }
                                    ElseIf ((Local0 == 0x02))
                                    {
                                        Return (Zero)
                                    }
                                    Else
                                    {
                                        Return (0x02)
                                    }
                                }

                                If ((ToInteger (Arg2) == 0x00230000))
                                {
                                    If ((M009 (0x03) == One))
                                    {
                                        Return (0x02)
                                    }

                                    Return (One)
                                }

                                If ((ToInteger (Arg2) == 0x00260000))
                                {
                                    Return (^^PCI0.LPC0.EC0.ESSD) /* \_SB_.PCI0.LPC0.EC0_.ESSD */
                                }

                                If ((ToInteger (Arg2) == 0x00270000))
                                {
                                    Return (KBID) /* \KBID */
                                }

                                Return (Zero)
                            }
                            Case (One)
                            {
                                If ((ToInteger (Arg2) == 0x01010000))
                                {
                                    Return (^^PCI0.LPC0.EC0.F5E0) /* \_SB_.PCI0.LPC0.EC0_.F5E0 */
                                }

                                If ((ToInteger (Arg2) == 0x01020000))
                                {
                                    Return (^^PCI0.LPC0.EC0.CCP1) /* \_SB_.PCI0.LPC0.EC0_.CCP1 */
                                }

                                If ((ToInteger (Arg2) == 0x01030000))
                                {
                                    Return (^^PCI0.LPC0.EC0.ADCP) /* \_SB_.PCI0.LPC0.EC0_.ADCP */
                                    Return (Zero)
                                }

                                If ((ToInteger (Arg2) == 0x01040000))
                                {
                                    Return (^^PCI0.LPC0.EC0.F5E2) /* \_SB_.PCI0.LPC0.EC0_.F5E2 */
                                }

                                If ((ToInteger (Arg2) == 0x01060000))
                                {
                                    Return (^^PCI0.LPC0.EC0.CCP2) /* \_SB_.PCI0.LPC0.EC0_.CCP2 */
                                }

                                If ((ToInteger (Arg2) == 0x01070000))
                                {
                                    Local0 = 0x38
                                    Switch (ToInteger (^^PCI0.LPC0.EC0.F5E4))
                                    {
                                        Case (0x2E)
                                        {
                                            Local0 = 0x14
                                        }
                                        Case (0x4E)
                                        {
                                            Local0 = 0x18
                                        }
                                        Case (0x6E)
                                        {
                                            Local0 = 0x1C
                                        }
                                        Case (0x0F)
                                        {
                                            Local0 = 0x20
                                        }
                                        Case (0x2F)
                                        {
                                            Local0 = 0x28
                                        }
                                        Case (0x4F)
                                        {
                                            Local0 = 0x30
                                        }
                                        Case (0x6F)
                                        {
                                            Local0 = 0x38
                                        }
                                        Case (0x10)
                                        {
                                            Local0 = 0x40
                                        }
                                        Case (0x30)
                                        {
                                            Local0 = 0x50
                                        }
                                        Case (0x50)
                                        {
                                            Local0 = 0x60
                                        }
                                        Case (0x70)
                                        {
                                            Local0 = 0x70
                                        }
                                        Case (0x11)
                                        {
                                            Local0 = 0x80
                                        }
                                        Case (0x31)
                                        {
                                            Local0 = 0xA0
                                        }
                                        Default
                                        {
                                            Local0 = 0x38
                                        }

                                    }

                                    Return (Local0)
                                }

                                If ((ToInteger (Arg2) == 0x01080100))
                                {
                                    Return (Zero)
                                }

                                If ((ToInteger (Arg2) == 0x01080200))
                                {
                                    If ((^^PCI0.LPC0.EC0.ACTY () == One))
                                    {
                                        If ((SOCC == 0x02))
                                        {
                                            Return (0x11)
                                        }
                                        Else
                                        {
                                            Return (0x10)
                                        }
                                    }
                                    Else
                                    {
                                        Return (Zero)
                                    }
                                }

                                If ((ToInteger (Arg2) == 0x01080300))
                                {
                                    If ((^^PCI0.LPC0.EC0.ACTY () == One))
                                    {
                                        If ((SOCC == 0x02))
                                        {
                                            Return (0x11)
                                        }
                                        Else
                                        {
                                            Return (0x10)
                                        }
                                    }
                                    Else
                                    {
                                        Return (Zero)
                                    }
                                }

                                If ((ToInteger (Arg2) == 0x0108FF00))
                                {
                                    If ((^^PCI0.LPC0.EC0.ACTY () == One))
                                    {
                                        If ((SOCC == 0x02))
                                        {
                                            Return (0x12)
                                        }
                                        Else
                                        {
                                            Return (0x10)
                                        }
                                    }
                                    Else
                                    {
                                        Return (Zero)
                                    }
                                }

                                Return (Zero)
                            }
                            Case (0x02)
                            {
                                If ((ToInteger (Arg2) == 0x02010000))
                                {
                                    Return (^^PCI0.LPC0.EC0.GPL1) /* \_SB_.PCI0.LPC0.EC0_.GPL1 */
                                }

                                If ((ToInteger (Arg2) == 0x02020000))
                                {
                                    Return (^^PCI0.LPC0.EC0.GPL2) /* \_SB_.PCI0.LPC0.EC0_.GPL2 */
                                }

                                If ((ToInteger (Arg2) == 0x02030000))
                                {
                                    Return (^^PCI0.LPC0.EC0.NTCC) /* \_SB_.PCI0.LPC0.EC0_.NTCC */
                                }

                                If ((ToInteger (Arg2) == 0x02040000))
                                {
                                    Return (^^PCI0.LPC0.EC0.GGAP) /* \_SB_.PCI0.LPC0.EC0_.GGAP */
                                }

                                If ((ToInteger (Arg2) == 0x02050100))
                                {
                                    Return (Zero)
                                }

                                If ((ToInteger (Arg2) == 0x02050200))
                                {
                                    If ((^^PCI0.LPC0.EC0.ACTY () == One))
                                    {
                                        Return (BGPS) /* \BGPS */
                                    }
                                    Else
                                    {
                                        Return (Zero)
                                    }
                                }

                                If ((ToInteger (Arg2) == 0x02050300))
                                {
                                    If ((^^PCI0.LPC0.EC0.ACTY () == One))
                                    {
                                        Return (PGPS) /* \PGPS */
                                    }
                                    Else
                                    {
                                        Return (Zero)
                                    }
                                }

                                If ((ToInteger (Arg2) == 0x0205FF00))
                                {
                                    If ((^^PCI0.LPC0.EC0.ACTY () == One))
                                    {
                                        Return (MGPS) /* \MGPS */
                                    }
                                    Else
                                    {
                                        Return (Zero)
                                    }
                                }

                                If ((ToInteger (Arg2) == 0x02080000))
                                {
                                    If ((QTPP == Zero))
                                    {
                                        Return (0x02)
                                    }

                                    Name (REMA, Zero)
                                    Name (ATTP, Zero)
                                    Name (CTG2, Zero)
                                    Name (DBPP, Zero)
                                    Name (DNPP, Zero)
                                    Name (BTGP, Zero)
                                    Name (ATAB, Zero)
                                    Name (ATAN, Zero)
                                    Name (APL1, Zero)
                                    Name (CTG1, Zero)
                                    ATTP = ^^PCI0.LPC0.EC0.GGAP /* \_SB_.PCI0.LPC0.EC0_.GGAP */
                                    CTG2 = ^^PCI0.LPC0.EC0.GPL2 /* \_SB_.PCI0.LPC0.EC0_.GPL2 */
                                    DBPP = ^^PCI0.LPC0.EC0.GPL1 /* \_SB_.PCI0.LPC0.EC0_.GPL1 */
                                    APL1 = ^^PCI0.LPC0.EC0.CCP2 /* \_SB_.PCI0.LPC0.EC0_.CCP2 */
                                    CTG1 = ^^PCI0.LPC0.EC0.GVBT /* \_SB_.PCI0.LPC0.EC0_.GVBT */
                                    DNPP = ^^PCI0.LPC0.EC0.G1PL /* \_SB_.PCI0.LPC0.EC0_.G1PL */
                                    If ((ATTP > DBPP))
                                    {
                                        ATAB = (ATTP - DBPP) /* \_SB_.GZFD.WMAE.DBPP */
                                    }
                                    Else
                                    {
                                        ATAB = Zero
                                    }

                                    ATAN = (ATTP + DNPP) /* \_SB_.GZFD.WMAE.DNPP */
                                    Local1 = Zero
                                    If ((CTG2 < CTG1))
                                    {
                                        Local1 = (CTG2 + APL1) /* \_SB_.GZFD.WMAE.APL1 */
                                    }
                                    ElseIf ((APL1 < ATAB))
                                    {
                                        Local1 = (CTG2 + DBPP) /* \_SB_.GZFD.WMAE.DBPP */
                                        Local1 += APL1 /* \_SB_.GZFD.WMAE.APL1 */
                                    }
                                    ElseIf ((APL1 > ATAN))
                                    {
                                        Local1 = (CTG2 + APL1) /* \_SB_.GZFD.WMAE.APL1 */
                                        Local1 -= DNPP /* \_SB_.GZFD.WMAE.DNPP */
                                    }
                                    Else
                                    {
                                        Local1 = (CTG2 + ATTP) /* \_SB_.GZFD.WMAE.ATTP */
                                    }

                                    Local2 = Zero
                                    If ((Local1 <= QTPP))
                                    {
                                        Local2 = One
                                    }
                                    ElseIf ((Local1 <= BTPP))
                                    {
                                        Local2 = 0x02
                                    }
                                    ElseIf ((Local1 <= PTPP))
                                    {
                                        Local2 = 0x03
                                    }
                                    Else
                                    {
                                        Local2 = 0x04
                                    }

                                    ^^PCI0.LPC0.EC0.F9FA = Local2
                                    ^^PCI0.LPC0.EC0.LECR (0xD0, One, 0x02, 0x02)
                                    Return (Local2)
                                }

                                If ((ToInteger (Arg2) == 0x02090000))
                                {
                                    Return (DGID) /* \DGID */
                                }

                                If ((ToInteger (Arg2) == 0x020A0000))
                                {
                                    Return (^^PCI0.LPC0.EC0.GVBT) /* \_SB_.PCI0.LPC0.EC0_.GVBT */
                                }

                                If ((ToInteger (Arg2) == 0x020B0000))
                                {
                                    Return (^^PCI0.LPC0.EC0.G1PL) /* \_SB_.PCI0.LPC0.EC0_.G1PL */
                                }

                                Return (Zero)
                            }
                            Case (0x03)
                            {
                                If ((ToInteger (Arg2) == 0x03010001))
                                {
                                    Local0 = Zero
                                    If ((Acquire (^^PCI0.LPC0.EC0.LFCM, 0xA000) == Zero))
                                    {
                                        Local0 = ^^PCI0.LPC0.EC0.EACS /* \_SB_.PCI0.LPC0.EC0_.EACS */
                                        Release (^^PCI0.LPC0.EC0.LFCM)
                                    }

                                    Return (Local0)
                                }

                                If ((ToInteger (Arg2) == 0x03010002))
                                {
                                    Local0 = Zero
                                    If ((Acquire (^^PCI0.LPC0.EC0.LFCM, 0xA000) == Zero))
                                    {
                                        Local0 = ^^PCI0.LPC0.EC0.ETCS /* \_SB_.PCI0.LPC0.EC0_.ETCS */
                                        Release (^^PCI0.LPC0.EC0.LFCM)
                                    }

                                    Return (Local0)
                                }

                                If ((ToInteger (Arg2) == 0x03030000))
                                {
                                    Local0 = Zero
                                    If ((Acquire (^^PCI0.LPC0.EC0.LFCM, 0xA000) == Zero))
                                    {
                                        If ((^^PCI0.LPC0.EC0.PDTT == One))
                                        {
                                            Local0 |= ^^PCI0.LPC0.EC0.APTS /* \_SB_.PCI0.LPC0.EC0_.APTS */
                                        }
                                        ElseIf ((^^PCI0.LPC0.EC0.APTS != Zero))
                                        {
                                            Local0 |= ^^PCI0.LPC0.EC0.APTS /* \_SB_.PCI0.LPC0.EC0_.APTS */
                                            Local0 |= 0x0100
                                        }

                                        Release (^^PCI0.LPC0.EC0.LFCM)
                                    }

                                    Return (Local0)
                                }

                                Return (Zero)
                            }
                            Case (0x04)
                            {
                                If ((ToInteger (Arg2) == 0x04020000))
                                {
                                    Local0 = Zero
                                    If ((Acquire (^^PCI0.LPC0.EC0.LFCM, 0xA000) == Zero))
                                    {
                                        Local0 = ^^PCI0.LPC0.EC0.FNST /* \_SB_.PCI0.LPC0.EC0_.FNST */
                                        Release (^^PCI0.LPC0.EC0.LFCM)
                                    }

                                    Return (Local0)
                                }

                                If ((ToInteger (Arg2) == 0x04030001))
                                {
                                    Local0 = Zero
                                    If ((Acquire (^^PCI0.LPC0.EC0.LFCM, 0xA000) == Zero))
                                    {
                                        Local0 = (^^PCI0.LPC0.EC0.FANS * 0x64)
                                        Release (^^PCI0.LPC0.EC0.LFCM)
                                    }

                                    Return (Local0)
                                }

                                If ((ToInteger (Arg2) == 0x04030002))
                                {
                                    Local0 = Zero
                                    If ((Acquire (^^PCI0.LPC0.EC0.LFCM, 0xA000) == Zero))
                                    {
                                        Local0 = (^^PCI0.LPC0.EC0.FA2S * 0x64)
                                        Release (^^PCI0.LPC0.EC0.LFCM)
                                    }

                                    Return (Local0)
                                }

                                If ((ToInteger (Arg2) == 0x04030004))
                                {
                                    Local0 = Zero
                                    If ((Acquire (^^PCI0.LPC0.EC0.LFCM, 0xA000) == Zero))
                                    {
                                        Local0 = (^^PCI0.LPC0.EC0.FASF * 0x64)
                                        Release (^^PCI0.LPC0.EC0.LFCM)
                                    }

                                    Return (Local0)
                                }

                                Return (Zero)
                            }
                            Case (0x05)
                            {
                                If ((ToInteger (Arg2) == 0x05010000))
                                {
                                    Local0 = Zero
                                    If ((Acquire (^^PCI0.LPC0.EC0.LFCM, 0xA000) == Zero))
                                    {
                                        Local0 = ^^PCI0.LPC0.EC0.CPUS /* \_SB_.PCI0.LPC0.EC0_.CPUS */
                                        Release (^^PCI0.LPC0.EC0.LFCM)
                                    }

                                    Return (Local0)
                                }

                                If ((ToInteger (Arg2) == 0x05040000))
                                {
                                    Local0 = Zero
                                    If ((Acquire (^^PCI0.LPC0.EC0.LFCM, 0xA000) == Zero))
                                    {
                                        Local0 = ^^PCI0.LPC0.EC0.CPUT /* \_SB_.PCI0.LPC0.EC0_.CPUT */
                                        Release (^^PCI0.LPC0.EC0.LFCM)
                                    }

                                    Return (Local0)
                                }

                                If ((ToInteger (Arg2) == 0x05050000))
                                {
                                    Local0 = Zero
                                    If ((Acquire (^^PCI0.LPC0.EC0.LFCM, 0xA000) == Zero))
                                    {
                                        Local0 = ^^PCI0.LPC0.EC0.GPUT /* \_SB_.PCI0.LPC0.EC0_.GPUT */
                                        Release (^^PCI0.LPC0.EC0.LFCM)
                                    }

                                    Return (Local0)
                                }

                                Return (Zero)
                            }
                            Case (0x06)
                            {
                                If ((ToInteger (Arg2) == 0x06010000))
                                {
                                    Return (^^PCI0.LPC0.EC0.LECR (0xC0, 0x12, 0xFF, One))
                                }

                                Return (Zero)
                            }
                            Case (0x08)
                            {
                                If ((ToInteger (Arg2) == 0x08010001))
                                {
                                    Local0 = Zero
                                    Local1 = Zero
                                    If ((Acquire (^^PCI0.LPC0.EC0.LFCM, 0xA000) == Zero))
                                    {
                                        Local0 = ^^PCI0.LPC0.EC0.FWBT /* \_SB_.PCI0.LPC0.EC0_.FWBT */
                                        Local1 = ^^PCI0.LPC0.EC0.BA1P /* \_SB_.PCI0.LPC0.EC0_.BA1P */
                                        Local0 &= 0xFF
                                        Release (^^PCI0.LPC0.EC0.LFCM)
                                    }

                                    If ((Local1 == One))
                                    {
                                        If ((((Local0 == One) || (Local0 == 0x06)) || (Local0 == 0x08)))
                                        {
                                            Return (One)
                                        }
                                        Else
                                        {
                                            Return (0x02)
                                        }
                                    }
                                    Else
                                    {
                                        Return (Zero)
                                    }
                                }

                                Return (Zero)
                            }
                            Case (0x0A)
                            {
                                Return (Zero)
                            }
                            Default
                            {
                                Return (Zero)
                            }

                        }

                        Return (Zero)
                    }

                    If ((Arg1 == 0x12))
                    {
                        CreateDWordField (Arg2, Zero, SFV0)
                        CreateByteField (Arg2, 0x03, SFDI)
                        CreateDWordField (Arg2, 0x04, SFV1)
                        Switch (ToInteger (SFDI))
                        {
                            Case (Zero)
                            {
                                If ((SFV0 == 0x00010000))
                                {
                                    If (^^PCI0.LPC0.EC0.ECAV)
                                    {
                                        Local0 = ToInteger (SFV1)
                                        ^^PCI0.LPC0.EC0.WEJF (One, Local0)
                                        Local1 = HTPL ()
                                        Return (Local1)
                                    }
                                }

                                If ((SFV0 == 0x00100000))
                                {
                                    If ((Acquire (^^PCI0.LPC0.EC0.LFCM, 0xA000) == Zero))
                                    {
                                        If ((ToInteger (SFV1) == One))
                                        {
                                            ^^PCI0.LPC0.EC0.FNCE = One
                                        }
                                        Else
                                        {
                                            ^^PCI0.LPC0.EC0.FNCE = Zero
                                        }

                                        Release (^^PCI0.LPC0.EC0.LFCM)
                                    }

                                    Return (Zero)
                                }

                                If ((SFV0 == 0x00030000))
                                {
                                    If ((Acquire (^^PCI0.LPC0.EC0.LFCM, 0xA000) == Zero))
                                    {
                                        If ((ToInteger (SFV1) == One))
                                        {
                                            WSMI (0x05)
                                            ^^PCI0.LPC0.EC0.FLBT = One
                                        }
                                        Else
                                        {
                                            WSMI (0x06)
                                            ^^PCI0.LPC0.EC0.FLBT = Zero
                                        }

                                        Release (^^PCI0.LPC0.EC0.LFCM)
                                    }

                                    Return (Zero)
                                }

                                If ((SFV0 == 0x000A0000))
                                {
                                    If ((ToInteger (SFV1) == One))
                                    {
                                        LSKD = 0x31
                                        Notify (WMIU, 0xD0) // Hardware-Specific
                                    }

                                    If ((ToInteger (SFV1) == 0x02))
                                    {
                                        LSKD = 0x32
                                        Notify (WMIU, 0xD0) // Hardware-Specific
                                    }

                                    Return (Zero)
                                }

                                If ((SFV0 == 0x001A0000))
                                {
                                    If ((PANT & 0x02))
                                    {
                                        If ((SFV1 == One))
                                        {
                                            WECM (0x7F, One)
                                            M010 (0x4A, One)
                                        }
                                        Else
                                        {
                                            WECM (0x7F, Zero)
                                            M010 (0x4A, Zero)
                                        }
                                    }

                                    Return (Zero)
                                }

                                If ((SFV0 == 0x000E0200))
                                {
                                    If ((ToInteger (SFV1) == Zero))
                                    {
                                        ^^PCI0.LPC0.EC0.GFPB = Zero
                                    }
                                    Else
                                    {
                                        ^^PCI0.LPC0.EC0.GFPB = One
                                    }

                                    If ((Zero == ODV1))
                                    {
                                        Notify (GZFD, 0xEC) // Hardware-Specific
                                        Return (Zero)
                                    }

                                    If (((ODV1 >= 0x05) && (ODV1 <= 0x09)))
                                    {
                                        Notify (GZFD, 0xEC) // Hardware-Specific
                                        Return (Zero)
                                    }

                                    Return (Zero)
                                }

                                If ((SFV0 == 0x000E0300))
                                {
                                    If ((ToInteger (SFV1) == Zero))
                                    {
                                        ^^PCI0.LPC0.EC0.GFPP = Zero
                                    }
                                    Else
                                    {
                                        ^^PCI0.LPC0.EC0.GFPP = One
                                    }

                                    If ((One == ODV1))
                                    {
                                        Notify (GZFD, 0xEC) // Hardware-Specific
                                        Return (Zero)
                                    }

                                    If (((ODV1 >= 0x0A) && (ODV1 <= 0x0E)))
                                    {
                                        Notify (GZFD, 0xEC) // Hardware-Specific
                                        Return (Zero)
                                    }

                                    Return (Zero)
                                }

                                If ((SFV0 == 0x001E0200))
                                {
                                    Local0 = ToInteger (SFV1)
                                    If (((Local0 > Zero) && (Local0 <= 0x05)))
                                    {
                                        ODV5 = Zero
                                        ODV1 = (Local0 + 0x04)
                                        ^^PCI0.LPC0.EC0.LECR (0xD9, One, One, 0x02)
                                    }
                                    Else
                                    {
                                        ODV1 = Zero
                                        ODV5 = Zero
                                        ^^PCI0.LPC0.EC0.LECR (0xD9, One, 0x02, 0x02)
                                    }

                                    ^^PCI0.LPC0.EC0.FNQT (0xFF, 0xFF)
                                    If (CondRefOf (\_SB.NPCF))
                                    {
                                        Sleep (0x05)
                                        Notify (NPCF, 0xC0) // Hardware-Specific
                                    }

                                    Return (Zero)
                                }

                                If ((SFV0 == 0x001E0300))
                                {
                                    Local0 = ToInteger (SFV1)
                                    If (((Local0 > Zero) && (Local0 <= 0x05)))
                                    {
                                        ODV5 = Zero
                                        ODV1 = (Local0 + 0x09)
                                        ^^PCI0.LPC0.EC0.LECR (0xD9, One, One, 0x02)
                                    }
                                    Else
                                    {
                                        ODV1 = One
                                        ODV5 = Zero
                                        ^^PCI0.LPC0.EC0.LECR (0xD9, One, 0x02, 0x02)
                                    }

                                    ^^PCI0.LPC0.EC0.FNQT (0xFF, 0xFF)
                                    If (CondRefOf (\_SB.NPCF))
                                    {
                                        Sleep (0x05)
                                        Notify (NPCF, 0xC0) // Hardware-Specific
                                    }

                                    Return (Zero)
                                }

                                If ((SFV0 == 0x001F0000))
                                {
                                    If ((ToInteger (SFV1) == Zero))
                                    {
                                        ^^PCI0.LPC0.EC0.AASS = One
                                    }
                                    Else
                                    {
                                        ^^PCI0.LPC0.EC0.AASS = Zero
                                    }

                                    Return (Zero)
                                }

                                If ((SFV0 == 0x00210000))
                                {
                                    If ((ToInteger (SFV1) == Zero))
                                    {
                                        ^^PCI0.LPC0.EC0.GMDM = 0x02
                                        Return (Zero)
                                    }
                                    ElseIf ((ToInteger (SFV1) == One))
                                    {
                                        ^^PCI0.LPC0.EC0.GMDM = One
                                        Return (Zero)
                                    }
                                    Else
                                    {
                                        ^^PCI0.LPC0.EC0.GMDM = Zero
                                    }

                                    Return (Zero)
                                }

                                If ((SFV0 == 0x001C0001))
                                {
                                    If ((ToInteger (SFV1) == Zero))
                                    {
                                        ^^PCI0.LPC0.EC0.LECR (0xD3, Zero, Zero, 0x02)
                                    }
                                    Else
                                    {
                                        ^^PCI0.LPC0.EC0.LECR (0xD3, Zero, One, 0x02)
                                    }

                                    Return (Zero)
                                }

                                If ((SFV0 == 0x001C0002))
                                {
                                    Local0 = ToBuffer (SFV1)
                                    CreateByteField (Local0, Zero, ATSL)
                                    CreateByteField (Local0, One, ATSH)
                                    ^^PCI0.LPC0.EC0.LECR (0xD2, ATSH, ATSL, 0x02)
                                    Return (Zero)
                                }

                                If ((SFV0 == 0x00260000))
                                {
                                    If ((Acquire (^^PCI0.LPC0.EC0.LFCM, 0xA000) == Zero))
                                    {
                                        If ((SFV1 == One))
                                        {
                                            WSMI (0x0D)
                                            ^^PCI0.LPC0.EC0.ESSD = One
                                        }
                                        Else
                                        {
                                            WSMI (0x0E)
                                            ^^PCI0.LPC0.EC0.ESSD = Zero
                                        }

                                        Release (^^PCI0.LPC0.EC0.LFCM)
                                    }

                                    Return (Zero)
                                }

                                Return (Zero)
                            }
                            Case (One)
                            {
                                If ((SFV0 == 0x01010000))
                                {
                                    ^^PCI0.LPC0.EC0.F5E0 = ToInteger (SFV1)
                                    If ((ODV1 == 0x03))
                                    {
                                        Local1 = (^^PCI0.LPC0.EC0.F5E0 * 0x03E8)
                                        ^^PCI0.LPC0.EC0.FNQT (0x07, Local1)
                                    }

                                    Return (Zero)
                                }

                                If ((SFV0 == 0x01020000))
                                {
                                    ^^PCI0.LPC0.EC0.CCP1 = ToInteger (SFV1)
                                    If ((ODV1 == 0x03))
                                    {
                                        If ((DBFS == One))
                                        {
                                            Local1 = (^^PCI0.LPC0.EC0.CCP2 * 0x03E8)
                                        }
                                        Else
                                        {
                                            Local1 = (^^PCI0.LPC0.EC0.CCP1 * 0x03E8)
                                        }

                                        ^^PCI0.LPC0.EC0.FNQT (0x05, Local1)
                                    }

                                    Return (Zero)
                                }

                                If ((SFV0 == 0x01030000))
                                {
                                    ^^PCI0.LPC0.EC0.ADCP = ToInteger (SFV1)
                                    If ((ODV1 == 0x03))
                                    {
                                        Local1 = (^^PCI0.LPC0.EC0.ADCP * 0x03E8)
                                        ^^PCI0.LPC0.EC0.FNQT (0x06, Local1)
                                    }

                                    Return (Zero)
                                }

                                If ((SFV0 == 0x01040000))
                                {
                                    ^^PCI0.LPC0.EC0.F5E2 = ToInteger (SFV1)
                                    If ((ODV1 == 0x03))
                                    {
                                        ^^PCI0.LPC0.EC0.FNQT (0x03, ^^PCI0.LPC0.EC0.F5E2)
                                    }

                                    Return (Zero)
                                }

                                If ((SFV0 == 0x01060000))
                                {
                                    ^^PCI0.LPC0.EC0.CCP2 = ToInteger (SFV1)
                                    If ((ODV1 == 0x03))
                                    {
                                        If ((DBFS == One))
                                        {
                                            Local1 = (^^PCI0.LPC0.EC0.CCP2 * 0x03E8)
                                        }
                                        Else
                                        {
                                            Local1 = (^^PCI0.LPC0.EC0.CCP1 * 0x03E8)
                                        }

                                        ^^PCI0.LPC0.EC0.FNQT (0x05, Local1)
                                    }

                                    Return (Zero)
                                }

                                If ((SFV0 == 0x01070000))
                                {
                                    Local0 = Zero
                                    Switch (ToInteger (SFV1))
                                    {
                                        Case (0x14)
                                        {
                                            Local0 = 0x2E
                                        }
                                        Case (0x18)
                                        {
                                            Local0 = 0x4E
                                        }
                                        Case (0x1C)
                                        {
                                            Local0 = 0x6E
                                        }
                                        Case (0x20)
                                        {
                                            Local0 = 0x0F
                                        }
                                        Case (0x28)
                                        {
                                            Local0 = 0x2F
                                        }
                                        Case (0x30)
                                        {
                                            Local0 = 0x4F
                                        }
                                        Case (0x38)
                                        {
                                            Local0 = 0x6F
                                        }
                                        Case (0x40)
                                        {
                                            Local0 = 0x10
                                        }
                                        Case (0x50)
                                        {
                                            Local0 = 0x30
                                        }
                                        Case (0x60)
                                        {
                                            Local0 = 0x50
                                        }
                                        Case (0x70)
                                        {
                                            Local0 = 0x70
                                        }
                                        Case (0x80)
                                        {
                                            Local0 = 0x11
                                        }
                                        Case (0xA0)
                                        {
                                            Local0 = 0x31
                                        }
                                        Default
                                        {
                                            Local0 = 0x6F
                                        }

                                    }

                                    ^^PCI0.LPC0.EC0.F5E4 = Local0
                                    If ((ODV1 == 0x03)){}
                                    Return (Zero)
                                }

                                If ((SFV0 == 0x01080100))
                                {
                                    Return (Zero)
                                }

                                If ((SFV0 == 0x01080200))
                                {
                                    If ((ToInteger (SFV1) == Zero))
                                    {
                                        WSMI (0x0C)
                                    }
                                    Else
                                    {
                                        WSMI (0x0B)
                                    }

                                    Return (Zero)
                                }

                                If ((SFV0 == 0x01080300))
                                {
                                    If ((ToInteger (SFV1) == Zero))
                                    {
                                        WSMI (0x0C)
                                    }
                                    Else
                                    {
                                        WSMI (0x0B)
                                    }

                                    Return (Zero)
                                }

                                If ((SFV0 == 0x0108FF00))
                                {
                                    If ((ToInteger (SFV1) == Zero))
                                    {
                                        WSMI (0x0C)
                                    }
                                    Else
                                    {
                                        WSMI (0x0B)
                                    }

                                    Return (Zero)
                                }

                                Return (Zero)
                            }
                            Case (0x02)
                            {
                                If ((SFV0 == 0x02070000))
                                {
                                    If ((ToInteger (SFV1) == Zero))
                                    {
                                        ^^PCI0.LPC0.EC0.GSTA = One
                                    }
                                    Else
                                    {
                                        ^^PCI0.LPC0.EC0.GSTA = Zero
                                    }

                                    HTPL ()
                                    Return (Zero)
                                }

                                If ((SFV0 == 0x02010000))
                                {
                                    ^^PCI0.LPC0.EC0.GPL1 = ToInteger (SFV1)
                                    If ((ODV1 == 0x03))
                                    {
                                        If (CondRefOf (\_SB.NPCF))
                                        {
                                            Notify (NPCF, 0xC0) // Hardware-Specific
                                        }
                                    }

                                    Return (Zero)
                                }

                                If ((SFV0 == 0x02020000))
                                {
                                    ^^PCI0.LPC0.EC0.GPL2 = ToInteger (SFV1)
                                    If ((ODV1 == 0x03))
                                    {
                                        If (CondRefOf (\_SB.NPCF))
                                        {
                                            Notify (NPCF, 0xC0) // Hardware-Specific
                                        }
                                    }

                                    Return (Zero)
                                }

                                If ((SFV0 == 0x02030000))
                                {
                                    ^^PCI0.LPC0.EC0.NTCC = ToInteger (SFV1)
                                    If ((ODV1 == 0x03))
                                    {
                                        If (CondRefOf (\_SB.PCI0.GPP0.PEGP))
                                        {
                                            If ((^^PCI0.LPC0.EC0.CHNG () != Zero))
                                            {
                                                Notify (^^PCI0.GPP0.PEGP, 0xC0) // Hardware-Specific
                                            }
                                        }
                                    }

                                    Return (Zero)
                                }

                                If ((SFV0 == 0x02040000))
                                {
                                    ^^PCI0.LPC0.EC0.GGAP = ToInteger (SFV1)
                                    If ((ODV1 == 0x03))
                                    {
                                        If (CondRefOf (\_SB.NPCF))
                                        {
                                            Notify (NPCF, 0xC0) // Hardware-Specific
                                        }
                                    }

                                    Return (Zero)
                                }

                                If ((SFV0 == 0x020B0000))
                                {
                                    ^^PCI0.LPC0.EC0.G1PL = ToInteger (SFV1)
                                    If ((ODV1 == 0x03))
                                    {
                                        If (CondRefOf (\_SB.NPCF))
                                        {
                                            Notify (NPCF, 0xC0) // Hardware-Specific
                                        }
                                    }

                                    Return (Zero)
                                }

                                If ((SFV0 == 0x02050100))
                                {
                                    Return (Zero)
                                }

                                If ((SFV0 == 0x02050200))
                                {
                                    If ((ToInteger (SFV1) == Zero))
                                    {
                                        BGPS = 0x10
                                    }
                                    Else
                                    {
                                        BGPS = 0x11
                                    }

                                    Return (Zero)
                                }

                                If ((SFV0 == 0x02050300))
                                {
                                    If ((ToInteger (SFV1) == Zero))
                                    {
                                        PGPS = 0x10
                                    }
                                    Else
                                    {
                                        PGPS = 0x11
                                    }

                                    Return (Zero)
                                }

                                If ((SFV0 == 0x0205FF00))
                                {
                                    If ((ToInteger (SFV1) == Zero))
                                    {
                                        MGPS = 0x10
                                    }
                                    Else
                                    {
                                        MGPS = 0x12
                                    }

                                    Return (Zero)
                                }

                                Return (Zero)
                            }
                            Case (0x03)
                            {
                                If ((SFV0 == 0x03010001))
                                {
                                    If ((ToInteger (SFV1) == One))
                                    {
                                        WSMI (0x07)
                                        ^^PCI0.LPC0.EC0.EACS = One
                                    }
                                    Else
                                    {
                                        WSMI (0x08)
                                        ^^PCI0.LPC0.EC0.EACS = Zero
                                    }

                                    Return (Zero)
                                }

                                If ((SFV0 == 0x03010002))
                                {
                                    If ((ToInteger (SFV1) == One))
                                    {
                                        WSMI (0x09)
                                        ^^PCI0.LPC0.EC0.ETCS = One
                                    }
                                    Else
                                    {
                                        WSMI (0x0A)
                                        ^^PCI0.LPC0.EC0.ETCS = Zero
                                    }

                                    Return (Zero)
                                }

                                Return (Zero)
                            }
                            Case (0x04)
                            {
                                If ((SFV0 == 0x04020000))
                                {
                                    If ((Acquire (^^PCI0.LPC0.EC0.LFCM, 0xA000) == Zero))
                                    {
                                        If ((SFV1 == One))
                                        {
                                            ^^PCI0.LPC0.EC0.FNST = One
                                        }
                                        Else
                                        {
                                            ^^PCI0.LPC0.EC0.FNST = Zero
                                        }

                                        Release (^^PCI0.LPC0.EC0.LFCM)
                                    }

                                    Return (Zero)
                                }

                                If ((SFV0 == 0x04020001))
                                {
                                    Return (Zero)
                                }

                                If ((SFV0 == 0x04030001))
                                {
                                    Local0 = (SFV1 / 0x64)
                                    ^^PCI0.LPC0.EC0.LECR (0xD1, One, Local0, 0x02)
                                    Return (Zero)
                                }

                                If ((SFV0 == 0x04030002))
                                {
                                    Local0 = (SFV1 / 0x64)
                                    ^^PCI0.LPC0.EC0.LECR (0xD1, 0x02, Local0, 0x02)
                                    Return (Zero)
                                }

                                If ((SFV0 == 0x04030004))
                                {
                                    Local0 = (SFV1 / 0x64)
                                    ^^PCI0.LPC0.EC0.LECR (0xD1, 0x03, Local0, 0x02)
                                    Return (Zero)
                                }

                                Return (Zero)
                            }
                            Case (0x05)
                            {
                                Return (Zero)
                            }
                            Case (0x06)
                            {
                                If ((SFV0 == 0x06010000))
                                {
                                    If ((SFV1 == 0x02))
                                    {
                                        ^^PCI0.LPC0.EC0.LECR (0xC0, 0x10, 0xFF, One)
                                        Sleep (One)
                                        WSMI (0x02)
                                        Return (Zero)
                                    }
                                    ElseIf ((SFV1 == One))
                                    {
                                        ^^PCI0.LPC0.EC0.LECR (0xC0, 0x11, 0xFF, One)
                                        Sleep (One)
                                        WSMI (One)
                                        Return (Zero)
                                    }
                                    Else
                                    {
                                        Return (Zero)
                                    }
                                }

                                Return (Zero)
                            }
                            Case (0x0A)
                            {
                                Return (Zero)
                            }
                            Default
                            {
                                Return (Zero)
                            }

                        }

                        Return (Zero)
                    }

                    If ((Arg1 == 0x13))
                    {
                        CreateDWordField (Arg2, Zero, GIDS)
                        CreateDWordField (Arg2, 0x04, GDMD)
                        If ((ToInteger (GIDS) == 0x08010002))
                        {
                            If ((ToInteger (GDMD) == 0x30))
                            {
                                Name (ES30, Buffer (0x10)
                                {
                                    /* 0000 */  0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  // ........
                                    /* 0008 */  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00   // ........
                                })
                                CreateWordField (ES30, 0x04, TTCG)
                                CreateWordField (ES30, 0x06, TTRT)
                                CreateWordField (ES30, 0x08, HVTM)
                                CreateWordField (ES30, 0x0A, HTTM)
                                CreateWordField (ES30, 0x0C, HIHV)
                                TTCG = ^^PCI0.LPC0.EC0.B301 /* \_SB_.PCI0.LPC0.EC0_.B301 */
                                TTRT = ^^PCI0.LPC0.EC0.B302 /* \_SB_.PCI0.LPC0.EC0_.B302 */
                                HVTM = ^^PCI0.LPC0.EC0.B303 /* \_SB_.PCI0.LPC0.EC0_.B303 */
                                HTTM = ^^PCI0.LPC0.EC0.B304 /* \_SB_.PCI0.LPC0.EC0_.B304 */
                                HIHV = ^^PCI0.LPC0.EC0.B305 /* \_SB_.PCI0.LPC0.EC0_.B305 */
                                Return (ES30) /* \_SB_.GZFD.WMAE.ES30 */
                            }

                            If ((ToInteger (GDMD) == 0x50))
                            {
                                Name (ES50, Buffer (0x08)
                                {
                                     0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00   // ........
                                })
                                CreateByteField (ES50, 0x04, ES5D)
                                ES5D = ^^PCI0.LPC0.EC0.NTCG /* \_SB_.PCI0.LPC0.EC0_.NTCG */
                                Return (ES50) /* \_SB_.GZFD.WMAE.ES50 */
                            }

                            If ((ToInteger (GDMD) == 0x60))
                            {
                                Name (ES60, Buffer (0x24)
                                {
                                     0x00                                             // .
                                })
                                CreateDWordField (ES60, Zero, E60S)
                                CreateDWordField (ES60, 0x04, E600)
                                CreateDWordField (ES60, 0x08, E601)
                                CreateDWordField (ES60, 0x0C, E602)
                                CreateDWordField (ES60, 0x10, E603)
                                CreateDWordField (ES60, 0x14, E604)
                                CreateDWordField (ES60, 0x18, E605)
                                CreateDWordField (ES60, 0x1C, E606)
                                CreateDWordField (ES60, 0x20, E607)
                                E600 = ^^PCI0.LPC0.EC0.BBA1 /* \_SB_.PCI0.LPC0.EC0_.BBA1 */
                                E601 = ^^PCI0.LPC0.EC0.BBB1 /* \_SB_.PCI0.LPC0.EC0_.BBB1 */
                                E602 = ^^PCI0.LPC0.EC0.BBC1 /* \_SB_.PCI0.LPC0.EC0_.BBC1 */
                                E603 = ^^PCI0.LPC0.EC0.BBD1 /* \_SB_.PCI0.LPC0.EC0_.BBD1 */
                                E604 = ^^PCI0.LPC0.EC0.BBE1 /* \_SB_.PCI0.LPC0.EC0_.BBE1 */
                                E605 = ^^PCI0.LPC0.EC0.BBF1 /* \_SB_.PCI0.LPC0.EC0_.BBF1 */
                                E606 = ^^PCI0.LPC0.EC0.BBG1 /* \_SB_.PCI0.LPC0.EC0_.BBG1 */
                                E607 = ^^PCI0.LPC0.EC0.BBH1 /* \_SB_.PCI0.LPC0.EC0_.BBH1 */
                                E60S = 0x08
                                Return (ES60) /* \_SB_.GZFD.WMAE.ES60 */
                            }

                            If ((ToInteger (GDMD) == 0x62))
                            {
                                Name (ES62, Buffer (0x14)
                                {
                                     0x00                                             // .
                                })
                                CreateDWordField (ES62, Zero, E62S)
                                CreateDWordField (ES62, 0x04, E620)
                                CreateDWordField (ES62, 0x08, E621)
                                CreateDWordField (ES62, 0x0C, E622)
                                CreateDWordField (ES62, 0x10, E623)
                                E620 = ^^PCI0.LPC0.EC0.BB61 /* \_SB_.PCI0.LPC0.EC0_.BB61 */
                                E621 = ^^PCI0.LPC0.EC0.BB62 /* \_SB_.PCI0.LPC0.EC0_.BB62 */
                                E622 = ^^PCI0.LPC0.EC0.BB63 /* \_SB_.PCI0.LPC0.EC0_.BB63 */
                                E623 = ^^PCI0.LPC0.EC0.BB64 /* \_SB_.PCI0.LPC0.EC0_.BB64 */
                                E62S = 0x04
                                Return (ES62) /* \_SB_.GZFD.WMAE.ES62 */
                            }

                            If ((ToInteger (GDMD) == 0x3E))
                            {
                                Name (ES3E, Buffer (0x08)
                                {
                                     0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00   // ........
                                })
                                CreateWordField (ES3E, 0x04, E3ED)
                                If ((Acquire (^^PCI0.LPC0.EC0.LFCM, 0xA000) == Zero))
                                {
                                    E3ED = ((^^PCI0.LPC0.EC0.BTSB << 0x0D) | ^^PCI0.LPC0.EC0.LSSP) /* \_SB_.PCI0.LPC0.EC0_.LSSP */
                                    Release (^^PCI0.LPC0.EC0.LFCM)
                                }

                                Return (ES3E) /* \_SB_.GZFD.WMAE.ES3E */
                            }
                        }
                    }

                    If ((Arg1 == 0x63))
                    {
                        Name (GDBP, Buffer (0x64)
                        {
                             0x00                                             // .
                        })
                        If ((GKHF == Zero))
                        {
                            GKHF = One
                            Return (GDBP) /* \_SB_.GZFD.WMAE.GDBP */
                        }

                        GKHF = Zero
                        CreateByteField (Arg2, Zero, GCMD)
                        If ((ToInteger (GCMD) == 0x5A))
                        {
                            Return (Buffer (0x08)
                            {
                                 0x04, 0x00, 0x00, 0x00, 0x03, 0x00, 0x02, 0x00   // ........
                            })
                        }

                        If ((ToInteger (GCMD) == 0x30))
                        {
                            CreateByteField (Arg2, One, HADL)
                            CreateByteField (Arg2, 0x02, HADH)
                            Local0 = ^^PCI0.LPC0.EC0.LECR (0xA8, HADH, HADL, 0x02)
                            If ((Local0 != 0xAA))
                            {
                                Return (Buffer (0x05)
                                {
                                     0x01, 0x00, 0x00, 0x00, 0x01                     // .....
                                })
                            }

                            Return (Buffer (0x05)
                            {
                                 0x01, 0x00, 0x00, 0x00, 0x00                     // .....
                            })
                        }

                        If ((ToInteger (GCMD) == 0x31))
                        {
                            Local0 = ^^PCI0.LPC0.EC0.LECR (0xA9, 0xFF, 0xFF, Zero)
                            If ((Local0 != 0xAA))
                            {
                                Return (Buffer (0x05)
                                {
                                     0x01, 0x00, 0x00, 0x00, 0x01                     // .....
                                })
                            }

                            Return (Buffer (0x05)
                            {
                                 0x01, 0x00, 0x00, 0x00, 0x00                     // .....
                            })
                        }

                        If ((ToInteger (GCMD) == 0x32))
                        {
                            Local0 = ^^PCI0.LPC0.EC0.LECR (0xAA, 0xFF, 0xFF, Zero)
                            If ((Local0 != 0xAA))
                            {
                                Return (Buffer (0x05)
                                {
                                     0x01, 0x00, 0x00, 0x00, 0x01                     // .....
                                })
                            }

                            Return (Buffer (0x05)
                            {
                                 0x01, 0x00, 0x00, 0x00, 0x00                     // .....
                            })
                        }
                    }
                }

