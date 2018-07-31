variable_group_names = {
    'TM': 'Transfer Matrix Variables',
    'TM_TBBO': 'Transfer Matrix variables, to be buttspliced only',
    'TM_TBM': 'Transfer Matrix variables, to be merged',
    'T_VO': 'Trade variables (Volume)',
    'PD': 'Price Deflator variables',
    'PD_Q': 'Price Deflator variables, in quarterly frequency',
    'NA_VO': 'National Account variables (Volume)',
    'NA_Q_VO': 'National Account variables, in quarterly frequency (Volume)',
    'NA_IS_VA': 'National Account variables, income side (Value)',
    'FL': 'Full List of Variables',
    'S_VA': 'Sector variables (Value)',
    'FL_FSMR': 'Full List of Variables, for small countries/regions',
    'I_VO': 'Index variables (Volume)',
    'RI_TBEBT1960': 'RATS Input variables, to be extended backwards to 1960',
}

I_VO = ['OVGHA.3.0.0.0']

PD_Q = ['ZCPIH', 'ZCPIXEF', 'ZCPIENG', 'ZCPIFOO', 'ZCPIUNF', 'ZCPINEG',
        'ZCPISER']

TM_TBM = ['UOOMSR', 'UOOMSE', 'UDMGCE', 'UDMGCR', 'UDMGKE', 'UDMGKTR']

NA_Q_VO = ['OCPH', 'OCTG', 'OIGT', 'OIST', 'OUNF', 'OUNT', 'OUTT', 'OVGD',
           'OXGS', 'OMGS']

NA_IS_VA = ['UVGD', 'UVGE', 'UTVNBP', 'UWCD', 'UWWD', 'UOGD', 'UWSC']

FL_FSMR = ['OVGD', 'UXGN', 'OXGN', 'UXSN', 'OXSN', 'UMGN', 'OMGN', 'UMSN',
           'OMSN', 'UBCA']

T_VO = ['OXGS', 'OMGS', 'OXGN', 'OXSN', 'OMGN', 'OMSN', 'OBGN', 'OBGS', 'OBSN']

NA_VO = ['OCPH', 'OCTG', 'OIGT', 'OIGCO', 'OIGDW', 'OIGNR', 'OIGEQ', 'OIGOT', 'OIST', 'OITT', 'OUNF', 'OUNT', 'OUTT',
         'OVGD', 'OVGE', 'OXGS', 'OMGS', 'OXGN', 'OXSN', 'OMGN', 'OMSN', 'OBGN', 'OBGS', 'OBSN', 'OIGG', 'OIGP']

PD = ['PCPH.3.1.0.0', 'PCTG.3.1.0.0', 'PIGT.3.1.0.0', 'PIGCO.3.1.0.0', 'PIGDW.3.1.0.0', 'PIGNR.3.1.0.0',
      'PIGEQ.3.1.0.0', 'PIGOT.3.1.0.0', 'PUNF.3.1.0.0', 'PUNT.3.1.0.0', 'PUTT.3.1.0.0', 'PVGD.3.1.0.0', 'PXGS.3.1.0.0',
      'PMGS.3.1.0.0', 'PXGN.3.1.0.0', 'PXSN.3.1.0.0', 'PMGN.3.1.0.0', 'PMSN.3.1.0.0', 'PIGP.3.1.0.0', 'PIST.3.1.0.0',
      'PVGE.3.1.0.0']

RI_TBEBT1960 = ['NPTD.1.0.0.0', 'NPAN.1.0.0.0', 'NPAN1.1.0.0.0', 'NLTN.1.0.0.0', 'NLCN.1.0.0.0', 'NECN.1.0.0.0',
                'NUTN.1.0.0.0', 'ZUTN.1.0.0.0', 'NETN.1.0.0.0', 'NETD.1.0.0.0', 'OIGT.1.1.0.0', 'OVGD.1.1.0.0',
                'OVGD.6.1.0.0', 'NLHA.1.0.0.0', 'OVGDT.1.0.0.0', 'PLCD.3.1.0.0', 'OKND.1.0.0.0', 'HWCDW.1.0.0.0',
                'UIGT.1.0.0.0', 'UVGD.1.0.0.0', 'UWCD.1.0.0.0', 'ZVGDFA3.3.0.0.0']

TM_TBBO = ['UCTG', 'UTVTBP', 'UYVTBP', 'UWCG', 'UBGS', 'UBGN', 'UBSN', 'UBRA', 'UBTA', 'UBCA', 'UBKA', 'DXGI', 'DXGE',
           'DMGI', 'DMGE', 'UGVAC', 'UYVC', 'UYNC', 'UCTRC', 'UTVC', 'UTYC', 'UEHC', 'UITC', 'UKOC', 'UOGC', 'UWCH',
           'UWSH', 'UYNH', 'UCTRH', 'UEHH', 'UTYH', 'UCTPH', 'UCPH0', 'UITH', 'UKOH', 'UOGH', 'UPOMN', 'UKCG0', 'UTVG',
           'UTYG', 'UTSG', 'UTAG', 'UROG', 'UKTTG', 'UCTGI', 'UYVG', 'UYTGH', 'UYTGM', 'UYIG', 'UCCG0', 'UCIG0', 'UUOG',
           'UIGG0', 'UKOG', 'UUTG', 'UYIGE', 'UBLGE']

