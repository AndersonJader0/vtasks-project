from login_vsts import LoginVSTS
from excel_generator import excelGenerator
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import re


class MainTasks(LoginVSTS):
    tasks = []
    environment = ''
    PROD = ['prod', 'producao', 'produção']
    PRE = ['pre', 'pré', 'pre-prod', 'pré-prod', 'pre-producao', 'pré-produção']
    HML2 = ['hml','hml2','homologue','homologação']
    USERS_DEPLOY = ['@anderson', '@leandro', '@vinicius', '@lucas']
 
    def _init_(self):
        self.tasks = self.tasks
        self.environment = self.environment
        self.PROD = self.PROD
        self.PRE = self.PRE
        self.HML2 = self.HML2
        self.USERS_DEPLOY = self.USERS_DEPLOY
        super()._init_()
 
    def getTasks(self):
        self.Authentication()
        self.wait.until(EC.presence_of_element_located((By.XPATH , '//button[@class="bolt-button enabled subtle bolt-focus-treatment"]')))
 
        num_committeds = self.browser.find_elements(By.XPATH, '//div[@class="flex-column flex-grow kanban-board-column padding-bottom-8"][3]/div/div/span/a/span[2]')
        name_committeds = self.browser.find_elements(By.XPATH, '//div[@class="flex-column flex-grow kanban-board-column padding-bottom-8"][3]/div/div/span/a/span[3]')
 
        num_approveds = 0
        i = 0
        for num_committed, name_committed in zip(num_committeds, name_committeds):
            name_committed = self.formatText(name_committed.text) 
            self.tasks.append({
                'PBI':num_committed.text,
                'DESCRIÇÃO':name_committed,
                'STATUS': ''
            })
            status = self.checkTasks(num_committed)
            status = self.formatText(status)

            if status == 'aprovada':
                match self.environment:
                    case 'HML2':
                        self.tasks[i]['STATUS'] = 'OK - HML2'
                        self.environment = ''
                        num_approveds += 1
                    case 'PRE':
                        self.tasks[i]['STATUS'] = 'OK - PRE'
                        self.environment = ''
                        num_approveds += 1
                    case 'PROD':
                        self.tasks[i]['STATUS'] = 'OK - PROD'
                        self.environment = ''
                        num_approveds += 1
            elif status != 'aprovada':
                match status:
                    case 'testar':
                        self.tasks[i]['STATUS'] = 'testar'
                    case 'lucas - testar':
                        self.tasks[i]['STATUS'] = status
                    case 'anderson - testar':
                        self.tasks[i]['STATUS'] = status
                    case 'vinicius - testar':
                        self.tasks[i]['STATUS'] = status
                    case 'leandro - testar':
                        self.tasks[i]['STATUS'] = status
                    case '':
                        self.tasks[i]['STATUS'] = ''
            i += 1
            self.browser.back()
        tasks_excel = excelGenerator()
        tasks_excel.getExcel(self.tasks, num_approveds)

    def checkTasks(self, num_committed):
        
        num_committed.click()
        try:
            verify = self.browser.find_element(By.XPATH, '//div[@class="comment-item flex-row displayed-comment depth-8 markdown-discussion-comment"]/div[2]').text
            verify = self.formatText(verify)
            if 'aprovada' in verify or 'aprovado' in verify:
                status = 'aprovada'
                if any(prod in verify for prod in self.PROD):
                    self.environment = 'PROD'
                    return status
                elif any(pre in verify for pre in self.PRE):
                    self.environment = 'PRE'
                    return status
                elif any(hml2 in verify for hml2 in self.HML2):
                    self.environment = 'HML2'
                    return status
            elif 'aprovada' not in verify or 'aprovado' not in verify:
                status = self.checkTest(verify)
                return status
        except:
            status = self.checkTest(verify)
            return status
        
    def formatText(self, text):
        if text == '@lucas - testar' or text == '@anderson - testar' or text == '@leandro - testar' or text == '@vinicius - testar':
            text = text.replace('@', '')
            return text
        elif 'Sustentação - ' in text or 'Sustentação-' in text or 'sustentação -' in text or 'sustentação-' in text:
            text = text.replace('Sustentação - ','')
            text = text.replace('Sustentação-', '')
            text = text.replace('sustentação -', '')
            text = text.replace('sustentação-', '')
            text = re.sub(" - Q[1,2,3]", '', text)
            text = re.sub("- Q[1,2,3]",'', text)
            text = re.sub("-Q[1,2,3]", '', text)
            return text
        else:
            text = text.replace('<','')
            text = text.lower()
            return text
        
    def checkTest(self, verify):
        status = ''
        i = 0

        if 'testar' not in verify and 'validar' not in verify:
            status = ''
            return status
        else:
            if all(user in verify for user in self.USERS_DEPLOY):
                status = 'testar'
                return status
            elif any(user in verify for user in self.USERS_DEPLOY):
                for user in self.USERS_DEPLOY:
                    if user in verify:
                        status = user + ' - testar'
                        i += 1
                        if i == 2:
                            return 'testar'
                return status
            else:
                status = ''
                return status
 
mainTasks = MainTasks()
mainTasks.getTasks()