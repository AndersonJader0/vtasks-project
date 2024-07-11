import re
from login_azure import LoginAzure
from excel_generator import ExcelGenerator
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TasksOperator(LoginAzure):
    def __init__(self):
        super()._init_()
        self.tasks = []
        self.tasks_ordened = []
        self.environment = None

    def get_tasks(self):
        self.authenticate()
        self.wait.until(EC.presence_of_element_located((By.XPATH , '//button[@class="bolt-button enabled subtle bolt-focus-treatment"]')))

        number_committeds = self.browser.find_elements(By.XPATH, '//div[@class="flex-column flex-grow kanban-board-column padding-bottom-8"][3]/div/div/span/a/span[2]')
        name_committeds = self.browser.find_elements(By.XPATH, '//div[@class="flex-column flex-grow kanban-board-column padding-bottom-8"][3]/div/div/span/a/span[3]')
        number_approveds = 0

        for i, (number_committed, name_committed) in enumerate(zip(number_committeds, name_committeds)):
            self.process_task(number_committed, name_committed, i)
            if self.tasks[i]['STATUS'].startswith('OK'):
                number_approveds += 1

        # print(sorted(int(self.tasks[]['PBI'].values())))

        # for task in self.tasks:
        print(max(self.tasks['PBI'].values()))
        # print(max(int(self.tasks['PBI'].values)))


        # excel = ExcelGenerator()
        # excel.getExcel(self.tasks, number_approveds)

    def process_task(self, number_committed, name_committed, index):
        number_committed_text = number_committed.text
        name_committed_text = self.format_text_task(name_committed.text)
        
        self.tasks.append({
            'PBI': int(number_committed_text),
            'DESCRIÇÃO': name_committed_text,
            'STATUS': '',
            'EFFORT': '',
        })

    def format_text_task(self, text):
        SUSTENTACAO = ['Sustentação -', 'Sustentacao -', 'Sustentacão -', 'Sustentaçao']
        PRIORITY = ['-Q[1,2,3]', '- Q[1,2,3]', ' - Q[1,2,3]']
        if any(sustentacao.lower() in text.lower() for sustentacao in SUSTENTACAO):
            for sustentacao in SUSTENTACAO:
                if sustentacao in text:
                    text = text.replace(sustentacao, '')
            for Q in range(0, 3):
                text = re.sub(PRIORITY[Q], '', text)
            return text
            
    
tasksOperator = TasksOperator()
tasksOperator.get_tasks()