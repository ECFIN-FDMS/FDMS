from fdms.config.variable_groups import TM, NA_VO


# Variables from AMECO used explicitly in the calculations
AMECO_VARS_1 = [
    'NLTN.1.0.0.0', 'NSTD.1.0.0.0', 'NECN.1.0.0.0', 'NLHT.1.0.0.0', 'NLHT9.1.0.0.0', 'NLCN.1.0.0.0', 'OMGS.1.1.0.0',
    'OXGS.1.1.0.0', 'OXGN.1.1.0.0', 'OXSN.1.1.0.0', 'OIGT.1.1.0.0', 'OIGCO.1.1.0.0', 'OCPH.1.1.0.0', 'OUNT.1.1.0.0',
    'OUTT.1.1.0.0', 'OITT.1.0.0.0', 'RVGDP.1.1.0.0', 'UVGDH.1.0.0.0', 'UKCT.1.0.0.0', 'FETD9.1.0.0.0', 'FWTD.1.0.0.0',
    'ZUTN.1.0.0.0', 'NUTN.1.0.0.0', 'UTOG.1.0.0.0', 'UUCG.1.0.0.0', 'URCG.1.0.0.0', 'UUTG.1.0.0.0', 'URTG.1.0.0.0',
    'UBLG.1.0.0.0', 'UBLGI.1.0.0.0', 'UBLGIE.1.0.0.0', 'UTAT.1.0.0.0', 'UOOMS.1.0.0.0', 'UTTG.1.0.0.0', 'UDGGL.1.0.0.0',
    'UCRG.1.0.0.0', 'USGG.1.0.0.0', 'UUTGE.1.0.0.0', 'UUCGI.1.0.0.0', 'UTCT.1.0.0.0', 'USGC.1.0.0.0', 'UOGC.1.0.0.0',
    'UBLC.1.0.0.0', 'UYOH.1.0.0.0', 'UVGH.1.0.0.0', 'USGH.1.0.0.0', 'ASGH.1.0.0.0', 'UBLH.1.0.0.0', 'UBLP.1.0.0.0',
    'USGN.1.0.0.0', 'USGP.1.0.0.0', 'UBYA.1.0.0.0', 'UBCA.1.0.0.0', 'UBLA.1.0.0.0', 'ILN.1.1.0.0', 'ISN.1.1.0.0'
]


# If Country in group 'Forecast: Countries from transfer matrix'
# Tail .1.0.0.0
AMECO_VARS_2 = [var + '.1.0.0.0' for var in TM]


# Tail .1.1.0.0
AMECO_VARS_3 = [var + '.1.1.0.0' for var in NA_VO]


# Variables from countries used explicitly in the calculations
INPUT_VARS_1 = [
    'NETN', 'UMSN', 'UXSN', 'UMGN', 'UMSN', 'UMGS', 'UIGG', 'UIGDW', 'UIGT', 'UIST', 'UXSN', 'UIST', 'OMSN', 'OXSN',
    'OMGN', 'OMSN', 'OMSN', 'OIGG', 'OIGDW', 'OIGT', 'OIST', 'OXSN', 'OIST', 'OMSN', 'OXSN', 'OMGN', 'OMSN', 'OMSN',
    'OIGG', 'OIGDW', 'OIGT', 'OIST', 'OXSN', 'OIST', 'UWWD', 'ZCPIH', 'NETD', 'NWTD', 'NETN', 'NETN', 'UCTG', 'UMGS',
]


