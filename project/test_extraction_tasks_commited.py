from test_login import Test_Login
from test_excel import Test_Excel
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import re


class Test_ExtractTasksCommitted(Test_Login):
    tasks = []
    environment = ''
 
    def _init_(self):
        self.tasks = self.tasks
        self.environment = self.environment
        super()._init_()
 
    def test_getTaskApproved(self):
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
            status = self.test_check_approval_tasks(num_committed)
            if status == 'Aprovada':
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
            i += 1
 
        test_tasks = Test_Excel()
        test_tasks.test_get_excel(self.tasks, num_approveds)
 
    def test_check_approval_tasks(self, name_committed):
        name_committed.click()
        try:
            verify = self.browser.find_element(By.XPATH, '//div[@class="comment-item flex-row displayed-comment depth-8 markdown-discussion-comment"]/div[2]').text
            if 'aprovada' in verify.lower() or 'aprovado' in verify.lower():
                status = 'Aprovada'
                if 'prod' in verify.lower() or 'produção' in verify.lower():
                    self.environment = 'PROD'
                    self.browser.back()
                    return status
                elif 'pre' in verify.lower() or 'pré' in verify.lower():
                    self.environment = 'PRE'
                    self.browser.back()
                    return status
                elif 'hml' in verify.lower() or 'hml2' in verify.lower():
                    self.environment = 'HML2'
                    self.browser.back()
                    return status
            else:
                status = ''
                self.browser.back()
                return status
        except:
            status = ''
            self.browser.back()
            return status
 
test_extractionTasksCommited = Test_ExtractTasksCommitted()
test_extractionTasksCommited.test_getTaskApproved()