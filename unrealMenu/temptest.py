import sys
import os
sys.path.append(r'c:/CgTeamWork_v6/bin/base')
import cgtw2


t = cgtw2.tw('192.168.1.246:8383','TDDATA','abc123456')
epsDict = {'J01': '27480F90-5566-686B-74F1-0D72CE377211', 'J02': '84B6B7EF-9503-4117-61EB-929CD75B5507', 'J03': '4729C79F-4286-1E90-9055-61EC335AA54E', 'J04': '304B9DCE-5A8E-CD3E-088A-840492917D88', 'J05': '94D0FB95-C6A1-FF35-9DC3-35494FCAA794', 'PV': 'CDCFBB3A-5F9D-FCEC-7CCE-A7582A10286C', 'J06': 'F48AD2D8-942D-4E43-63B9-6F93E86CF2C8', 'J07': '2D92D621-A706-4B03-8C8E-78A8E146EB36', 'J08': '91C7E2BB-14E8-AEDE-7090-B17FEC35C9D7', 'J09': '0B9B22B1-2A74-3863-2804-3FEE70D7F6BF', 'J10': 'CF2BBC96-EF85-A115-7B07-AD73590ED1E6', 'PV02': '1E092760-A409-3644-2E39-B4B7415E3929'}
shotDict = {'J01': [], 'J02': [], 'J03': [], 'J04': [], 'J05': [], 'PV': ['PV_021', 'PV_001', 'PV_007-008', 'PV_005', 'PV_006', 'PV_009-011', 'PV_004', 'PV_019', 'PV_002', 'PV_003', 'PV_020', 'PV_016', 'PV_014-015', 'PV_017', 'PV_012', 'PV_012A', 'PV_013', 'PV_017A', 'PV_018'], 'J06': [], 'J07': [], 'J08': [], 'J09': [], 'J10': [], 'PV02': ['PV02_035', 'PV02_020', 'PV02_031', 'PV02_024', 'PV02_026', 'PV02_014', 'PV02_036', 'PV02_039', 'PV02_042', 'PV02_022', 'PV02_048', 'PV02_017', 'PV02_015', 'PV02_003A', 'PV02_005', 'PV02_030', 'PV02_027', 'PV02_046', 'PV02_047', 'PV02_028', 'PV02_038', 'PV02_012', 'PV02_011', 'PV02_020C', 'PV02_018', 'PV02_032', 'PV02_049', 'PV02_019', 'PV02_041', 'PV02_037', 'PV02_020E', 'PV02_040', 'PV02_033', 'PV02_029', 'PV02_021', 'PV02_044', 'PV02_045', 'PV02_003', 'PV02_010', 'PV02_013', 'PV02_016', 'PV02_001', 'PV02_043', 'PV02_050', 'PV02_002', 'PV02_006', 'PV02_009', 'PV02_004', 'PV02_016A', 'PV02_020F', 'PV02_008A', 'PV02_020G', 'PV02_017B', 'PV02_017A', 'PV02_020D', 'PV02_020A', 'PV02_008C', 'PV02_025', 'PV02_034', 'PV02_011A', 'PV02_007', 'PV02_023', 'PV02_008', 'PV02_008B', 'PV02_020B']}

shotDict = {}
for key in epsDict.keys():
    shotDict[key] = []
shotIDs = t.info.get_id('proj_zw', 'shot', [])
shotDataList = t.info.get('proj_zw', 'shot', shotIDs, ['shot.link_eps', 'shot.entity'])
if shotDataList:
    for shotInfo in shotDataList:
        for eps in epsDict.keys():
            if shotInfo['shot.link_eps']  == eps:
                shotDict[shotInfo['shot.link_eps']].append(shotInfo['shot.entity'])



print (shotDict)