# Expected variables calculated one by one in the existing calculations
EXPECTED_VARS_1 = [
    'NLTN.1.0.0.0', 'NSTD.1.0.0.0', 'NETD.1.0.414.0', 'NECN.1.0.0.0', 'NLHT.1.0.0.0', 'NLHT9.1.0.0.0', 'NLCN.1.0.0.0',
    'UMGS', 'UXGS', 'UBGN', 'UBSN', 'UBGS', 'UIGG', 'UIGP', 'UIGNR', 'UUNF', 'UUNT', 'UUTT', 'UITT', 'UMGS.1.0.0.0',
    'UXGS.1.0.0.0', 'UBGN.1.0.0.0', 'UBSN.1.0.0.0', 'UBGS.1.0.0.0', 'UIGG.1.0.0.0', 'UIGP.1.0.0.0', 'UIGNR.1.0.0.0',
    'UUNF.1.0.0.0', 'UUNT.1.0.0.0', 'UUTT.1.0.0.0', 'UITT.1.0.0.0', 'OMGS.1.0.0.0', 'OXGS.1.0.0.0', 'OBGN.1.0.0.0',
    'OBSN.1.0.0.0', 'OBGS.1.0.0.0', 'OIGP.1.0.0.0', 'OIGNR.1.0.0.0', 'OUNF.1.0.0.0', 'OUNT.1.0.0.0', 'OUTT.1.0.0.0',
    'OITT.1.0.0.0', 'CMGS.1.0.0.0', 'CBGS.1.0.0.0', 'CUNF.1.0.0.0', 'CIST.1.0.0.0', 'OVGD.6.1.212.0', 'UVGN.1.0.0.0',
    'UOGD.1.0.0.0', 'UTVNBP.1.0.0.0', 'UVGE.1.0.0.0', 'UWCDA.1.0.0.0', 'UWSC.1.0.0.0', 'UVGDH.1.0.0.0', 'KNP.1.0.212.0',
    'ZCPIH.6.0.0.0', 'OVGN.1.0.0.0', 'OVGN.6.0.0.0', 'UKCT.1.0.0.0', 'OKCT.1.0.0.0', 'OINT.1.0.0.0', 'OKND.1.0.0.0',
    'ZVGDFA3.3.0.0.0', 'XNE.1.0.99.0', 'XNEF.1.0.99.0', 'XNEB.1.0.99.0', 'XNU.1.0.30.0', 'FETD9.1.0.0.0',
    'FWTD9.1.0.0.0', 'RVGDE.1.0.0.0', 'RVGEW.1.0.0.0', 'RVGDAE.3.1.0.0', 'FETD9.6.0.0.0', 'ZUTN.1.0.0.0',
    'NUTN.1.0.0.0', 'PLCD.3.1.0.0', 'QLCD.3.1.0.0', 'ZATN9.1.0.0.0', 'ZETN9.1.0.0.0', 'ZUTN9.1.0.0.0', 'UTOG.1.0.0.0',
    'UUCG.1.0.0.0', 'URCG.1.0.0.0', 'UUTG.1.0.0.0', 'URTG.1.0.0.0', 'UBLG.1.0.0.0', 'UBLGE.1.0.0.0', 'UYIGE.1.0.0.0',
    'UBLGI.1.0.0.0', 'UBLGIE.1.0.0.0', 'UTAT.1.0.0.0', 'UOOMS.1.0.0.0', 'UTTG.1.0.0.0', 'UDGGL.1.0.0.0', 'UDGG.1.0.0.0',
    'EATTG.1.0.0.0', 'EATYG.1.0.0.0', 'EATSG.1.0.0.0', 'ETTG.1.0.0.0', 'RTTG.1.0.0.0', 'FTTG.1.0.0.0', 'ETYG.1.0.0.0',
    'RTYG.1.0.0.0', 'FTYG.1.0.0.0', 'ETSG.1.0.0.0', 'RTSG.1.0.0.0', 'FTSG.1.0.0.0', 'UCRG.1.0.0.0', 'USGG.1.0.0.0',
    'UUTGE.1.0.0.0', 'UUCGI.1.0.0.0', 'UTCT.1.0.0.0', 'USGC.1.0.0.0', 'UOGC.1.0.0.0', 'UBLC.1.0.0.0', 'UYOH.1.0.0.0',
    'UVGH.1.0.0.0', 'UVGHA.1.0.0.0', 'OVGHA.3.0.0.0', 'USGH.1.0.0.0', 'ASGH.1.0.0.0', 'UBLH.1.0.0.0', 'UBLP.1.0.0.0',
    'USGN.1.0.0.0', 'USGP.1.0.0.0', 'UBYA.1.0.0.0', 'UBCA.1.0.0.0', 'UBLA.1.0.0.0', 'DXGT.1.0.0.0', 'DMGT.1.0.0.0',
    'DBGT.1.0.0.0', 'DBGE.1.0.0.0', 'DBGI.1.0.0.0', 'OVGD.6.0.0.0', 'UTCGCP.1.0.319.0', 'UUCGCP.1.0.319.0',
    'UBLGCP.1.0.319.0', 'UBLGAP.1.0.319.0', 'UBLGBP.1.0.319.0', 'UBLGAPS.1.0.319.0', 'UBLGBPS.1.0.319.0',
    'OXGS.1.0.30.0', 'OMGS.1.0.30.0', 'OBGN.1.0.30.0', 'OBSN.1.0.30.0', 'OBGS.1.0.30.0', 'UXGS.1.0.30.0',
    'UMGS.1.0.30.0', 'UBGN.1.0.30.0', 'UBSN.1.0.30.0', 'UBGS.1.0.30.0', 'ZCPIH.12.0.0.0', 'ZCPIH.1.0.0.0',
    'CMGS.2.0.0.0', 'CBGS.2.0.0.0'
]