TM = ['NPTD', 'NPAN', 'NPAN1', 'NLTN', 'NLCN', 'NUTN', 'ZUTN', 'NETN', 'NETD', 'FETD', 'NWTD', 'FWTD', 'UCPH', 'OCPH',
      'ZCPIH', 'ZCPIXEF', 'ZCPIENG', 'ZCPIFOO', 'ZCPIUNF', 'ZCPINEG', 'ZCPISER', 'ZCPIN', 'UCTG', 'OCTG', 'OCCG',
      'OCIG', 'UIGT', 'OIGT', 'UIGG', 'UIGP', 'UIGCO', 'UIGDW', 'UIGNR', 'UIGEQ', 'UIGOT', 'OIGCO', 'OIGDW', 'OIGNR',
      'OIGEQ', 'OIGOT', 'UIST', 'OIST', 'UUNF', 'OUNF', 'UUNT', 'OUNT', 'UUTT', 'OUTT', 'UVGN', 'UVGD', 'OVGD', 'NLHA',
      'UVGE', 'OVGE', 'UTVNBP', 'UTVTBP', 'UYVTBP', 'UWCD', 'UWCG', 'UWWD', 'UOGD', 'UXGS', 'OXGS', 'UMGS', 'OMGS',
      'UXGN', 'OXGN', 'UXSN', 'OXSN', 'UMGN', 'OMGN', 'UMSN', 'OMSN', 'UBGS', 'UBGN', 'UBSN', 'UBRA', 'UBTA', 'UBKA',
      'DXGI', 'DXGE', 'DMGI', 'DMGE', 'NETM', 'FETM', 'NWTM', 'FWTM', 'UGVAC', 'UYVC', 'UYNC', 'UCTRC', 'UTVC', 'UWCC',
      'UTYC', 'UEHC', 'UITC', 'UKOC', 'UOGC', 'UWCH', 'UWSH', 'UYNH', 'UCTRH', 'UEHH', 'UTYH', 'UCTPH', 'UCPH0', 'UITH',
      'UKOH', 'UOGH', 'UPOMN', 'UKCG0', 'UTVG', 'UTYG', 'UTSG', 'UTAG', 'UROG', 'UKTTG', 'UTKG', 'UKTG995', 'UCTGI',
      'UYVG', 'UYTGH', 'UYTGM', 'UYIG', 'UCCG0', 'UCIG0', 'UUOG', 'UIGG0', 'UKOG', 'UUTG', 'UYIGE', 'UBLGE', 'UOOMSR',
      'UOOMSE', 'UDMGCE', 'UDMGCR', 'UDMGKE', 'UDMGKTR', 'UDGG', 'USN90TE', 'UTNTE', 'NLFS', 'OBGN', 'OBGS', 'OBSN',
      'OIGC', 'OIGG', 'OIGH', 'OIGM', 'OIGP', 'TRDT', 'TRIT', 'TRSC', 'UBLM', 'USADCMG', 'USADCMY', 'USAXTMR',
      'USAXTMRB', 'USLCDMY', 'USLCUMY', 'USLDCMG', 'USLDPMY', 'USLXTMR', 'USLXTMRB', 'USN90M', 'USNDCMG', 'USNFBTR',
      'USNOIMU', 'USNTR', 'USNXTMR', 'USNXTMRB', 'UTADCMY', 'UTADERY', 'UTAFBRG', 'UTAFBRY', 'UTAXTMRB', 'UTEU',
      'UTLCDMY', 'UTLDERY', 'UTLFBRG', 'UTLFBRY', 'UTLXTMRB', 'UTNCATR', 'UTNDCMG', 'UTNDERY', 'UTNFBRG', 'UTNFBRY',
      'UTNG', 'UTNKATR', 'UTNM', 'UTNNBYG', 'UTNOIGU', 'UTNOIMU', 'UTNOIRT', 'UTNOIYU', 'UTNP', 'UTNXTMR', 'UTNXTMRB',
      'UWCM', 'UWSC', 'UWWM', 'UYEU', 'WCPIENG', 'WCPIFOO', 'WCPINEG', 'WCPISER', 'WCPIUNF', 'ZATN', 'ZETN']

