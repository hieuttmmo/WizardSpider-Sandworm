import re
from unittest import result
from webbrowser import get
import requests
import xlsxwriter

VENDORS = ['ahnlab', 'bitdefender', 'checkpoint', 'cisco', 'crowdstrike', 'cybereason', 'cycraft', 'cylance', 'cynet', 'deepinstinct', 'elastic', 'eset', 'fidelis', 'fireeye', 'fortinet', 'malwarebytes', 'mcafee', 'microsoft', 'paloaltonetworks', 'qualys', 'rapid7', 'reaqta', 'sentinelone', 'somma', 'sophos', 'symantec', 'trendmicro', 'uptycs', 'vmware', 'withsecure']
RESULT_URL = 'https://attackevals.mitre-engenuity.org/api/export/?participant={0}&adversary=wizard-spider-sandworm'
HEADER = {'Accept': 'application/json',\
          'Accept-Language': 'en-US,en;q=0.5',\
          'Accept-Encoding': 'gzip, deflate, br',\
          'Referer': 'https://attackevals.mitre-engenuity.org/enterprise/participants/ahnlab?view=overview&adversary=wizard-spider-sandworm',\
          'DNT': '1',\
          'Connection': 'keep-alive', 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors','Sec-Fetch-Site': 'same-origin', 'Sec-GPC': '1'
         }
class Workbook():
    def __init__(self) -> None:
        self.workbook = xlsxwriter.Workbook('wizard-spider-sandworm-mitre-consolidate.xlsx')
        self.worksheet = self.workbook.add_worksheet('Consolidate')
        self.columns = ['Vendor','Substep', 'Criteria', 'Tactic', 'TechniqueId', 'TechniqueName', 'SubtechniqueId', 'SubtechniqueName', 'Detection']
        self.current_row_index = 0

    def workbook_init(self):
        row_index = 0
        column_index = 0
        for column_name in self.columns:
            self.worksheet.write(row_index, column_index, column_name)
            column_index += 1
        self.current_row_index +=1

    def workbook_close(self):
        self.workbook.close()
        
    def get_vendor_result(self): 
        results = []
        for vendor in VENDORS:        
            r = requests.get(RESULT_URL.format(vendor), headers=HEADER, verify=False)
            temp = r.json()[0]
            results.append(temp)
        return results

    def write_vendor_result(self, vendor_result):
        for scenario in vendor_result['Adversaries'][0]['Detections_By_Step']:
            for step in vendor_result['Adversaries'][0]['Detections_By_Step'][scenario]['Steps']:
                for substep in step['Substeps']:
                    pre_format = [vendor_result['Participant_Name'], substep['Substep'], substep['Criteria'], substep['Tactic']['Tactic_Name'], substep['Technique']['Technique_Id'], substep['Technique']['Technique_Name'], substep['Subtechnique']['Subtechnique_Id'], substep['Subtechnique']['Subtechnique_Name'], substep['Detections'][0]['Detection_Type']]
                    for i in range(len(pre_format)):
                        self.worksheet.write(self.current_row_index,i,pre_format[i])
                    self.current_row_index += 1

def main():
    workbook = Workbook()
    workbook.workbook_init()
    results = workbook.get_vendor_result()
    for result in results:
        workbook.write_vendor_result(result)
    workbook.workbook_close()

if __name__ == main():
    main()


