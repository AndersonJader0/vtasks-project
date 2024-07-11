## Refatorar


from login_azure import LoginAzure
from excel_generator import ExcelGenerator
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import re


class TasksOperator(LoginAzure):
    def __init__(self):
        super()._init_()
        self.tasks = []
        self.environment = []
        self.PROD = ['prod', 'producao', 'produção']
        self.PRE = ['pre', 'pré', 'pre-prod', 'pré-prod', 'pre-producao', 'pré-produção']
        self.HML2 = ['hml','hml2','homologue','homologação']
        self.USERS_DEPLOY = ['@anderson', '@leandro', '@vinicius', '@lucas']
        self.hasEffort = False
        self.effort = ''
 
# ----------------------------------
#   Obtenção das tarefas
# ----------------------------------
    
    def get_tasks(self):
        self.authenticate()
        self.wait.until(EC.presence_of_element_located((By.XPATH , '//button[@class="bolt-button enabled subtle bolt-focus-treatment"]')))
 
        num_committeds = self.browser.find_elements(By.XPATH, '//div[@class="flex-column flex-grow kanban-board-column padding-bottom-8"][3]/div/div/span/a/span[2]')
        name_committeds = self.browser.find_elements(By.XPATH, '//div[@class="flex-column flex-grow kanban-board-column padding-bottom-8"][3]/div/div/span/a/span[3]')

 
        num_approveds = 0
        i = 0
        for num_committed, name_committed in zip(num_committeds, name_committeds):
            name_committed = self.format_text(name_committed.text) 
            self.tasks.append({
                'PBI':num_committed.text,
                'DESCRIÇÃO':name_committed,
                'STATUS': '',
                'EFFORT': ''
            })
            status = self.check_tasks(num_committed)
            status = self.format_text(status)

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
                match self.hasEffort:
                    case True:
                        self.tasks[i]['EFFORT'] = self.effort
                        self.hasEffort = False
                    case False:
                        self.tasks[i]['EFFORT'] = 'faltou'
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
        tasks_excel = ExcelGenerator()
        tasks_excel.getExcel(self.tasks, num_approveds)

# ----------------------------------
#   Verificação se está aprovada
# ----------------------------------
    
    def check_tasks(self, num_committed):
        num_committed.click()
        try:
            first_comment = self.browser.find_element(By.XPATH, '//div[@class="comment-item flex-row displayed-comment depth-8 markdown-discussion-comment"]/div[2]').text
            second_comment = ''
            try: 
                self.browser.implicitly_wait(1)
                second_comment = self.browser.find_element(By.XPATH, '//div[@class="comment-item flex-row displayed-comment depth-8 markdown-discussion-comment"][2]/div[2]').text
            except:
                self.browser.implicitly_wait(10)
                second_comment = ''
            comment = first_comment + second_comment
            comment = self.format_text(comment)

            APROVADA = ['aprovada', 'aprovado', 'ok em pré', 'correto em pré', 'correto em pre', 'correta em pré', 'correta em pre']
            if any(aprov in comment for aprov in APROVADA):
                self.check_effort()
                status = 'aprovada'
                if any(prod in comment for prod in self.PROD):
                    self.environment = 'PROD'
                    return status
                elif any(pre in comment for pre in self.PRE):
                    self.environment = 'PRE'
                    return status
                elif any(hml2 in comment for hml2 in self.HML2):
                    self.environment = 'HML2'
                    return status
            elif all(aprov not in comment for aprov in APROVADA):
                status = self.check_test(comment)
                return status
        except:
            status = self.check_test(comment)
            return status
        
# ----------------------------------
#   Tratamento do texto do título
# ----------------------------------
    
    def format_text(self, text):
        if any(user + ' - testar' in text for user in self.USERS_DEPLOY):
            text = text.replace('@', '')
            return text
        elif 'sustentação -' in text.lower() or 'sustentação-' in text.lower():
            SUSTENTACAO = ['Sustentação -', 'Sustentação - ', 'Sustentação-']
            PRIORITY = ['-Q[1,2,3]', '- Q[1,2,3]', ' - Q[1,2,3]']
            for sust in SUSTENTACAO:
                if sust in text:
                    text = text.replace(sust, '')
            text = re.sub(PRIORITY[0], '', text)
            text = re.sub(PRIORITY[1], '', text)
            text = re.sub(PRIORITY[2], '', text)
            return text
        else:
            text = text.replace('<','')
            text = text.lower()
            return text
        
# ----------------------------------
#   Verificação quem precisa testar
# ----------------------------------
    
    def check_test(self, comment):
        status = ''
        i = 0

        if 'testar' not in comment and 'validar' not in comment:
            status = ''
            return status
        else:
            if all(user in comment for user in self.USERS_DEPLOY):
                status = 'testar'
                return status
            elif any(user in comment for user in self.USERS_DEPLOY):
                for user in self.USERS_DEPLOY:
                    if user in comment:
                        status = user + ' - testar'
                        i += 1
                        if i == 2:
                            return 'testar'
                return status
            else:
                status = ''
                return status
            
# ----------------------------------
#   Verificação se possui effort
# ----------------------------------

    def check_effort(self):
        try:
            self.effort = self.browser.find_element(By.XPATH, '//div[@class="work-item-form-control-wrapper"][2]/div/div[2]/div/div/input')
            self.effort = self.effort.get_attribute('value')
            if self.effort != '':
                self.hasEffort = True
            return
        except:
            print('Erro')
            return
 
tasksOperator = TasksOperator()
tasksOperator.get_tasks()