S_VA = ['USGN.1.0.0.0', 'USGP.1.0.0.0', 'USGC.1.0.0.0', 'USGH.1.0.0.0', 'UBLA.1.0.0.0', 'UBLG.1.0.0.0', 'UBLC.1.0.0.0',
        'UBLH.1.0.0.0', 'UVGN.1.0.0.0', 'UVGDH.1.0.0.0', 'UTVNBP.1.0.0.0', 'UTVTBP.1.0.0.0', 'UYVTBP.1.0.0.0',
        'UWCG.1.0.0.0', 'UOGD.1.0.0.0', 'UBRA.1.0.0.0', 'UBTA.1.0.0.0', 'UBCA.1.0.0.0', 'UBKA.1.0.0.0', 'DXGT.1.0.0.0',
        'DXGI.1.0.0.0', 'DXGE.1.0.0.0', 'DMGT.1.0.0.0', 'DMGI.1.0.0.0', 'DMGE.1.0.0.0', 'UGVAC.1.0.0.0', 'UYVC.1.0.0.0',
        'UYNC.1.0.0.0', 'UCTRC.1.0.0.0', 'UTVC.1.0.0.0', 'UWCC.1.0.0.0', 'UTYC.1.0.0.0', 'UEHC.1.0.0.0', 'UITC.1.0.0.0',
        'UKOC.1.0.0.0', 'UOGC.1.0.0.0', 'UWCH.1.0.0.0', 'UWSH.1.0.0.0', 'UCTRH.1.0.0.0', 'UEHH.1.0.0.0', 'UTYH.1.0.0.0',
        'UCTPH.1.0.0.0', 'UCPH0.1.0.0.0', 'UITH.1.0.0.0', 'UKOH.1.0.0.0', 'UYOH.1.0.0.0', 'UVGH.1.0.0.0',
        'UVGHA.1.0.0.0', 'UPOMN.1.0.0.0', 'UKCG0.1.0.0.0', 'UTVG.1.0.0.0', 'UTYG.1.0.0.0', 'UTSG.1.0.0.0',
        'UTAG.1.0.0.0', 'UTAT.1.0.0.0', 'UTOG.1.0.0.0', 'URCG.1.0.0.0', 'UKTTG.1.0.0.0', 'URTG.1.0.0.0',
        'UCTGI.1.0.0.0', 'UYVG.1.0.0.0', 'UYTGH.1.0.0.0', 'UYTGM.1.0.0.0', 'UYIG.1.0.0.0', 'UCCG0.1.0.0.0',
        'UCIG0.1.0.0.0', 'UUOG.1.0.0.0', 'UUCG.1.0.0.0', 'UIGG0.1.0.0.0', 'UKOG.1.0.0.0', 'UUTG.1.0.0.0',
        'UBLGI.1.0.0.0', 'UYIGE.1.0.0.0', 'UUTGE.1.0.0.0', 'UBLGE.1.0.0.0', 'UBLGIE.1.0.0.0', 'UOOMS.1.0.0.0',
        'UOOMSR.1.0.0.0', 'UOOMSE.1.0.0.0', 'UDGG.1.0.0.0', 'UDGGL.1.0.0.0', 'USN90TE.1.0.0.0', 'UTNTE.1.0.0.0',
        'DBGE.1.0.0.0', 'DBGI.1.0.0.0', 'DBGT.1.0.0.0', 'UBGN.1.0.0.0', 'UBGS.1.0.0.0', 'UBLM.1.0.0.0', 'UBSN.1.0.0.0',
        'UBYA.1.0.0.0', 'UCRG.1.0.0.0', 'UCTG.1.0.0.0', 'UMGN.1.0.0.0', 'UMSN.1.0.0.0', 'USADCMG.1.0.0.0',
        'USADCMY.1.0.0.0', 'USAXTMR.1.0.0.0', 'USAXTMRB.1.0.0.0', 'USGG.1.0.0.0', 'USLCDMY.1.0.0.0', 'USLCUMY.1.0.0.0',
        'USLDCMG.1.0.0.0', 'USLDPMY.1.0.0.0', 'USLXTMR.1.0.0.0', 'USLXTMRB.1.0.0.0', 'USN90M.1.0.0.0',
        'USNDCMG.1.0.0.0', 'USNFBTR.1.0.0.0', 'USNOIMU.1.0.0.0', 'USNTR.1.0.0.0', 'USNXTMR.1.0.0.0', 'USNXTMRB.1.0.0.0',
        'UTADCMY.1.0.0.0', 'UTADERY.1.0.0.0', 'UTAFBRG.1.0.0.0', 'UTAFBRY.1.0.0.0', 'UTAXTMRB.1.0.0.0',
        'UTLCDMY.1.0.0.0', 'UTLDERY.1.0.0.0', 'UTLFBRG.1.0.0.0', 'UTLFBRY.1.0.0.0', 'UTLXTMRB.1.0.0.0',
        'UTNCATR.1.0.0.0', 'UTNDCMG.1.0.0.0', 'UTNDERY.1.0.0.0', 'UTNFBRG.1.0.0.0', 'UTNFBRY.1.0.0.0', 'UTNG.1.0.0.0',
        'UTNKATR.1.0.0.0', 'UTNM.1.0.0.0', 'UTNNBYG.1.0.0.0', 'UTNOIGU.1.0.0.0', 'UTNOIMU.1.0.0.0', 'UTNOIRT.1.0.0.0',
        'UTNOIYU.1.0.0.0', 'UTNP.1.0.0.0', 'UTNXTMR.1.0.0.0', 'UTNXTMRB.1.0.0.0', 'UTTG.1.0.0.0', 'UWCD.1.0.0.0',
        'UWCDA.1.0.0.0', 'UXGN.1.0.0.0', 'UXSN.1.0.0.0']
