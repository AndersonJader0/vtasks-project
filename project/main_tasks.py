from login_vsts import LoginVSTS
from excel_generator import excelGenerator
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import re


class MainTasks(LoginVSTS):
    tasks = []
    environment = ''
 
    def _init_(self):
        self.tasks = self.tasks
        self.environment = self.environment
        super()._init_()
 
    def getTasks(self):
        self.Authentication()
        self.wait.until(EC.presence_of_element_located((By.XPATH , '//button[@class="bolt-button enabled subtle bolt-focus-treatment"]')))
 
        num_committeds = self.browser.find_elements(By.XPATH, '//div[@class="flex-column flex-grow kanban-board-column padding-bottom-8"][3]/div/div/span/a/span[2]')
        name_committeds = self.browser.find_elements(By.XPATH, '//div[@class="flex-column flex-grow kanban-board-column padding-bottom-8"][3]/div/div/span/a/span[3]')
 
        num_approveds = 0
        i = 0
        for num_committed, name_committed in zip(num_committeds, name_committeds):
            self.tasks.append({
                'PBI':num_committed.text,
                'DESCRIÇÃO':re.sub("- Q[1,2,3]", "", name_committed.text.replace('Sustentação - ', '')),
                'STATUS': ''
            })
            status = self.checkTasks(num_committed)
            self.browser.back()
            if status == 'aprovada':
                if self.environment == 'HML2':
                    self.tasks[i]['STATUS'] = 'OK - HML2'
                    self.environment = ''
                    num_approveds += 1
                elif self.environment == 'PRE':
                    self.tasks[i]['STATUS'] = 'OK - PRE'
                    self.environment = ''
                    num_approveds += 1
                elif self.environment == 'PROD':
                    self.tasks[i]['STATUS'] = 'OK - PROD'
                    self.environment = ''
                    num_approveds += 1
            elif status != 'aprovada': 
                if status == 'testar':
                    self.tasks[i]['STATUS'] = 'Testar'
                elif status == 'Lucas - testar':
                    self.tasks[i]['STATUS'] = status
                elif status == 'Anderson - testar':
                    self.tasks[i]['STATUS'] = status
                elif status == 'Vinicius - testar':
                    self.tasks[i]['STATUS'] = status
                elif status == 'Leandro - testar':
                    self.tasks[i]['STATUS'] = status
                else:
                    self.tasks[i]['STATUS'] = ''
            i += 1

 
        tasks_excel = excelGenerator()
        tasks_excel.getExcel(self.tasks, num_approveds)
 
    def checkTasks(self, name_committed):
        name_committed.click()
        try:
            verify = self.browser.find_element(By.XPATH, '//div[@class="comment-item flex-row displayed-comment depth-8 markdown-discussion-comment"]/div[2]').text
            if 'aprovada' in verify.lower() or 'aprovado' in verify.lower():
                status = 'aprovada'
                if 'prod' in verify.lower() or 'produção' in verify.lower():
                    self.environment = 'PROD'
                    return status
                elif 'pre' in verify.lower() or 'pré' in verify.lower():
                    self.environment = 'PRE'
                    return status
                elif 'hml' in verify.lower() or 'hml2' in verify.lower():
                    self.environment = 'HML2'
                    return status
            elif 'aprovada' not in verify.lower() or 'aprovado' not in verify.lower():
                status = self.checkTest(verify)
                return status

        except:
            status = self.checkTest(verify)
            return status
        
    def checkTest(self, verify):
        verify.replace('<','')
        status = ''
        if 'testar' in verify or 'validar' in verify:
            if '@Lucas' in verify or '@Anderson' in verify or '@Vinicius' in verify or '@Leandro' in verify:
                if '@Anderson' not in verify and '@Vinicius' not in verify and '@Leandro' not in verify:
                    status = 'Lucas - testar'
                    return status
                elif '@Lucas' not in verify and '@Vinicius' not in verify and '@Leandro' not in verify:
                    status = 'Anderson - testar'
                    return status
                elif '@Lucas' not in verify and '@Anderson' not in verify and '@Leandro' not in verify:
                    status = 'Vinicius - testar'
                    return status
                elif '@Lucas' not in verify and '@Anderson' not in verify and '@Vinicius' not in verify:
                    status = 'Leandro - testar'
                    return status
                elif '@Lucas' in verify and '@Anderson' in verify and '@Vinicius' in verify:
                    status = 'testar'
                    return status
                else:
                    status = 'testar'
                    return status
            else:
                status = ''
                return status
        elif 'testar' not in verify or 'validar' not in verify:
            status = ''
            return status

 
mainTasks = MainTasks()
mainTasks.getTasks()