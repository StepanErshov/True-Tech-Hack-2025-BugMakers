import os 
import json
import datetime
from config import *
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from typing import List


os.environ["OPENAI_API_KEY"] = KEY
os.environ["OPENAI_API_BASE"] = "http://localhost:11434"
os.environ["OPENAI_MODEL_NAME"] = "ollama/llama3"

CRM = {  
  "issue_type": "billing | technical | complaint",  
  "client_sentiment": "anger | neutral | happy",  
  "resolution": "compensation | escalation | info_provided"  
}  
@CrewBase
class LatestAiDevelopmentCrew():
    """Crew для обработки запросов техподдержки МТС"""
    agents: List[Agent]
    tasks: List[Task]

    @agent
    def intent_agent(self) -> Agent:
        return Agent(
            role="Аналитик намерений клиента",
            goal="Определить что хочет сделать клиент",
            backstory="""Ты помощник работника линии технической поддержки МТС,
            отвечающий за определение желания пользователя.""",
            verbose=True
        )

    @agent
    def knowledge_agent(self) -> Agent:
        return Agent(
            role="Эксперт по решениям",
            goal="Предложить решение проблемы клиента",
            backstory="""Ты помощник работника линии технической поддержки МТС,
            отвечающий за генерацию релевантных решений.""",
            verbose=True
        )

    @agent
    def emotion_agent(self) -> Agent:
        return Agent(
            role="Аналитик эмоций",
            goal="Оценить эмоциональное состояние клиента",
            backstory="""Ты помощник работника линии технической поддержки МТС,
            отвечающий за оценку эмоционального состояния клиента.""",
            verbose=True
        )

    @agent
    def action_s_agent(self) -> Agent:
        return Agent(
            role="Эксперт по генерации обратной связи",
            goal="Сгенерировать обратную свзяь для Клиента испходя из его эмоциональной оценки и намерений",
            backstory="""Ты помощник работка линии техничесской поддрежки МТС,
            отвечающий за генерацию фидбека для клиента с рекомендациями дальнейших действий
            на основе эмоционального состояния и намерений клиента"""
        )
    
    @agent
    def summary_agent(self) -> Agent:
        return Agent(
            role="Генератор CRM отчетов",
            goal=f"""Твоя задача на основении текста введенного пользователем
            собрать все необходимые параметры и на их основе сформировать CRM
            отчет в виде {CRM} парметры которые нужно для заполнения варируй сам!""",
            backstory=f"""Ты помощник работника лиинии поддержки МТС отвечающий за 
            сбор необходимой информации и сжатию ее в строгий формат вида {CRM}"""
        )
    
    @agent
    def qa_agent(self) -> Agent:
        return Agent(
            role="Советник по общению с клиентом",
            goal="""Твоя задача на основании эмоционального контеста пользователя 
            рекомандовать работнику коллцентра варинта общения с клиентом""",
            backstory="""Ты помощник работника колцентра который должен помогать 
            работнику общаться с клиентом корректирую возможные ошибки в диалоге"""
        )

    @task
    def intent_task(self) -> Task:
        return Task(
            description="""Определи что хочет сделать клиент на основе его запроса:
            {topic}""",
            expected_output="Точное описание проблемы/запроса клиента",
            agent=self.intent_agent()
        )

    @task
    def knowledge_task(self) -> Task:
        return Task(
            description="""Предложи решение проблемы клиента:
            {topic}""",
            expected_output="Релевантное решение проблемы клиента",
            agent=self.knowledge_agent()
        )

    @task
    def emotion_task(self) -> Task:
        return Task(
            description="""Оцени эмоциональное состояние клиента:
            {topic}""",
            expected_output="Оценка эмоционального состояния клиента",
            agent=self.emotion_agent()
        )

    @task
    def action_s_task(self) -> Task:
        return Task(
            description="""Генерация обратной свзяи для клиента на основе 
            его эмоционального состояния и намерений по входному тексту {topic}""",
            expected_output="""последовательность шагов которые работника
            колцентра может посоветовать предпринять клиенту""",
            agent=self.action_s_agent()
        )

    @task
    def summary_task(self) -> Task:
        return Task(
            description=f"""Генерация отчета CRM в формате {CRM} на текста
            введенного пользователем""",
            expected_output=f"json файл в формате: {CRM}",
            agent=self.summary_agent()
        )
    
    @task
    def qa_task(self) -> Task:
        return Task(
            description=f"""Предложение вариантов общения с клилентом на основе 
            его эмоционального состояния и корректировка возможных ошибок в 
            диалоге""",
            expected_output="""Сгенерированный текст с рекомендациями для проведения 
            диалогов""",
            agent=self.qa_agent()
        )
    

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )

if __name__ == "__main__":
    try:

        crew_instance = LatestAiDevelopmentCrew()
        crewww = crew_instance.crew()

        result = crew_instance.crew().kickoff(inputs={
            "topic": "не работает приложение связи, что мне делать, к кому мне обращаться?"
        })
        
        print(result)

        output_data = {
            'task_description': "не работает приложение связи, что мне делать, к кому мне обращаться?",
            'expected_output': "task.expected_output",
            "results": {
                "intent_analysis": str(crewww.tasks[0].output),
                "solution_proposal": str(crewww.tasks[1].output),
                "emotion_analysis": str(crewww.tasks[2].output),
                "action_s_agent": str(crewww.tasks[3].output),
                "summary_agent": str(crewww.tasks[4].output),
                "qa_agent": str(crewww.tasks[5].output)
            },
            'execution_time': datetime.datetime.now().isoformat(),
            'agent_role': "agent.role"
        }

        with open('results.json', 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

    except Exception as e:
        error_data = {
            "error": str(e),
            "timestamp": datetime.datetime.now().isoformat()
        }
        with open('error_log.json', 'w') as f:
            json.dump(error_data, f)
        print("Произошла ошибка:", e)

# result = crew.kickoff(inputs={'topic': 'AI Agents'})
# print(result)

# try:
#     output_data = {
#         'task_description': task.description,
#         'expected_output': task.expected_output,
#         'result': str(result),
#         'execution_time': datetime.datetime.now().isoformat(),
#         'agent_role': agent.role
#     }

#     with open('ai_results.json', 'w', encoding='utf-8') as f:
#         json.dump(output_data, f, ensure_ascii=False, indent=2)

# except Exception as e:
#     print(f"Произошла ошибка: {str(e)}")
#     with open('ai_error.json', 'w', encoding='utf-8') as f:
#         json.dump({'error': str(e), 'timestamp': datetime.datetime.now().isoformat()}, f)